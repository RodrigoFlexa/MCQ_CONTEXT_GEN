"""Constrói o inventário de conhecimento (fichas por assunto) do PetroQuest.

Exemplo (PowerShell, na raiz do repositório):

    python -u pipeline/inventario/run_inventario.py `
        --corpus-manifest dataset/domain_corpora/manifest.json `
        --subtopicos "Gestão do Desempenho Empresarial (KPI)" "Manutenção e Plano de Manutenção" `
        --output pipeline/inventario/saida_piloto

Repetir o mesmo comando retoma de onde parou (cache de LLM, varredura e vetores).
"""
import argparse
import json
import math
import sys
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.inventario import VERSION  # noqa: E402
from pipeline.inventario import assuntos as A  # noqa: E402
from pipeline.inventario import consolidacao as C  # noqa: E402
from pipeline.inventario import extracao as X  # noqa: E402
from pipeline.inventario import fichas as F  # noqa: E402
from pipeline.inventario import selecao as S  # noqa: E402
from pipeline.inventario import varredura as V  # noqa: E402
from pipeline.inventario import revisao as R  # noqa: E402
from pipeline.inventario.llm import LLMClient, load_dotenv  # noqa: E402
from pipeline.inventario.textutil import (atomic_json, norm, read_json, read_jsonl, sha, slug,  # noqa: E402
                                          write_jsonl)

STAGES = ('assuntos', 'varredura', 'selecao', 'extracao', 'revisao', 'consolidacao', 'fichas')


class Log:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()

    def __call__(self, *parts):
        msg = ' '.join(str(p) for p in parts)
        line = f"{datetime.now().strftime('%H:%M:%S')} {msg}"
        with self.lock:
            print(line, flush=True)
            with self.path.open('a', encoding='utf-8') as f:
                f.write(line + '\n')


def parse(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--corpus-manifest', default='dataset/domain_corpora/manifest.json')
    p.add_argument('--allow-sample-corpus', action='store_true', help='aceita manifesto de amostra (testes)')
    p.add_argument('--output', default='pipeline/inventario/saida')
    p.add_argument('--topicos', nargs='*', default=[], help='nomes (ou partes) de tópicos; vazio = todos')
    p.add_argument('--subtopicos', nargs='*', default=[], help='nomes (ou partes) de subtópicos; vazio = todos')
    p.add_argument('--llm-provider', choices=['azure', 'openai'], default='azure')
    p.add_argument('--llm-model', default=None, help='deployment Azure; padrão gpt-5-4-petrobras')
    p.add_argument('--plan', action='store_true', help='valida parâmetros e corpora, lista o recorte, sem chamadas')
    p.add_argument('--check-api', action='store_true', help='teste curto real: um pedido LLM e embeddings, sem corpora')
    p.add_argument('--effort', default='medium', choices=['none', 'low', 'medium', 'high'])
    p.add_argument('--workers', type=int, default=4, help='chamadas LLM simultâneas')
    p.add_argument('--max-chamadas', type=int, default=30000)
    p.add_argument('--embedder', default='embedding-3-large-global',
                   choices=['embedding-3-large-global', 'BAAI/bge-m3', 'hash'])
    p.add_argument('--reranker', default='none', help='none = similaridade densa; BAAI/bge-reranker-v2-m3 exige GPU')
    p.add_argument('--device', default='cuda', help='para modelos locais: cuda ou cuda:N; Azure não usa GPU local')
    p.add_argument('--embed-batch', type=int, default=64)
    p.add_argument('--rerank-batch', type=int, default=32)
    p.add_argument('--chunk-words', type=int, default=350)
    p.add_argument('--chunk-stride', type=int, default=250)
    p.add_argument('--candidatos-por-colecao', type=int, default=40)
    p.add_argument('--dense-top', type=int, default=60)
    p.add_argument('--trechos-por-assunto', type=int, default=12)
    p.add_argument('--min-rerank', type=float, default=0.10)
    p.add_argument('--limiar-consolidacao', type=float, default=0.86)
    p.add_argument('--review-batch', type=int, default=8, help='unidades por chamada do revisor/refinador')
    p.add_argument('--parar-apos', choices=STAGES, default='fichas')
    p.add_argument('--limite-unidades', type=int, default=None, help='TESTE: lê só N páginas/linhas por coleção')
    return p.parse_args(argv)


def validate_args(args):
    for key in ('workers', 'max_chamadas', 'embed_batch', 'rerank_batch', 'chunk_words', 'chunk_stride',
                'candidatos_por_colecao', 'dense_top', 'trechos_por_assunto', 'review_batch'):
        if getattr(args, key) < 1:
            raise ValueError(f'{key} deve ser positivo')
    if args.chunk_words < 80 or args.chunk_stride > args.chunk_words:
        raise ValueError('Trechos >=80 palavras e stride <= chunk_words')
    if args.limite_unidades is not None and args.limite_unidades < 1:
        raise ValueError('limite-unidades deve ser positivo')
    for key in ('min_rerank', 'limiar_consolidacao'):
        v = getattr(args, key)
        if not math.isfinite(v) or not 0 <= v <= 1:
            raise ValueError(f'{key} deve estar entre 0 e 1')
    if args.plan and args.check_api:
        raise ValueError('Escolha --plan ou --check-api')
    if args.reranker not in ('none', '', 'BAAI/bge-reranker-v2-m3'):
        raise ValueError('Reranker: none ou BAAI/bge-reranker-v2-m3')
    if args.embedder == 'hash' and args.reranker not in ('none', ''):
        raise ValueError('O substituto hash é apenas para testes sem reranker local')


def select_subtopics(topicos, want_topics, want_subs):
    wt = [norm(x) for x in want_topics]
    ws = [norm(x) for x in want_subs]
    out = []
    for t, subs in topicos.items():
        if wt and not any(w in norm(t) for w in wt):
            continue
        for s, frase in subs.items():
            if ws and not any(w == norm(s) or w in norm(s) for w in ws):
                continue
            key = sha(t + '||' + s, 10)
            out.append({'key': key, 'topico': t, 'subtopico': s, 'frase': frase,
                        'dir': f"{slug(t, 28)}__{slug(s, 40)}-{key[:4]}"})
    return out


def main(argv=None):
    args = parse(argv)
    validate_args(args)
    from pipeline.inventario.locking import output_lock
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    with output_lock(output):
        return run_main(argv)


def run_main(argv=None):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:  # noqa: BLE001
        pass
    args = parse(argv)
    validate_args(args)
    load_dotenv(ROOT)
    import os
    model = args.llm_model or ('gpt-5-4-petrobras' if args.llm_provider == 'azure' else
                               os.environ.get('INVENTARIO_LLM_MODEL', 'gpt-6-luna'))
    out = Path(args.output)
    if not out.is_absolute():
        out = ROOT / out
    out.mkdir(parents=True, exist_ok=True)
    log = Log(out / 'execucao.log')
    t0 = time.time()
    timings = {}
    from pipeline.fase_3.topicos import TOPICOS
    subs = select_subtopics(TOPICOS, args.topicos, args.subtopicos)
    if not subs:
        raise SystemExit('Nenhum subtópico corresponde ao filtro informado.')
    log(f"[início] {VERSION} | modelo={model} effort={args.effort} | {len(subs)} subtópicos | saída={out}")
    from pipeline.domain_corpora.manifest import load_manifest
    manifest_path = Path(args.corpus_manifest)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    collections = None
    if not args.check_api and (args.plan or args.parar_apos != 'assuntos'):
        log('[corpora] verificando arquivos e hashes antes de qualquer chamada...')
        _, collections = load_manifest(manifest_path, allow_sample=args.allow_sample_corpus)
    if args.plan:
        for sub in subs:
            log(f"[plano] {sub['topico']} / {sub['subtopico']}")
        log(f'[plano] {len(subs)} subtópicos; provider={args.llm_provider}; modelo={model}; '
            f'embeddings={args.embedder}; reranker={args.reranker}; chamadas=0; somente documentos/fichas')
        return {'subtopicos': len(subs), 'calls': 0}
    if args.check_api and args.embedder != 'embedding-3-large-global':
        raise ValueError('--check-api exige embedding-3-large-global')
    config = {'version': VERSION, 'model': model, 'args': vars(args)}
    identity = {k: v for k, v in vars(args).items() if k not in
                ('workers', 'max_chamadas', 'parar_apos', 'plan', 'check_api', 'output')}
    config['signature'] = sha(json.dumps([VERSION, model, identity], sort_keys=True), 40)
    previous = read_json(out / 'run_config.json')
    if previous and previous.get('signature') != config['signature']:
        raise ValueError('Configuração mudou; escolha uma nova pasta de saída para preservar o experimento')
    corpus_sha = sha(manifest_path.read_text(encoding='utf-8'), 40) if collections is not None else None
    if previous and previous.get('corpus_sha') and corpus_sha and previous['corpus_sha'] != corpus_sha:
        raise ValueError('Os corpora mudaram; use uma nova saída para preservar o experimento')
    config['corpus_sha'] = corpus_sha or (previous or {}).get('corpus_sha')
    config['started_at'] = (previous or {}).get('started_at', datetime.now().isoformat())
    atomic_json(out / 'run_config.json', config)
    needs_gpu = (args.embedder == 'BAAI/bge-m3' or args.reranker not in ('none', '', 'hash')) and (
        STAGES.index(args.parar_apos) >= STAGES.index('selecao'))
    if needs_gpu:
        from pipeline.inventario.modelos import require_gpu, _device
        _device(args.device)
        log(f"[gpu] {require_gpu()}")  # falha aqui, antes de gastar chamadas, se não houver CUDA
    llm = LLMClient(model, None if args.effort == 'none' else args.effort, out / 'cache' / 'llm_cache.sqlite3',
                    out / 'chamadas_llm.jsonl', max_calls=args.max_chamadas, provider=args.llm_provider)
    try:
        if args.check_api:
            from pipeline.inventario.modelos import load_models
            emb, _ = load_models(args.embedder, 'none', output=out)
            try:
                import uuid
                data = llm.json('Responda somente JSON: {"ok":true}',
                                'Teste de conectividade: ' + str(uuid.uuid4()), tag='check_api',
                                max_tokens=4096, validate=check_api_json)
                vectors = emb.impl.encode(['confiabilidade de ativos offshore', 'maintenance backlog'],
                                          usar_cache=False)
                if vectors.shape != (2, 3072):
                    raise ValueError('Dimensão inesperada')
                log(f'[API OK] LLM={model}; embeddings={args.embedder}; shape={vectors.shape}')
                return data
            finally:
                emb.close()
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            return run_stages(args, out, log, t0, llm, pool, subs, timings, manifest_path, collections)
    finally:
        llm.close()


def check_api_json(data):
    if data.get('ok') is not True:
        raise ValueError('Teste JSON inválido')


def run_stages(args, out, log, t0, llm, pool, subs, timings, manifest_path, collections):

    # ------------------------------------------------------------ 1. assuntos
    t = time.time()

    def do_assuntos(sub):
        d = out / 'subtopicos' / sub['dir']
        path = d / 'assuntos.json'
        cached = read_json(path)
        if cached and cached.get('frase_sha') == sha(sub['frase']) and cached.get('version') == A.VERSION:
            return sub, cached['assuntos'], cached['diagnostico']
        items, diag = A.extract_assuntos(llm, sub['topico'], sub['subtopico'], sub['frase'])
        atomic_json(path, {'version': A.VERSION, 'frase_sha': sha(sub['frase']), 'subtopico': sub,
                           'diagnostico': diag, 'assuntos': items})
        return sub, items, diag

    by_sub = {}
    for fut in as_completed([pool.submit(do_assuntos, s) for s in subs]):
        sub, items, diag = fut.result()
        by_sub[sub['key']] = items
        log(f"[assuntos] {sub['subtopico'][:60]}: {diag['n']} assuntos ({diag['genericos']} genéricos, "
            f"{diag['nao_literais']} não literais, cobertura da frase {diag['cobertura_lexical_da_frase']:.0%})")
    all_assuntos = [{**a, 'key': f"{s['key']}::{a['id']}", 'sub_key': s['key']}
                    for s in subs for a in by_sub[s['key']] if not a['generico']]
    timings['assuntos'] = round(time.time() - t, 1)
    log(f"[assuntos] total: {len(all_assuntos)} assuntos pesquisáveis em {len(subs)} subtópicos")
    if args.parar_apos == 'assuntos':
        return finish(out, log, llm, timings, t0, [])

    # ----------------------------------------------------------- 2. varredura
    t = time.time()
    params = {'chunk_words': args.chunk_words, 'stride': args.chunk_stride, 'quota': args.candidatos_por_colecao,
              'limit_units': args.limite_unidades}
    sig = V.signature(all_assuntos, manifest_path, params)
    idx_dir = out / 'indices'
    meta = read_json(idx_dir / 'varredura_meta.json')
    if meta and meta.get('signature') == sig and all((idx_dir / p).exists() for p in ('candidatos.jsonl', 'trechos.jsonl')):
        chunks = {r['chunk_id']: r for r in read_jsonl(idx_dir / 'trechos.jsonl')}
        candidates = defaultdict(list)
        for r in read_jsonl(idx_dir / 'candidatos.jsonl'):
            candidates[r['akey']].append({**chunks[r['chunk_id']], 'lex_score': r['lex_score']})
        log(f"[varredura] reaproveitada: {len(chunks):,} trechos candidatos")
    else:
        log('[varredura] verificando manifesto e hashes dos corpora (pode levar alguns minutos)...')
        log('[varredura] coleções:', ', '.join(f"{c['id']}({c.get('documents')})" for c in collections))
        candidates, stats = V.scan(V.iter_limited_units(collections, args.limite_unidades), all_assuntos,
                                   quota=args.candidatos_por_colecao,
                                   chunk_words=args.chunk_words, stride=args.chunk_stride,
                                   limit_units=args.limite_unidades, log=log)
        chunks = {}
        rows = []
        for akey, lst in candidates.items():
            for c in lst:
                chunks.setdefault(c['chunk_id'], {k: v for k, v in c.items() if k != 'lex_score'})
                rows.append({'akey': akey, 'chunk_id': c['chunk_id'], 'lex_score': c['lex_score']})
        write_jsonl(idx_dir / 'trechos.jsonl', chunks.values())
        write_jsonl(idx_dir / 'candidatos.jsonl', rows)
        atomic_json(idx_dir / 'varredura_meta.json', {'signature': sig, 'version': V.VERSION, 'params': params,
                                                      'stats': stats})
        log(f"[varredura] {stats['janelas']:,} janelas, {stats['ruido']:,} ruído, {stats['candidatos_unicos']:,} "
            f"trechos candidatos em {stats['segundos']:.0f}s | por coleção: {stats['por_colecao']}")
    timings['varredura'] = round(time.time() - t, 1)
    if args.parar_apos == 'varredura':
        return finish(out, log, llm, timings, t0, [])

    # ------------------------------------------------------------- 3. seleção
    t = time.time()
    from pipeline.inventario.modelos import load_models
    log(f"[modelos] carregando {args.embedder} e {args.reranker} (device={args.device})")
    embedder, reranker = load_models(args.embedder, args.reranker, args.device, output=out)
    try:
        return run_selected(args, out, log, t0, llm, pool, subs, timings, sig, idx_dir, candidates,
                            by_sub, embedder, reranker, t)
    finally:
        if hasattr(embedder, 'close'):
            embedder.close()


def run_selected(args, out, log, t0, llm, pool, subs, timings, sig, idx_dir, candidates, by_sub,
                 embedder, reranker, selection_started):
    from pipeline.inventario.modelos import EmbeddingCache
    t = selection_started
    log(f"[modelos] prontos em {getattr(embedder, 'device', 'hash')}")
    emb_cache = EmbeddingCache(idx_dir / 'emb_cache.npz', args.embedder)
    # Vetoriza todos os candidatos de uma vez (lotes grandes aproveitam melhor a GPU).
    all_texts = sorted({c['texto'] for lst in candidates.values() for c in lst})
    tv = time.time()
    emb_cache.encode(embedder, all_texts, batch_size=args.embed_batch)
    emb_cache.save()
    log(f"[seleção] {len(all_texts):,} trechos candidatos vetorizados em {time.time() - tv:.0f}s")
    selections = {}
    for s in subs:
        d = out / 'subtopicos' / s['dir']
        sel_sig = sha(json.dumps([sig, S.VERSION, args.embedder, args.reranker, args.dense_top,
                                  args.trechos_por_assunto, args.min_rerank]), 20)
        cached = read_json(d / 'selecao.json')
        if cached and cached.get('signature') == sel_sig:
            selections[s['key']] = cached['assuntos']
            continue
        res = {}
        for a in by_sub[s['key']]:
            if a['generico']:
                continue
            chosen, info = S.select_for_assunto(a, candidates.get(f"{s['key']}::{a['id']}", []), emb_cache, embedder,
                                                reranker, dense_top=args.dense_top, k=args.trechos_por_assunto,
                                                min_rerank=args.min_rerank, batch=args.embed_batch,
                                                rerank_batch=args.rerank_batch)
            res[a['id']] = {'info': info, 'trechos': chosen}
        atomic_json(d / 'selecao.json', {'signature': sel_sig, 'assuntos': res})
        emb_cache.save()
        selections[s['key']] = res
        n_sel = sum(v['info']['selecionados'] for v in res.values())
        n_zero = sum(v['info']['selecionados'] == 0 for v in res.values())
        log(f"[seleção] {s['subtopico'][:60]}: {n_sel} trechos selecionados; {n_zero} assuntos sem trecho "
            f"(serão gerados sem contexto)")
    emb_cache.save()
    timings['selecao'] = round(time.time() - t, 1)
    if args.parar_apos == 'selecao':
        return finish(out, log, llm, timings, t0, [])

    # ------------------------------------------------------------ 4. extração
    t = time.time()
    jobs = []
    for s in subs:
        uniq = {}
        hits = defaultdict(set)
        for aid, v in selections[s['key']].items():
            for c in v['trechos']:
                uniq.setdefault(c['chunk_id'], c)
                hits[c['chunk_id']].add(aid)
        for cid, c in uniq.items():
            jobs.append((s, c, hits[cid]))
    log(f"[extração] {len(jobs)} trechos únicos -> {len(jobs)} chamadas ao LLM (as já feitas vêm do cache)")
    kept = defaultdict(list)
    dropped = defaultdict(list)
    failures = 0
    failed_jobs = []
    done = 0

    def do_extract(job):
        s, c, h = job
        return s['key'], X.extract_chunk(llm, s, c, by_sub[s['key']], h)

    futures = {pool.submit(do_extract, j): j for j in jobs}
    for fut in as_completed(futures):
        try:
            key, (k, dr) = fut.result()
            kept[key] += k
            dropped[key] += dr
        except Exception as exc:  # noqa: BLE001
            failures += 1
            s, c, _ = futures[fut]
            failed_jobs.append({'sub_key': s['key'], 'chunk_id': c['chunk_id'], 'error': type(exc).__name__})
            log(f"[extração] falha: {type(exc).__name__}; chunk={c['chunk_id']}")
            if type(exc).__name__ in ('AuthenticationError', 'BudgetExceeded', 'PermissionDeniedError',
                                      'NotFoundError', 'BadRequestError'):
                for pending in futures:
                    pending.cancel()
                atomic_json(out / 'falhas_extracao.json', failed_jobs)
                raise
        done += 1
        if done % 50 == 0 or done == len(jobs):
            el = time.time() - t
            log(f"[extração] {done}/{len(jobs)} trechos | unidades aceitas {sum(map(len, kept.values()))} | "
                f"descartadas {sum(map(len, dropped.values()))} | {done / max(el, 1e-6):.2f} trechos/s | "
                f"tokens {llm.usage['prompt_tokens']:,}+{llm.usage['completion_tokens']:,}")
    ext_stats = {}
    for s in subs:
        d = out / 'subtopicos' / s['dir']
        k = sorted(kept[s['key']], key=lambda u: u['uid'])
        dr = sorted(dropped[s['key']], key=lambda u: u['uid'])
        write_jsonl(d / 'unidades_brutas.jsonl', k)
        write_jsonl(d / 'unidades_descartadas.jsonl', dr)
        reasons = defaultdict(int)
        for u in dr:
            for r in u['descartada_por']:
                reasons[r] += 1
        drafts = {kind:sum(u['redacao']['ajuste'] == kind for u in k+dr)
                  for kind in ('nenhum', 'editorial', 'tecnico')}
        ext_stats[s['key']] = {'aceitas': len(k), 'descartadas': len(dr), 'motivos': dict(reasons),
                               'redacao':drafts}
        log(f"[redação] {s['subtopico']}: {drafts} (ajustes propostos; aguardam revisão)")
    atomic_json(out / 'resumo_redacao.json', {key:value['redacao'] for key,value in ext_stats.items()})
    timings['extracao'] = round(time.time() - t, 1)
    log(f"[extração] concluída: {failures} falhas")
    atomic_json(out / 'falhas_extracao.json', failed_jobs)
    if failures:
        raise RuntimeError(f'{failures} extrações falharam. Repita o comando: sucessos estão em cache. '
                           'Falha de API não será classificada como ausência de contexto.')
    if args.parar_apos == 'extracao':
        return finish(out, log, llm, timings, t0, [])

    # -------------------------------------------------------------- revisão
    t = time.time()
    source_chunks = {c['chunk_id']:c for row in selections.values() for v in row.values() for c in v['trechos']}
    review_stats = {}
    for s in subs:
        d = out / 'subtopicos' / s['dir']
        raw_units = kept[s['key']] + dropped[s['key']]
        log(f"[revisão] {s['subtopico']}: {len(raw_units)} unidades; lote={args.review_batch}")
        try:
            reviewed, rejected, pending, verdicts, stats = R.review_units(
                llm,s,raw_units,source_chunks,by_sub[s['key']],batch_size=args.review_batch,pool=pool)
        except Exception as exc:
            atomic_json(out / 'falha_revisao.json', {'sub_key':s['key'],'error':type(exc).__name__})
            raise
        kept[s['key']] = reviewed
        review_stats[s['key']] = stats
        ext_stats[s['key']]['revisao'] = stats
        write_jsonl(d / 'unidades_revisadas.jsonl',reviewed)
        write_jsonl(d / 'unidades_rejeitadas_revisao.jsonl',rejected)
        write_jsonl(d / 'unidades_pendentes.jsonl',pending)
        write_jsonl(d / 'pareceres_revisao.jsonl',verdicts)
        atomic_json(d / 'resumo_revisao.json',stats)
        log(f"[revisão] {s['subtopico']}: {stats}")
    atomic_json(out / 'falha_revisao.json',None)
    atomic_json(out / 'resumo_revisao.json',review_stats)
    timings['revisao'] = round(time.time()-t,1)
    if args.parar_apos == 'revisao':
        return finish(out,log,llm,timings,t0,[])

    # -------------------------------------------------------- 5. consolidação
    t = time.time()
    consolidated = {}
    for s in subs:
        units = kept[s['key']]
        vecs = emb_cache.encode(embedder, [f"{u['afirmacao']} {u['condicoes']}" for u in units],
                                batch_size=args.embed_batch) if units else None
        cons, st = C.consolidate(llm, s['key'], units, vecs, threshold=args.limiar_consolidacao, pool=pool)
        consolidated[s['key']] = cons
        ext_stats[s['key']]['consolidacao'] = st
        log(f"[consolidação] {s['subtopico'][:60]}: {len(units)} unidades -> {len(cons)} consolidadas "
            f"({st.get('equivalentes', 0)} fusões, {st.get('conflito', 0)} conflitos)")
    emb_cache.save()
    timings['consolidacao'] = round(time.time() - t, 1)
    if args.parar_apos == 'consolidacao':
        return finish(out, log, llm, timings, t0, [])

    # -------------------------------------------------------------- 6. fichas
    rows = []
    for s in subs:
        d = out / 'subtopicos' / s['dir']
        rows += F.write_subtopic(d, s, by_sub[s['key']], consolidated[s['key']], selections[s['key']], ext_stats[s['key']])
    F.write_coverage(out, rows)
    F.write_generation_index(out, rows)
    F.write_topic_documents(out, rows)
    return finish(out, log, llm, timings, t0, rows, sum(len(v) for v in consolidated.values()))


def finish(out, log, llm, timings, t0, rows, n_units=None):
    resumo = {'tempo_total_s': round(time.time() - t0, 1), 'tempos_s': timings, 'uso_llm': llm.usage}
    revisions = read_json(out / 'resumo_revisao.json')
    if revisions:
        resumo['revisao'] = revisions
    if rows:
        resumo['assuntos'] = len(rows)
        resumo['status'] = {k: sum(r['status'] == k for r in rows) for k in ('ok', 'contexto_parcial', 'sem_contexto', 'generico')}
        resumo['unidades_consolidadas'] = n_units
        resumo['vinculos_assuntos'] = sum(r['unidades'] for r in rows)
    atomic_json(out / 'resumo.json', resumo)
    log(f"[fim] {json.dumps(resumo, ensure_ascii=False)}")
    return resumo


if __name__ == '__main__':
    main()
