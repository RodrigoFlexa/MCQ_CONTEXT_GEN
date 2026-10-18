"""Constrói o inventário de conhecimento do PetroQuest: notas técnicas por conceito, por assunto.

Fluxo: frases do especialista -> assuntos -> varredura lexical -> seleção bilíngue de trechos ->
fatos com citação -> conceitos por assunto -> nota técnica (redator) + revisão ->
mapa de combinações por subtópico (questões difíceis do tipo B) -> documentos.

Robustez: cada trecho/assunto/conceito é processado de forma independente. Filtro de conteúdo,
resposta inválida ou falha de API de um item vira uma linha em ocorrencias.jsonl e a execução segue.
Só interrompem: credencial/deployment inválidos, orçamento de chamadas e falhas consecutivas em série
(--max-falhas-consecutivas), que indicam problema sistêmico. Repetir o comando retoma do cache.

Exemplo (Linux):
    python3 -u pipeline/inventario/run_inventario.py --topicos 'Produção e Processo' \\
        --output pipeline/inventario/saida_producao_v4_notas
"""
import argparse
import json
import math
import shutil
import sys
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.inventario import VERSION  # noqa: E402
from pipeline.inventario import assuntos as A  # noqa: E402
from pipeline.inventario import combinacoes as M  # noqa: E402
from pipeline.inventario import consolidacao as C  # noqa: E402
from pipeline.inventario import extracao as X  # noqa: E402
from pipeline.inventario import fichas as F  # noqa: E402
from pipeline.inventario import complemento as CP
from pipeline.inventario import notas as N  # noqa: E402
from pipeline.inventario import revisao as R  # noqa: E402
from pipeline.inventario import selecao as S  # noqa: E402
from pipeline.inventario import varredura as V  # noqa: E402
from pipeline.inventario.llm import BudgetExceeded, CallFailed, ContentFiltered, LLMClient, is_fatal, load_dotenv  # noqa: E402
from pipeline.inventario.perfil_modelos import PROFILE, StageLLM, resolve as resolve_models  # noqa: E402
from pipeline.inventario.textutil import (atomic_json, norm, read_json, read_jsonl, sha, slug,  # noqa: E402
                                          write_jsonl)

STAGES = ('assuntos', 'varredura', 'selecao', 'fatos', 'conceitos', 'notas', 'combinacoes', 'documentos')


class SystemicFailure(RuntimeError):
    """Falhas consecutivas demais: serviço indisponível ou erro de configuração."""


class Log:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()

    def __call__(self, *parts):
        line = f"{datetime.now().strftime('%H:%M:%S')} {' '.join(str(p) for p in parts)}"
        with self.lock:
            print(line, flush=True)
            with self.path.open('a', encoding='utf-8') as f:
                f.write(line + '\n')


class Ocorrencias:
    """Registro (desta execução) de itens pulados: filtro de conteúdo, falha de chamada, erro interno."""

    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text('', encoding='utf-8')
        self.lock = threading.Lock()
        self.rows = []

    def add(self, **row):
        row = {'at': datetime.now().isoformat(timespec='seconds'), **row}
        with self.lock:
            self.rows.append(row)
            with self.path.open('a', encoding='utf-8') as f:
                f.write(json.dumps(row, ensure_ascii=False) + '\n')

    def count(self):
        return dict(Counter(r['tipo'] for r in self.rows))


def parse(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--corpus-manifest', default='dataset/domain_corpora/manifest.json')
    p.add_argument('--allow-sample-corpus', action='store_true', help='aceita manifesto de amostra (testes)')
    p.add_argument('--output', default='pipeline/inventario/saida')
    p.add_argument('--topicos', nargs='*', default=[], help='nomes (ou partes) de tópicos; vazio = todos')
    p.add_argument('--subtopicos', nargs='*', default=[], help='nomes (ou partes) de subtópicos; vazio = todos')
    p.add_argument('--limite-assuntos', type=int, default=None, help='PILOTO: só os N primeiros assuntos de cada subtópico')
    p.add_argument('--reaproveitar-de', default=None,
                   help='saída anterior: copia assuntos, índice lexical e cache de embeddings (não copia LLM)')
    p.add_argument('--llm-provider', choices=['azure', 'openai'], default='azure')
    p.add_argument('--llm-model', default=None, help='deployment Azure; padrão gpt-5-4-petrobras')
    p.add_argument('--perfil-modelos', choices=['unico', PROFILE], default='unico',
                   help='unico: --llm-model/--effort; petrobras-nano-low: Nano em assuntos/fatos, GPT-5.4 nas demais')
    p.add_argument('--plan', action='store_true', help='valida parâmetros e corpora, lista o recorte, sem chamadas')
    p.add_argument('--check-api', action='store_true', help='teste real de cada deployment/effort e embeddings, sem corpora')
    p.add_argument('--effort', default=None, choices=['none', 'low', 'medium', 'high'],
                   help='padrão medium no perfil unico; low no perfil petrobras-nano-low')
    p.add_argument('--workers', type=int, default=8, help='chamadas LLM simultâneas')
    p.add_argument('--max-chamadas', type=int, default=30000)
    p.add_argument('--max-falhas-consecutivas', type=int, default=20)
    p.add_argument('--embedder', default='embedding-3-large-global',
                   choices=['embedding-3-large-global', 'BAAI/bge-m3', 'hash'])
    p.add_argument('--reranker', default='none', help='none = cosseno; BAAI/bge-reranker-v2-m3 exige GPU')
    p.add_argument('--device', default='cuda', help='para modelos locais: cuda ou cuda:N; Azure não usa GPU local')
    p.add_argument('--embed-batch', type=int, default=64)
    p.add_argument('--rerank-batch', type=int, default=32)
    p.add_argument('--chunk-words', type=int, default=350)
    p.add_argument('--chunk-stride', type=int, default=250)
    p.add_argument('--candidatos-por-colecao', type=int, default=40)
    p.add_argument('--dense-top', type=int, default=60)
    p.add_argument('--trechos-por-assunto', type=int, default=12)
    p.add_argument('--min-score', type=float, default=None, help='piso de relevância; padrão depende do modo')
    p.add_argument('--rel-score', type=float, default=None, help='corte relativo ao melhor trecho; padrão por modo')
    p.add_argument('--min-por-colecao', type=int, default=2, help='trechos garantidos por coleção elegível')
    p.add_argument('--max-por-documento', type=int, default=3)
    p.add_argument('--limiar-duplicata', type=float, default=0.92, help='similaridade para fundir notas repetidas')
    p.add_argument('--sem-complemento-notas', action='store_true',
                   help='desliga busca complementar limitada aos candidatos já recuperados')
    p.add_argument('--parar-apos', choices=STAGES, default='documentos')
    p.add_argument('--limite-unidades', type=int, default=None, help='TESTE: lê só N páginas/linhas por coleção')
    return p.parse_args(argv)


def validate_args(args):
    for key in ('workers', 'max_chamadas', 'embed_batch', 'rerank_batch', 'chunk_words', 'chunk_stride',
                'candidatos_por_colecao', 'dense_top', 'trechos_por_assunto', 'max_falhas_consecutivas',
                'max_por_documento'):
        if getattr(args, key) < 1:
            raise ValueError(f'{key} deve ser positivo')
    if args.min_por_colecao < 0:
        raise ValueError('min-por-colecao não pode ser negativo')
    if args.chunk_words < 80 or args.chunk_stride > args.chunk_words:
        raise ValueError('Trechos >=80 palavras e stride <= chunk_words')
    for key in ('limite_unidades', 'limite_assuntos'):
        if getattr(args, key) is not None and getattr(args, key) < 1:
            raise ValueError(f'{key} deve ser positivo')
    for key in ('min_score', 'rel_score', 'limiar_duplicata'):
        v = getattr(args, key)
        if v is not None and (not math.isfinite(v) or not 0 <= v <= 1):
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
        return run_main(args)


def reuse_previous(args, out, subs, log):
    """Copia o que não depende do LLM novo: assuntos (para a varredura casar), índice lexical e vetores."""
    src = Path(args.reaproveitar_de)
    if not src.is_absolute():
        src = ROOT / src
    if not src.is_dir():
        raise ValueError(f'--reaproveitar-de não existe: {src}')
    copied = []
    for s in subs:
        a, b = src / 'subtopicos' / s['dir'] / 'assuntos.json', out / 'subtopicos' / s['dir'] / 'assuntos.json'
        if a.exists() and not b.exists():
            b.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(a, b)
            copied.append(b.relative_to(out).as_posix())
    for rel in ('indices/trechos.jsonl', 'indices/candidatos.jsonl', 'indices/varredura_meta.json',
                'indices/emb_cache.npz', 'dominio/embeddings/azure_cache.sqlite3',
                'dominio/embeddings/protocolo_azure.json'):
        a, b = src / rel, out / rel
        if a.exists() and not b.exists():
            b.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(a, b)
            copied.append(rel)
    log(f'[reaproveitamento] {len(copied)} arquivos copiados de {src}')


def run_main(args):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:  # noqa: BLE001
        pass
    load_dotenv(ROOT)
    import os
    model = args.llm_model or ('gpt-5-4-petrobras' if args.llm_provider == 'azure' else
                               os.environ.get('INVENTARIO_LLM_MODEL', 'gpt-6-luna'))
    routes = resolve_models(args, model)
    model_label = model if args.perfil_modelos == 'unico' else 'por etapa'
    out = Path(args.output)
    if not out.is_absolute():
        out = ROOT / out
    out.mkdir(parents=True, exist_ok=True)
    log = Log(out / 'execucao.log')
    t0 = time.time()
    from pipeline.fase_3.topicos import TOPICOS
    subs = select_subtopics(TOPICOS, args.topicos, args.subtopicos)
    if not subs:
        raise SystemExit('Nenhum subtópico corresponde ao filtro informado.')
    log(f"[início] {VERSION} | modelo={model_label} effort={args.effort} workers={args.workers} | "
        f"{len(subs)} subtópicos | saída={out}")
    log(f'[modelos] perfil={args.perfil_modelos}; etapas={json.dumps(routes, ensure_ascii=False)}')
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
        log(f'[plano] {len(subs)} subtópicos; provider={args.llm_provider}; modelo={model_label}; '
            f'embeddings={args.embedder}; reranker={args.reranker}; chamadas=0')
        return {'subtopicos': len(subs), 'calls': 0}
    if args.check_api and args.embedder != 'embedding-3-large-global':
        raise ValueError('--check-api exige embedding-3-large-global')
    config = {'version': VERSION, 'model': model, 'args': vars(args), 'modelos_por_etapa': routes}
    identity = {k: v for k, v in vars(args).items() if k not in
                ('workers', 'max_chamadas', 'parar_apos', 'plan', 'check_api', 'output', 'reaproveitar_de',
                 'max_falhas_consecutivas')}
    if args.perfil_modelos == 'unico':
        identity.pop('perfil_modelos')  # Compatibilidade com saídas anteriores de modelo único.
        signature_data = [VERSION, model, identity]
    else:
        signature_data = [VERSION, model, identity, routes]
    config['signature'] = sha(json.dumps(signature_data, sort_keys=True), 40)
    previous = read_json(out / 'run_config.json')
    if previous and previous.get('signature') != config['signature']:
        raise ValueError('Configuração mudou; escolha uma nova pasta de saída para preservar o experimento')
    corpus_sha = sha(manifest_path.read_text(encoding='utf-8'), 40) if collections is not None else None
    if previous and previous.get('corpus_sha') and corpus_sha and previous['corpus_sha'] != corpus_sha:
        raise ValueError('Os corpora mudaram; use uma nova saída para preservar o experimento')
    config['corpus_sha'] = corpus_sha or (previous or {}).get('corpus_sha')
    config['started_at'] = (previous or {}).get('started_at', datetime.now().isoformat())
    atomic_json(out / 'run_config.json', config)
    if args.reaproveitar_de and not args.check_api:
        reuse_previous(args, out, subs, log)
    needs_gpu = (args.embedder == 'BAAI/bge-m3' or args.reranker not in ('none', '', 'hash')) and (
        STAGES.index(args.parar_apos) >= STAGES.index('selecao'))
    if needs_gpu:
        from pipeline.inventario.modelos import require_gpu, _device
        _device(args.device)
        log(f"[gpu] {require_gpu()}")
    if args.perfil_modelos == 'unico':
        llm = LLMClient(model, None if args.effort == 'none' else args.effort, out / 'cache' / 'llm_cache.sqlite3',
                        out / 'chamadas_llm.jsonl', max_calls=args.max_chamadas, provider=args.llm_provider)
    else:
        llm = StageLLM(routes, out / 'cache' / 'llm_cache.sqlite3', out / 'chamadas_llm.jsonl',
                       max_calls=args.max_chamadas, provider=args.llm_provider, client_factory=LLMClient)
    try:
        if args.check_api:
            return check_api(args, out, log, llm, model)
        occ = Ocorrencias(out / 'ocorrencias.jsonl')
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            try:
                return Pipeline(args, out, log, llm, pool, occ, subs, manifest_path, collections, t0).run()
            except (SystemicFailure, BudgetExceeded) as exc:
                log(f'[interrompido] {type(exc).__name__}: {exc}')
                finish(out, log, llm, occ, {}, t0, status='interrompido', reason=str(exc))
                raise
    finally:
        llm.close()


def check_api(args, out, log, llm, model):
    from pipeline.inventario.modelos import load_models
    emb, _ = load_models(args.embedder, 'none', output=out)
    try:
        import uuid

        def validate(data):
            if data.get('ok') is not True:
                raise ValueError('Teste JSON inválido')
        checks = llm.clients.items() if isinstance(llm, StageLLM) else [((model, args.effort), llm)]
        for (deployment, effort), client in checks:
            data = client.json('Responda somente JSON: {"ok":true}',
                               'Teste de conectividade: ' + str(uuid.uuid4()),
                               tag=f'check_api:{deployment}', max_tokens=4096, validate=validate)
            log(f'[API OK] LLM={deployment}; effort={effort}')
        vectors = emb.impl.encode(['confiabilidade de ativos offshore', 'maintenance backlog'], usar_cache=False)
        if vectors.shape != (2, 3072):
            raise ValueError('Dimensão inesperada')
        log(f'[API OK] embeddings={args.embedder}; shape={vectors.shape}')
        return data
    finally:
        emb.close()


class Pipeline:
    def __init__(self, args, out, log, llm, pool, occ, subs, manifest_path, collections, t0):
        self.args, self.out, self.log, self.llm, self.pool, self.occ = args, out, log, llm, pool, occ
        self.subs, self.manifest_path, self.collections, self.t0 = subs, manifest_path, collections, t0
        self.timings = {}
        self.failed_assuntos = defaultdict(set)   # sub_key -> assuntos com processamento incompleto

    def d(self, sub):
        return self.out / 'subtopicos' / sub['dir']

    # ------------------------------------------------------------------ execução por item
    def run_jobs(self, stage, jobs, fn, describe, progress_every=50):
        """Executa jobs [(chave, payload)] em paralelo. Falhas de item viram ocorrências; só erros
        fatais, orçamento ou falhas consecutivas em série interrompem a etapa."""
        results, consec, done, failed, filtered = {}, 0, 0, 0, 0
        started = time.time()
        futures = {self.pool.submit(fn, payload): (key, payload) for key, payload in jobs}
        try:
            for fut in as_completed(futures):
                key, payload = futures[fut]
                try:
                    results[key] = fut.result()
                    consec = 0
                except ContentFiltered as exc:
                    filtered += 1
                    consec = 0
                    self.occ.add(etapa=stage, item=str(key), tipo='filtro_conteudo', mensagem=str(exc)[:600],
                                 **describe(payload))
                    self.log(f'[{stage}] filtro de conteúdo: {key} (item pulado; execução continua)')
                except BudgetExceeded:
                    raise
                except Exception as exc:  # noqa: BLE001
                    if is_fatal(exc):
                        raise
                    failed += 1
                    consec += 1
                    self.occ.add(etapa=stage, item=str(key), tipo=getattr(exc, 'kind', 'erro_interno'),
                                 mensagem=f'{type(exc).__name__}: {exc}'[:1000], **describe(payload))
                    self.log(f'[{stage}] falha em {key}: {type(exc).__name__}: {str(exc)[:200]}')
                    if consec >= self.args.max_falhas_consecutivas:
                        raise SystemicFailure(f'{consec} falhas consecutivas em {stage}; última: '
                                              f'{type(exc).__name__}: {str(exc)[:300]}') from exc
                done += 1
                if done % progress_every == 0 or done == len(jobs):
                    el = max(time.time() - started, 1e-6)
                    self.log(f'[{stage}] {done}/{len(jobs)} | ok {len(results)} | falhas {failed} | '
                             f'filtrados {filtered} | {done / el:.2f}/s | tokens '
                             f"{self.llm.usage['prompt_tokens']:,}+{self.llm.usage['completion_tokens']:,}")
        except BaseException:
            for f in futures:
                f.cancel()
            raise
        return results

    # ------------------------------------------------------------------ etapas
    def run(self):
        a = self.args
        by_sub = self.stage_assuntos()
        if a.parar_apos == 'assuntos':
            return finish(self.out, self.log, self.llm, self.occ, self.timings, self.t0)
        candidates, sig = self.stage_varredura(by_sub)
        self.candidates = candidates
        if a.parar_apos == 'varredura':
            return finish(self.out, self.log, self.llm, self.occ, self.timings, self.t0)
        from pipeline.inventario.modelos import EmbeddingCache, load_models
        self.log(f"[modelos] carregando {a.embedder} e {a.reranker}")
        embedder, reranker = load_models(a.embedder, a.reranker, a.device, output=self.out)
        try:
            emb_cache = EmbeddingCache(self.out / 'indices' / 'emb_cache.npz', a.embedder)
            selections = self.stage_selecao(by_sub, candidates, sig, embedder, reranker, emb_cache)
            if a.parar_apos == 'selecao':
                return finish(self.out, self.log, self.llm, self.occ, self.timings, self.t0)
            facts, chunks = self.stage_fatos(by_sub, selections)
            if a.parar_apos == 'fatos':
                return finish(self.out, self.log, self.llm, self.occ, self.timings, self.t0)
            plans = self.stage_conceitos(by_sub, facts)
            if a.parar_apos == 'conceitos':
                return finish(self.out, self.log, self.llm, self.occ, self.timings, self.t0)
            notes = self.stage_notas(by_sub, facts, chunks, plans, embedder, emb_cache)
            emb_cache.save()
            if a.parar_apos == 'notas':
                return finish(self.out, self.log, self.llm, self.occ, self.timings, self.t0)
            combos = self.stage_combinacoes(by_sub, notes)
            if a.parar_apos == 'combinacoes':
                return finish(self.out, self.log, self.llm, self.occ, self.timings, self.t0)
            rows = self.stage_documentos(by_sub, selections, facts, plans, notes, combos)
            return finish(self.out, self.log, self.llm, self.occ, self.timings, self.t0, rows=rows, notes=notes)
        finally:
            if hasattr(embedder, 'close'):
                embedder.close()

    def stage_assuntos(self):
        t = time.time()

        def do(sub):
            path = self.d(sub) / 'assuntos.json'
            cached = read_json(path)
            if cached and cached.get('frase_sha') == sha(sub['frase']) and cached.get('version') == A.VERSION:
                return cached['assuntos'], cached['diagnostico']
            items, diag = A.extract_assuntos(self.llm, sub['topico'], sub['subtopico'], sub['frase'])
            atomic_json(path, {'version': A.VERSION, 'frase_sha': sha(sub['frase']), 'subtopico': sub,
                               'diagnostico': diag, 'assuntos': items})
            return items, diag
        res = self.run_jobs('assuntos', [(s['key'], s) for s in self.subs], do, lambda s: {'sub_key': s['key']})
        by_sub = {}
        for s in self.subs:
            if s['key'] not in res:
                self.log(f"[assuntos] {s['subtopico']}: sem assuntos nesta execução (ver ocorrencias.jsonl)")
                continue
            items, diag = res[s['key']]
            if self.args.limite_assuntos:
                searchable = [x for x in items if not x['generico']][:self.args.limite_assuntos]
                items = searchable
            by_sub[s['key']] = items
            self.log(f"[assuntos] {s['subtopico'][:60]}: {diag['n']} assuntos ({diag['genericos']} genéricos; "
                     f"cobertura da frase {diag['cobertura_lexical_da_frase']:.0%})"
                     + (f"; piloto com {len(items)}" if self.args.limite_assuntos else ''))
        self.timings['assuntos'] = round(time.time() - t, 1)
        return by_sub

    def stage_varredura(self, by_sub):
        t = time.time()
        a = self.args
        all_assuntos = [{**x, 'key': f"{s['key']}::{x['id']}", 'sub_key': s['key']}
                        for s in self.subs if s['key'] in by_sub for x in by_sub[s['key']] if not x['generico']]
        params = {'chunk_words': a.chunk_words, 'stride': a.chunk_stride, 'quota': a.candidatos_por_colecao,
                  'limit_units': a.limite_unidades}
        sig = V.signature(all_assuntos, self.manifest_path, params)
        idx = self.out / 'indices'
        meta = read_json(idx / 'varredura_meta.json')
        candidates = defaultdict(list)
        if meta and meta.get('signature') == sig and all((idx / p).exists() for p in ('candidatos.jsonl', 'trechos.jsonl')):
            chunks = {r['chunk_id']: r for r in read_jsonl(idx / 'trechos.jsonl')}
            for r in read_jsonl(idx / 'candidatos.jsonl'):
                candidates[r['akey']].append({**chunks[r['chunk_id']], 'lex_score': r['lex_score']})
            self.log(f"[varredura] reaproveitada: {len(chunks):,} trechos candidatos")
        else:
            if meta:
                self.log('[varredura] índice existente não corresponde aos assuntos/parâmetros atuais; refazendo')
            self.log('[varredura] coleções: ' + ', '.join(f"{c['id']}({c.get('documents')})" for c in self.collections))
            found, stats = V.scan(V.iter_limited_units(self.collections, a.limite_unidades), all_assuntos,
                                  quota=a.candidatos_por_colecao, chunk_words=a.chunk_words, stride=a.chunk_stride,
                                  limit_units=a.limite_unidades, log=self.log)
            chunks, rows = {}, []
            for akey, lst in found.items():
                for c in lst:
                    chunks.setdefault(c['chunk_id'], {k: v for k, v in c.items() if k != 'lex_score'})
                    rows.append({'akey': akey, 'chunk_id': c['chunk_id'], 'lex_score': c['lex_score']})
                    candidates[akey].append(c)
            write_jsonl(idx / 'trechos.jsonl', chunks.values())
            write_jsonl(idx / 'candidatos.jsonl', rows)
            atomic_json(idx / 'varredura_meta.json', {'signature': sig, 'version': V.VERSION, 'params': params,
                                                      'stats': stats})
            self.log(f"[varredura] {stats['janelas']:,} janelas, {stats['ruido']:,} ruído, "
                     f"{stats['candidatos_unicos']:,} candidatos em {stats['segundos']:.0f}s | {stats['por_colecao']}")
        self.timings['varredura'] = round(time.time() - t, 1)
        return candidates, sig

    def stage_selecao(self, by_sub, candidates, sig, embedder, reranker, emb_cache):
        t = time.time()
        a = self.args
        texts = sorted({c['texto'] for lst in candidates.values() for c in lst})
        tv = time.time()
        emb_cache.encode(embedder, texts, batch_size=a.embed_batch)
        emb_cache.save()
        self.log(f"[seleção] {len(texts):,} trechos candidatos vetorizados em {time.time() - tv:.0f}s")
        params = [sig, S.VERSION, a.embedder, a.reranker, a.dense_top, a.trechos_por_assunto, a.min_score,
                  a.rel_score, a.min_por_colecao, a.max_por_documento]
        sel_sig = sha(json.dumps(params), 20)
        selections, total = {}, Counter()
        for s in self.subs:
            if s['key'] not in by_sub:
                continue
            path = self.d(s) / 'selecao.json'
            cached = read_json(path)
            if cached and cached.get('signature') == sel_sig:
                res = cached['assuntos']
            else:
                res = {}
                for x in by_sub[s['key']]:
                    if x['generico']:
                        continue
                    chosen, info = S.select_for_assunto(
                        x, candidates.get(f"{s['key']}::{x['id']}", []), emb_cache, embedder, reranker,
                        dense_top=a.dense_top, k=a.trechos_por_assunto, min_score=a.min_score, rel_score=a.rel_score,
                        min_por_colecao=a.min_por_colecao, max_por_documento=a.max_por_documento,
                        batch=a.embed_batch, rerank_batch=a.rerank_batch)
                    res[x['id']] = {'info': info, 'trechos': chosen}
                atomic_json(path, {'signature': sel_sig, 'version': S.VERSION, 'assuntos': res})
                emb_cache.save()
            selections[s['key']] = res
            per = Counter()
            for v in res.values():
                per.update(v['info'].get('colecoes') or {})
            total.update(per)
            self.log(f"[seleção] {s['subtopico'][:60]}: {sum(per.values())} trechos | {dict(per)} | "
                     f"{sum(v['info']['selecionados'] == 0 for v in res.values())} assuntos sem trecho")
        self.log(f'[seleção] total por coleção: {dict(total)}')
        self.timings['selecao'] = round(time.time() - t, 1)
        return selections

    def stage_fatos(self, by_sub, selections):
        t = time.time()
        jobs, chunks = [], {}
        for s in self.subs:
            if s['key'] not in selections:
                continue
            hits = defaultdict(set)
            for aid, v in selections[s['key']].items():
                for c in v['trechos']:
                    chunks[c['chunk_id']] = c
                    hits[c['chunk_id']].add(aid)
            for cid in sorted(hits):
                jobs.append(((s['key'], cid), (s, chunks[cid], hits[cid])))
        self.log(f'[fatos] {len(jobs)} trechos (respostas já obtidas vêm do cache)')
        res = self.run_jobs('fatos', jobs, lambda p: X.extract_chunk(self.llm, p[0], p[1], by_sub[p[0]['key']], p[2]),
                            lambda p: {'sub_key': p[0]['key'], 'assuntos': sorted(p[2]), 'chunk_id': p[1]['chunk_id']})
        kept_by, dropped_by = defaultdict(list), defaultdict(list)
        for key, (s, c, h) in jobs:
            if key in res:
                kept, dropped = res[key]
                kept_by[s['key']] += kept
                dropped_by[s['key']] += dropped
            else:
                self.failed_assuntos[s['key']].update(h)
        for s in self.subs:
            if s['key'] not in selections:
                continue
            kept = sorted(kept_by[s['key']], key=lambda f: f['fid'])
            dropped = sorted(dropped_by[s['key']], key=lambda f: f['fid'])
            write_jsonl(self.d(s) / 'fatos.jsonl', kept)
            write_jsonl(self.d(s) / 'fatos_descartados.jsonl', dropped)
            reasons = Counter(r for f in dropped for r in f['descartado_por'])
            self.log(f"[fatos] {s['subtopico'][:60]}: {len(kept)} aceitos, {len(dropped)} descartados {dict(reasons)} | "
                     f"coleções {dict(Counter(f['fonte']['collection'] for f in kept))}")
        self.timings['fatos'] = round(time.time() - t, 1)
        return dict(kept_by), chunks

    def stage_conceitos(self, by_sub, facts):
        t = time.time()
        jobs = []
        for s in self.subs:
            if s['key'] not in by_sub:
                continue
            for x in by_sub[s['key']]:
                if not x['generico']:
                    mine = [f for f in facts.get(s['key'], []) if x['id'] in f['assuntos']]
                    jobs.append(((s['key'], x['id']), (s, x, mine)))
        res = self.run_jobs('conceitos', jobs, lambda p: C.plan_assunto(self.llm, p[0], p[1], p[2]),
                            lambda p: {'sub_key': p[0]['key'], 'assunto': p[1]['id']}, progress_every=25)
        plans = defaultdict(dict)
        for (sk, aid), _ in jobs:
            if (sk, aid) in res:
                plans[sk][aid] = res[(sk, aid)]
            else:
                self.failed_assuntos[sk].add(aid)
        for s in self.subs:
            if s['key'] in by_sub:
                atomic_json(self.d(s) / 'conceitos.json', plans.get(s['key'], {}))
                p = plans.get(s['key'], {})
                self.log(f"[conceitos] {s['subtopico'][:60]}: {sum(len(v['conceitos']) for v in p.values())} conceitos; "
                         f"{sum(len(v['descartados']) for v in p.values())} fatos descartados por pertinência")
        self.timings['conceitos'] = round(time.time() - t, 1)
        return plans

    def stage_notas(self, by_sub, facts, chunks, plans, embedder, emb_cache):
        t = time.time()
        jobs = []
        # A mesma janela pode gerar F0 diferentes para subtópicos distintos.
        # Cada plano deve consultar a extração do seu próprio subtópico.
        facts_by_sub = {sk: {f['fid']: f for f in lst} for sk, lst in facts.items()}
        assunto_by = {(s['key'], x['id']): x for s in self.subs if s['key'] in by_sub for x in by_sub[s['key']]}
        for s in self.subs:
            for aid, plan in plans.get(s['key'], {}).items():
                for k in plan['conceitos']:
                    jobs.append((k['kid'], (s, assunto_by[(s['key'], aid)], k)))

        def do(p):
            s, x, k = p
            facts_by_fid = facts_by_sub.get(s['key'], {})
            draft = N.write_note(self.llm, s, x, k, facts_by_fid, chunks)
            if not getattr(self.args, 'sem_complemento_notas', False):
                pool = {c['chunk_id']: c for akey, cs in getattr(self, 'candidates', {}).items()
                        if akey.startswith(s['key'] + '::') for c in cs}
                used = [v[len('trecho:'):] for v in draft['idmap'].values() if v.startswith('trecho:')]
                extra = CP.retrieve(draft['nota'].get('buscas_complementares', []), pool.values(), used)
                if extra:
                    try:
                        draft = N.enrich_note(self.llm, draft, extra, k['kid'])
                    except (ContentFiltered, CallFailed) as exc:
                        self.occ.add(etapa='complemento', item=k['kid'], tipo=getattr(exc, 'kind', 'filtro_conteudo'),
                                     mensagem=str(exc)[:600], sub_key=s['key'])
                local_chunks = {**chunks, **{c['chunk_id']: c for c in extra}}
            else:
                local_chunks = chunks
            if draft['insuficiente']:
                return note_record(s, x, k, draft, None, facts_by_fid, local_chunks)
            return note_record(s, x, k, draft, R.review_note(self.llm, draft, k['kid']), facts_by_fid, local_chunks)
        res = self.run_jobs('notas', jobs, do, lambda p: {'sub_key': p[0]['key'], 'assunto': p[1]['id']},
                            progress_every=20)
        notes = defaultdict(list)
        failed_kinds = {r['item']: r['tipo'] for r in self.occ.rows if r['etapa'] == 'notas'}
        for kid, (s, x, k) in jobs:
            if kid in res:
                notes[s['key']].append(res[kid])
            else:
                status = 'filtrada' if failed_kinds.get(kid) == 'filtro_conteudo' else 'falhou'
                notes[s['key']].append({'nid': kid, 'status': status, 'sub_key': s['key'], 'assuntos': [x['id']],
                                        'conceito': k, 'metricas': {'palavras': 0, 'alvos': {}}})
                self.failed_assuntos[s['key']].add(x['id'])
        for s in self.subs:
            mine = notes.get(s['key'], [])
            approved = [n for n in mine if n['status'] == 'aprovada']
            if len(approved) > 1:
                vecs = emb_cache.encode(embedder, [n['titulo'] + '. ' + n['resumo'] for n in approved],
                                        batch_size=self.args.embed_batch)
                kept, dup = N.dedupe(approved, vecs, self.args.limiar_duplicata)
                notes[s['key']] = kept + dup + [n for n in mine if n['status'] != 'aprovada']
            c = Counter(n['status'] for n in notes.get(s['key'], []))
            if s['key'] in by_sub:
                self.log(f"[notas] {s['subtopico'][:60]}: {dict(c)}")
        self.timings['notas'] = round(time.time() - t, 1)
        return notes

    def stage_combinacoes(self, by_sub, notes):
        t = time.time()
        jobs = [(s['key'], s) for s in self.subs if s['key'] in by_sub]
        res = self.run_jobs('combinacoes', jobs, lambda s: M.plan_subtopic(self.llm, s, notes.get(s['key'], [])),
                            lambda s: {'sub_key': s['key']}, progress_every=5)
        combos, every = {}, []
        for s in self.subs:
            if s['key'] not in by_sub:
                continue
            plan = res.get(s['key']) or {'version': M.VERSION, 'modo': 'falhou', 'combinacoes': [], 'descartadas': []}
            combos[s['key']] = plan
            every += plan['combinacoes']
            atomic_json(self.d(s) / 'combinacoes.json', plan)
            self.log(f"[combinacoes] {s['subtopico'][:60]}: {len(plan['combinacoes'])} combinações "
                     f"({sum(c['multi_assunto'] for c in plan['combinacoes'])} entre assuntos) | modo {plan['modo']}")
        write_jsonl(self.out / 'combinacoes.jsonl', every)
        self.timings['combinacoes'] = round(time.time() - t, 1)
        return combos

    def stage_documentos(self, by_sub, selections, facts, plans, notes, combos):
        rows, approved = [], []
        for s in self.subs:
            if s['key'] not in by_sub:
                continue
            rows += F.write_subtopic(self.d(s), s, by_sub[s['key']], selections.get(s['key'], {}),
                                     facts.get(s['key'], []), plans.get(s['key'], {}), notes.get(s['key'], []),
                                     self.failed_assuntos.get(s['key'], set()),
                                     (combos.get(s['key']) or {}).get('combinacoes', []))
            approved += [n for n in notes.get(s['key'], []) if n['status'] == 'aprovada']
        write_jsonl(self.out / 'notas_aprovadas.jsonl', approved)
        F.write_coverage(self.out, rows)
        F.write_generation_index(self.out, rows)
        F.write_topic_documents(self.out, [s for s in self.subs if s['key'] in by_sub])
        return rows


def note_record(sub, assunto, conceito, draft, review, facts_by_fid, chunks):
    """Registro completo de uma nota: versão final, rascunho, revisão e fontes citadas."""
    final = review['nota'] if review else draft['nota']
    used = {f for s in final['secoes'] for f in s['fatos']}
    used.update(f for r in final.get('relacoes', []) for f in r['fatos'])
    fontes = {}
    for ref in sorted(used):
        if ref.startswith('trecho:'):
            c = chunks.get(ref[len('trecho:'):], {})
            fontes[ref] = {'tipo': 'trecho', 'texto': c.get('texto', ''), **{k: c.get(k) for k in ('chunk_id', 'collection', 'document_id', 'title',
                                                                      'url', 'jurisdiction', 'page_ini', 'page_fim')}}
        elif ref in facts_by_fid:
            f = facts_by_fid[ref]
            fontes[ref] = {'tipo': 'fato', 'afirmacao': f['afirmacao'], 'condicoes': f['condicoes'],
                           'citacao': f['citacao'], **f['fonte']}
    status = 'insuficiente' if review is None else review['status']
    return {'nid': conceito['kid'], 'status': status, 'topico': sub['topico'], 'subtopico': sub['subtopico'],
            'sub_key': sub['key'], 'assuntos': [assunto['id']], 'assunto_texto': assunto['texto'], 'conceito': conceito,
            **{k: final[k] for k in ('titulo', 'resumo', 'secoes', 'alvos', 'correcoes', 'lacunas')},
            **{k: final[k] for k in ('schema_conhecimento', 'relacoes', 'alvos_bloqueados',
                                      'buscas_complementares') if k in final},
            'complemento': draft.get('complemento', []),
            'antes_complemento': draft.get('antes_complemento'),
            'metricas': review['metricas'] if review else draft['metricas'],
            'avaliacao': (review or {}).get('revisao', {}).get('avaliacao'),
            'revisao': (review or {}).get('revisao'),
            'motivos_reprovacao': (review or {}).get('motivos_reprovacao') or ([draft['insuficiente']] if not review else []),
            'alertas': (review or {}).get('alertas_finais', draft['alertas']),
            'rascunho': draft['nota'], 'alertas_rascunho': draft['alertas'],
            'fontes': fontes, 'colecoes': sorted({v.get('collection') for v in fontes.values() if v.get('collection')}),
            'versoes': {'notas': N.VERSION, 'revisao': R.VERSION}}


def finish(out, log, llm, occ, timings, t0, rows=None, notes=None, status=None, reason=None):
    oc = occ.count() if occ else {}
    resumo = {'versao': VERSION, 'status': status or ('concluido_com_ocorrencias' if oc else 'concluido'),
              'tempo_total_s': round(time.time() - t0, 1), 'tempos_s': timings, 'uso_llm': llm.usage,
              'ocorrencias': oc}
    resumo['uso_llm_por_etapa'] = getattr(llm, 'usage_by_stage', {})
    if isinstance(llm, StageLLM):
        resumo['modelos_por_etapa'] = llm.routes
        resumo['tentativas_llm'] = llm.budget.used
    else:
        resumo['tentativas_llm'] = getattr(llm, 'calls', 0)
    if reason:
        resumo['motivo'] = reason
    if rows:
        resumo['assuntos'] = dict(Counter(r['status'] for r in rows))
        resumo['notas'] = dict(Counter(n['status'] for lst in (notes or {}).values() for n in lst))
        resumo['palavras_aprovadas'] = sum(r['palavras'] for r in rows)
        all_notes = [n for group in (notes or {}).values() for n in group]
        relations = [r for n in all_notes for r in n.get('relacoes', [])]
        resumo['conhecimento'] = {
            'relacoes_por_origem': dict(Counter(r['origem'] for r in relations)),
            'relacoes_avaliaveis': sum(r['avaliavel'] for r in relations),
            'alvos_avaliaveis': sum(len(n.get('alvos', [])) for n in all_notes if n['status'] == 'aprovada'),
            'alvos_bloqueados': sum(len(n.get('alvos_bloqueados', [])) for n in all_notes),
            'notas_com_complemento': sum(bool(n.get('complemento')) for n in all_notes)}
    atomic_json(out / 'resumo.json', resumo)
    log(f"[fim] {json.dumps(resumo, ensure_ascii=False)}")
    if oc:
        log('[fim] há itens pulados (ver ocorrencias.jsonl). Repita o mesmo comando para reprocessá-los; '
            'o que já foi obtido vem do cache.')
    return resumo


if __name__ == '__main__':
    try:
        main()
    except SystemicFailure:
        sys.exit(3)
    except BudgetExceeded:
        sys.exit(4)
