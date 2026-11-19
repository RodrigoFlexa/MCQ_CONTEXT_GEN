"""Construção paralela do índice BM25 dos corpora, compatível com `CorpusIndex`.

Produz exatamente o mesmo banco que `CorpusIndex(dir, manifest).build()` (mesmo
fingerprint, mesmas linhas, mesma ordem e mesma busca), mas:
- prepara os trechos em vários processos (documentos de um JSONL grande são divididos
  em faixas que respeitam a fronteira de documento; cada TXT do Petrolês é uma tarefa);
- grava em um único escritor com cache grande e sem journal, cria os índices
  secundários e o FTS5 depois da carga (em vez de inserir linha a linha);
- mostra progresso e tempo restante.

Depois de construído, `CorpusIndex(...).build()` reconhece o fingerprint e só reaproveita.

Antes de construir, procura um índice já pronto de fluxos anteriores (por padrão em
`pipeline/qa_research/.local/index`) feito dos mesmos arquivos de dados, na mesma ordem e
com os mesmos parâmetros de janela. O conteúdo é idêntico; muda só o fingerprint (a fórmula
ganhou a chave "complete" em 31/10/2026, e o manifesto pode ter sido regravado). O banco é
movido (mesmo disco, instantâneo), recebe o fingerprint novo e não é reconstruído.

Uso, na raiz do repositório (no servidor, onde estão os corpora):

    python -m pipeline.qa_research.refino.indexar --manifest auto --workers 8
"""
import argparse
import contextlib
import gzip
import multiprocessing
import json
import os
import pickle
import re
import sqlite3
import tempfile
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeout
from pathlib import Path

from pipeline.domain_corpora.io_utils import file_hash
from pipeline.qa_research import corpus as K

SCHEMA_TABLES = """
CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE chunks(id INTEGER PRIMARY KEY, digest TEXT UNIQUE, body TEXT, payload TEXT);
CREATE TABLE sources(chunk INTEGER, uid TEXT UNIQUE, original_id TEXT, doc TEXT,
                     pos INTEGER, known INTEGER, payload TEXT);
CREATE VIRTUAL TABLE search USING fts5(body,content='chunks',content_rowid='id',
                                       tokenize='unicode61 remove_diacritics 2');
"""
# Mesmos índices do CorpusIndex; criados depois da carga (ordenação em bloco).
SCHEMA_INDEXES = """
CREATE INDEX original_ids ON sources(original_id);
CREATE INDEX positions ON sources(doc,pos);
CREATE INDEX source_chunks ON sources(chunk);
"""
DOC_ID = re.compile(rb'"document_id":\s*"((?:[^"\\]|\\.)*)"')
BATCH = 2000
# Onde os fluxos anteriores guardam o CorpusIndex (config.index_dir do qa_research).
LEGACY = ('pipeline/qa_research/.local/index',)
TABLES = {'metadata', 'chunks', 'sources', 'search', 'original_ids', 'positions', 'source_chunks'}


def make_pool(workers):
    # spawn: o refino cria o pool a partir de uma thread do asyncio; fork ali é arriscado.
    return ProcessPoolExecutor(max_workers=workers, mp_context=multiprocessing.get_context('spawn'))


def ram_mb():
    try:
        return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') // (1024 * 1024)
    except (ValueError, OSError, AttributeError):
        return 8192


def free_mb():
    """Memória disponível (Linux); None em outros sistemas."""
    try:
        for line in Path('/proc/meminfo').read_text().splitlines():
            if line.startswith('MemAvailable:'):
                return int(line.split()[1]) // 1024
    except OSError:
        pass
    return None


def default_workers():
    # Um processo a menos que os núcleos e no máximo um processo a cada 4 GB de RAM.
    return max(1, min(16, (os.cpu_count() or 2) - 1, ram_mb() // 4096))


def default_cache_mb():
    return int(max(256, min(2048, ram_mb() // 8)))


# ---------------------------------------------------------------- planejamento

def snapshot(manifest, directory, workers):
    """Fingerprint e arquivos idênticos aos de CorpusIndex.build (com hash paralelo)."""
    from pipeline.domain_corpora.manifest import load_manifest
    manifest = Path(manifest).resolve()
    data, collections = load_manifest(manifest, verify=False)
    expected = []
    for c in collections:
        expected += ([(c['resolved_path'], c['sha256'])] if c['format'] == 'pages_jsonl'
                     else [(f['resolved_path'], f['sha256']) for f in c['files']])
    with ThreadPoolExecutor(max_workers=max(1, min(8, workers))) as pool:
        for (path, digest), actual in zip(expected, pool.map(lambda p: file_hash(p[0]), expected)):
            if actual != digest:
                raise ValueError('Corpus modificado ou corrompido: ' + str(path))
    files = [{'path': str(manifest), 'sha256': K._file_hash(manifest)}]
    for c in collections:
        if c['format'] == 'pages_jsonl':
            files.append({'path': str(c['resolved_path']), 'sha256': c['sha256']})
        else:
            files.extend({'path': str(i['resolved_path']), 'sha256': i['sha256']} for i in c['files'])
    complete = not (data.get('sample', False) or data.get('partial', False))
    fingerprint = K._digest(K._json({'version': K._VERSION, 'files': files, 'complete': complete,
                                     'chunk_words': K._CHUNK_WORDS, 'stride': K._STRIDE}))
    folder = Path(directory).resolve() / fingerprint
    return dict(manifest=manifest, collections=collections, files=files, complete=complete,
                fingerprint=fingerprint, folder=folder)


def ready(snap):
    """Mesmo critério de reaproveitamento do CorpusIndex."""
    info_path, db_path = snap['folder'] / 'indice.json', snap['folder'] / 'corpus.sqlite3'
    try:
        info = json.loads(info_path.read_text(encoding='utf-8'))
        if info.get('fingerprint') == snap['fingerprint'] and db_path.is_file():
            import contextlib
            with contextlib.closing(sqlite3.connect(db_path)) as db:
                stored = db.execute("SELECT value FROM metadata WHERE key='fingerprint'").fetchone()
            if stored and stored[0] == snap['fingerprint']:
                return info
    except (FileNotFoundError, json.JSONDecodeError, sqlite3.DatabaseError):
        pass
    return None


def legacy_roots():
    from pipeline.qa_research.v3.runtime import ROOT
    return [ROOT / r for r in LEGACY]


def _same_params(info, name):
    """O nome da pasta prova versão, arquivos e janela (fórmula antiga ou atual)."""
    base = dict(version=K._VERSION, files=info.get('sources'), chunk_words=K._CHUNK_WORDS, stride=K._STRIDE)
    options = {K._digest(K._json(base))}
    options |= {K._digest(K._json(dict(base, complete=c))) for c in (True, False)}
    return name in options


def find_compatible(snap, roots):
    """Índices prontos com os mesmos arquivos de dados, na mesma ordem: (pasta, info, problemas)."""
    found, examined = [], 0
    for root in roots:
        root = Path(root).resolve()
        if not root.is_dir():
            continue
        for old in sorted(p for p in root.iterdir() if p.is_dir() and p != snap['folder']):
            try:
                info = json.loads((old / 'indice.json').read_text(encoding='utf-8'))
            except (OSError, ValueError):
                continue
            examined += 1
            sources = info.get('sources') or []
            if len(sources) != len(snap['files']) or sources[1:] != snap['files'][1:]:
                continue  # outro corpus (o primeiro item é o próprio manifesto)
            problems = []
            if info.get('version') != K._VERSION or info.get('fingerprint') != old.name or not _same_params(info, old.name):
                problems.append('versão ou parâmetros diferentes')
            db_path = old / 'corpus.sqlite3'
            if not db_path.is_file():
                problems.append('banco ausente')
            else:
                try:
                    with contextlib.closing(sqlite3.connect(db_path.as_uri() + '?mode=ro', uri=True)) as db:
                        stored = db.execute("SELECT value FROM metadata WHERE key='fingerprint'").fetchone()
                        tables = {r[0] for r in db.execute('SELECT name FROM sqlite_master')}
                    if not stored or stored[0] != old.name:
                        problems.append('fingerprint do banco não confere')
                    if not TABLES <= tables:
                        problems.append('esquema incompleto')
                except sqlite3.DatabaseError as exc:
                    problems.append('banco ilegível: ' + str(exc))
                if db_path.stat().st_dev != snap['folder'].stat().st_dev:
                    problems.append('está em outro disco (mover copiaria o banco inteiro)')
            found.append((old, info, problems))
    return found, examined


def adopt(snap, roots, progress=print):
    """Move para cá um índice idêntico já construído. Retorna (info, caminho) ou None."""
    name = snap['folder'].parent.name
    found, examined = find_compatible(snap, roots)
    if examined and not found:
        progress(f'[índice:{name}] {examined} índice(s) pronto(s) de outros fluxos examinado(s); '
                 'nenhum feito destes mesmos arquivos', flush=True)
    for old, info, problems in found:
        if problems:
            progress(f'[índice:{name}] índice anterior em {old} não reaproveitado: {"; ".join(problems)}', flush=True)
            continue
        target = snap['folder'] / 'corpus.sqlite3'
        os.replace(old / 'corpus.sqlite3', target)
        with contextlib.closing(sqlite3.connect(target)) as db:
            db.execute("UPDATE metadata SET value=? WHERE key='fingerprint'", (snap['fingerprint'],))
            db.commit()
        new = dict(info, fingerprint=snap['fingerprint'], signature=snap['fingerprint'],
                   complete_corpus=snap['complete'], corpus_bruto_completo=snap['complete'],
                   sources=snap['files'], index_path=str(target),
                   warnings=([] if snap['complete'] else [
                       'Cobertura parcial dos materiais originais disponíveis; ausência de resultados não demonstra ausência no corpus completo.']),
                   adotado=dict(de=str(old), fingerprint_anterior=old.name,
                                manifesto_anterior_sha256=info['sources'][0].get('sha256'),
                                em=time.strftime('%Y-%m-%d %H:%M:%S')))
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', prefix='indice-', suffix='.json',
                                         dir=snap['folder'], delete=False) as stream:
            stream.write(json.dumps(new, ensure_ascii=False, indent=2) + '\n')
            temporary = Path(stream.name)
        temporary.replace(snap['folder'] / 'indice.json')
        (old / 'indice.json').unlink(missing_ok=True)
        (old / 'MOVIDO.txt').write_text(f'Banco movido em {new["adotado"]["em"]} para {target}\n', encoding='utf-8')
        progress(f'[índice:{name}] reaproveitado o índice já construído em {old} '
                 f'({info.get("chunks", 0):,} trechos); movido para cá, sem reconstruir', flush=True)
        return new, target
    return None


def plan(snap, target_bytes):
    """Tarefas na ordem sequencial do CorpusIndex. JSONL grande vira faixas por documento."""
    tasks = []
    for ci, c in enumerate(snap['collections']):
        if c['format'] == 'petroles_txt':
            for fi, f in enumerate(c['files']):
                tasks.append(dict(kind='txt', collection=ci, file=fi, size=Path(f['resolved_path']).stat().st_size))
            continue
        path, size = Path(c['resolved_path']), Path(c['resolved_path']).stat().st_size
        if size <= target_bytes:
            tasks.append(dict(kind='jsonl', collection=ci, start=0, end=size, size=size))
            continue
        start, offset, last = 0, 0, None
        with path.open('rb') as stream:
            for line in stream:
                match = DOC_ID.search(line)
                doc = match[1] if match else json.loads(line).get('document_id', '').encode()
                if last is not None and doc != last and offset - start >= target_bytes:
                    tasks.append(dict(kind='jsonl', collection=ci, start=start, end=offset, size=offset - start))
                    start = offset
                last = doc
                offset += len(line)
        tasks.append(dict(kind='jsonl', collection=ci, start=start, end=offset, size=offset - start))
    return tasks


# ---------------------------------------------------------------- preparação (processos)

def _range_units(collection, start, end):
    with Path(collection['resolved_path']).open('rb') as stream:
        stream.seek(start)
        position = start
        while position < end:
            line = stream.readline()
            if not line:
                break
            position += len(line)
            row = json.loads(line)
            if row.get('collection') != collection['id']:
                raise ValueError('Proveniência não confere com o manifesto')
            yield row


def _chunks(task, collection):
    """Gera os trechos sem acumular a faixa inteira em memória."""
    if task['kind'] == 'txt':
        # Cada TXT é um documento próprio do Petrolês: a janela recomeça em cada arquivo.
        yield from K._manifest_chunks([dict(collection, files=[collection['files'][task['file']]])])
        return
    import pipeline.domain_corpora.manifest as M
    original = M.iter_units
    M.iter_units = lambda cols: _range_units(cols[0], task['start'], task['end'])
    try:
        yield from K._manifest_chunks([collection])
    finally:
        M.iter_units = original


def prepare(task, collection, workdir):
    """Mesmas transformações do laço de CorpusIndex.build, gravadas em arquivo temporário."""
    fd, name = tempfile.mkstemp(prefix='prep-', suffix='.pkl.gz', dir=workdir)
    os.close(fd)
    produced, invalid, batch = 0, 0, []
    with gzip.open(name, 'wb', compresslevel=1) as out:
        for chunk in _chunks(task, collection):
            body = chunk.get('texto', chunk.get('text', ''))
            original_id = chunk.get('chunk_id')
            if not isinstance(body, str) or not body.strip() or not isinstance(original_id, str) or not original_id:
                invalid += 1
                continue
            chunk = {**chunk, 'texto': body, 'chunk_id_original': original_id}
            for field in ('collection', 'document_id', 'title'):
                chunk.setdefault(field, None)
            digest = K._body_hash(body)
            source = {k: v for k, v in chunk.items() if k not in {'texto', 'text'}}
            uid = K._digest(K._json([digest, original_id, chunk.get('collection'),
                                     chunk.get('document_id'), chunk.get('source_file')]))
            position = chunk.get('word_offset')
            if not isinstance(position, int):
                match = re.search(r':w(\d+)(?::|$)', original_id)
                position = int(match[1]) if match else -1
            doc = K._json([chunk.get('collection'), chunk.get('document_id')])
            batch.append((str(chunk.get('collection')), digest, body, K._json(chunk), uid, original_id, doc,
                          position, int(K._known_boundaries(chunk)), K._json(source)))
            produced += 1
            if len(batch) >= BATCH:
                pickle.dump(batch, out, protocol=pickle.HIGHEST_PROTOCOL)
                batch = []
        if batch:
            pickle.dump(batch, out, protocol=pickle.HIGHEST_PROTOCOL)
    return dict(path=name, chunks=produced, invalid=invalid, size=task['size'])


def _read(path):
    with gzip.open(path, 'rb') as stream:
        while True:
            try:
                yield pickle.load(stream)
            except EOFError:
                return


# ---------------------------------------------------------------- escrita

def _eta(seconds):
    seconds = int(seconds)
    return f'{seconds // 3600}h{(seconds % 3600) // 60:02d}m' if seconds >= 3600 else f'{seconds // 60}m{seconds % 60:02d}s'


def build(manifest, directory, workers=None, cache_mb=None, target_mb=64, progress=print, executor=None,
          adopt_from=None):
    """Constrói (ou reaproveita) o índice de um manifesto. Retorna (info, caminho do banco).

    `adopt_from`: pastas onde procurar um índice idêntico já pronto (None: as dos fluxos
    anteriores; lista vazia: não procurar)."""
    workers = workers or default_workers()
    cache_mb = cache_mb or default_cache_mb()
    name = Path(directory).name
    progress(f'[índice:{name}] conferindo integridade dos arquivos', flush=True)
    snap = snapshot(manifest, directory, workers)
    found = ready(snap)
    if found:
        progress(f'[índice:{name}] já pronto ({found["chunks"]:,} trechos); reaproveitado', flush=True)
        return found, snap['folder'] / 'corpus.sqlite3'
    folder = snap['folder']
    folder.mkdir(parents=True, exist_ok=True)
    from pipeline.inventario.locking import output_lock
    with output_lock(folder):
        found = ready(snap)
        if found:
            return found, folder / 'corpus.sqlite3'
        for stale in folder.glob('corpus-*.build.sqlite3'):
            stale.unlink()
        for stale in folder.glob('prep-*.pkl.gz'):
            stale.unlink()
        adopted = adopt(snap, legacy_roots() if adopt_from is None else adopt_from, progress)
        if adopted:
            return adopted
        tasks = plan(snap, target_mb * 1024 * 1024)
        total = sum(t['size'] for t in tasks) or 1
        progress(f'[índice:{name}] {len(tasks)} tarefas, {total / 2**30:.2f} GB, {workers} processos, cache {cache_mb} MB',
                 flush=True)
        started = time.monotonic()
        with tempfile.NamedTemporaryFile(prefix='corpus-', suffix='.build.sqlite3', dir=folder, delete=False) as stream:
            temporary = Path(stream.name)
        db = sqlite3.connect(temporary)
        own = executor is None
        pool = executor or make_pool(workers)
        try:
            for pragma in ('journal_mode=OFF', 'synchronous=OFF', 'locking_mode=EXCLUSIVE',
                           f'cache_size=-{cache_mb * 1024}'):
                db.execute('PRAGMA ' + pragma)
            db.executescript(SCHEMA_TABLES)
            seen, next_id, count, invalid, sources = {}, 0, 0, 0, 0
            by_collection = Counter()
            done_bytes, last_report = 0, 0.0
            window = max(2, 2 * workers)
            pending = []
            queue = list(tasks)

            def submit():
                while queue and len(pending) < window:
                    t = queue.pop(0)
                    pending.append((t, pool.submit(prepare, t, snap['collections'][t['collection']], str(folder))))

            submit()
            while pending:
                task, future = pending.pop(0)
                while True:
                    try:
                        result = future.result(timeout=60)
                        break
                    except FutureTimeout:
                        # A escrita segue a ordem original; mostra que está viva e em quê.
                        mem = free_mb()
                        progress(f'[índice:{name}] aguardando tarefa {tasks.index(task) + 1}/{len(tasks)} '
                                 f'({snap["collections"][task["collection"]]["id"]}, {task["size"] / 2**20:.0f} MB)'
                                 + (f' | memória livre {mem / 1024:.1f} GB' if mem is not None else ''), flush=True)
                submit()
                for batch in _read(result['path']):
                    chunk_rows, source_rows = [], []
                    for coll, digest, body, payload, uid, original_id, doc, pos, known, spayload in batch:
                        key = bytes.fromhex(digest)  # metade da memória de uma string hex
                        rowid = seen.get(key)
                        if rowid is None:
                            next_id += 1
                            rowid = seen[key] = next_id
                            chunk_rows.append((rowid, digest, body, payload))
                            count += 1
                            by_collection[coll] += 1
                        source_rows.append((rowid, uid, original_id, doc, pos, known, spayload))
                    db.executemany('INSERT INTO chunks(id,digest,body,payload) VALUES(?,?,?,?)', chunk_rows)
                    before = db.total_changes
                    db.executemany('INSERT OR IGNORE INTO sources VALUES(?,?,?,?,?,?,?)', source_rows)
                    sources += db.total_changes - before
                os.unlink(result['path'])
                invalid += result['invalid']
                done_bytes += result['size']
                now = time.monotonic()
                if now - last_report >= 20 or not pending:
                    last_report = now
                    elapsed = now - started
                    rest = elapsed * (total - done_bytes) / max(done_bytes, 1)
                    mem = free_mb()
                    progress(f'[índice:{name}] {done_bytes / total:.0%} lido | {count:,} trechos | '
                             f'{elapsed / 60:.1f} min | restante da leitura ~{_eta(rest)}'
                             + (f' | memória livre {mem / 1024:.1f} GB' if mem is not None else ''), flush=True)
            if not count:
                raise ValueError('As fontes informadas não contêm trechos originais válidos')
            progress(f'[índice:{name}] criando índices secundários', flush=True)
            db.executescript(SCHEMA_INDEXES)
            progress(f'[índice:{name}] montando o índice de texto (FTS5)', flush=True)
            db.execute("INSERT INTO search(search) VALUES('rebuild')")
            db.execute("INSERT INTO search(search) VALUES('optimize')")
            db.execute("INSERT INTO metadata VALUES('fingerprint',?)", (snap['fingerprint'],))
            db.commit()
        except BaseException:
            db.close()
            temporary.unlink(missing_ok=True)
            for leftover in folder.glob('prep-*.pkl.gz'):
                leftover.unlink(missing_ok=True)
            raise
        finally:
            if own:
                pool.shutdown(cancel_futures=True)
        db.close()
        path = folder / 'corpus.sqlite3'
        temporary.replace(path)
        info = {'version': K._VERSION, 'fingerprint': snap['fingerprint'], 'signature': snap['fingerprint'],
                'engine': K._ENGINE, 'chunks': count, 'source_records': sources,
                'invalid_chunks_skipped': invalid, 'collections': dict(by_collection),
                'coverage': 'verified_manifest', 'cobertura': 'verified_manifest',
                'complete_corpus': snap['complete'], 'corpus_bruto_completo': snap['complete'],
                'sources': snap['files'], 'index_path': str(path),
                'warnings': ([] if snap['complete'] else [
                    'Cobertura parcial dos materiais originais disponíveis; ausência de resultados não demonstra ausência no corpus completo.']),
                'neighbors': 'same_document_known_boundaries_only',
                'construcao': dict(paralela=True, processos=workers, tarefas=len(tasks),
                                   minutos=round((time.monotonic() - started) / 60, 1))}
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', prefix='indice-', suffix='.json', dir=folder,
                                         delete=False) as stream:
            stream.write(json.dumps(info, ensure_ascii=False, indent=2) + '\n')
            temporary_info = Path(stream.name)
        temporary_info.replace(folder / 'indice.json')
        progress(f'[índice:{name}] pronto: {count:,} trechos em {info["construcao"]["minutos"]} min', flush=True)
        return info, path


def attach(manifest, directory, info, path):
    """CorpusIndex pronto para busca, sem refazer a conferência de hash."""
    index = K.CorpusIndex(directory, manifest=manifest)
    index.path, index.info = Path(path), info
    return index


def main(argv=None):
    from .retrieval import discover
    from pipeline.qa_research.v3.runtime import ROOT
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--manifest', nargs='+', default=['auto'])
    parser.add_argument('--index-cache', type=Path, default=ROOT / 'dataset/indices_refino')
    parser.add_argument('--workers', type=int, default=default_workers())
    parser.add_argument('--cache-mb', type=int, default=default_cache_mb())
    parser.add_argument('--target-mb', type=int, default=64, help='Tamanho de cada faixa de JSONL por tarefa')
    parser.add_argument('--adotar-de', nargs='*', type=Path, default=None,
                        help='Pastas com índices prontos de outros fluxos (padrão: pipeline/qa_research/.local/index)')
    parser.add_argument('--sem-adotar', action='store_true', help='Não procurar índices prontos; sempre construir')
    args = parser.parse_args(argv)
    adopt_from = [] if args.sem_adotar else args.adotar_de
    manifests, notes = discover(ROOT, args.manifest)
    for n in notes:
        print('[manifesto]', n['manifesto'], '|', n['estado'], flush=True)
    if not manifests:
        print('Nenhum manifesto pronto.')
        return 2
    with make_pool(args.workers) as pool:
        for manifest in manifests:
            build(manifest, args.index_cache / Path(manifest).parent.name, args.workers, args.cache_mb,
                  args.target_mb, executor=pool, adopt_from=adopt_from)
    print('Índices prontos. O refino reaproveita estes índices automaticamente.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
