"""Busca BM25 no acervo autorizado completo disponível, com contexto vizinho separado.

SQLite FTS5 fornece o recuperador; a decisão semântica pertence ao verificador.
Sem manifesto, usa todos os índices/seleções salvos, declarando a cobertura parcial.
"""
import json
import re
import sqlite3
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, content_words, norm, read_json, read_jsonl, sha


def file_hash(path):
    import hashlib
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def source_files(origins):
    files = []
    for origin in origins:
        root = Path(origin)
        if not root.is_dir():
            raise ValueError(f'inventário ausente: {root}')
        files.extend(sorted(root.glob('subtopicos/*/selecao.json')))
        for name in ('trechos.jsonl', 'candidatos.jsonl'):
            path = root / 'indices' / name
            if path.exists():
                files.append(path)
    return files


def saved_chunks(origins):
    for origin in origins:
        path = Path(origin) / 'indices/trechos.jsonl'
        if path.exists():
            with path.open(encoding='utf-8') as stream:
                for line in stream:
                    if line.strip():
                        row = json.loads(line)
                        if row.get('texto'):
                            yield row
        for path in sorted(Path(origin).glob('subtopicos/*/selecao.json')):
            for item in read_json(path)['assuntos'].values():
                yield from item.get('trechos', [])


class CorpusIndex:
    def __init__(self, directory, origins, manifest=None):
        self.directory, self.origins = Path(directory), list(origins)
        self.manifest = Path(manifest) if manifest else None
        self.path = self.directory / 'corpus.sqlite3'

    def build(self):
        files = source_files(self.origins)
        fingerprint = [[p.as_posix(), file_hash(p)] for p in files]
        collections = None
        if self.manifest:
            from pipeline.domain_corpora.manifest import load_manifest
            _, collections = load_manifest(self.manifest, verify=True)
            fingerprint.append([self.manifest.as_posix(), file_hash(self.manifest)])
        signature = sha(json.dumps(['fts-v11-1', fingerprint], sort_keys=True), 40)
        previous = read_json(self.directory / 'indice.json')
        if previous and previous.get('signature') == signature and self.path.exists():
            self.info = previous
            return previous
        self.directory.mkdir(parents=True, exist_ok=True)
        # Um arquivo temporário só é promovido após concluir a indexação.
        temporary = self.directory / 'corpus.build.sqlite3'
        if temporary.exists():
            temporary.unlink()
        db = sqlite3.connect(temporary)
        try:
            db.execute('CREATE TABLE chunks (id INTEGER PRIMARY KEY, uid TEXT UNIQUE, doc TEXT, pos INTEGER, body TEXT, payload TEXT)')
            db.execute('CREATE INDEX document_position ON chunks(doc,pos)')
            db.execute("CREATE VIRTUAL TABLE search USING fts5(body,content='chunks',content_rowid='id',tokenize='unicode61 remove_diacritics 2')")
            inserted = 0
            def insert(chunk):
                nonlocal inserted
                body = chunk.get('texto', '')
                if not body.strip():
                    return
                original = chunk['chunk_id']
                uid = sha(original + '\n' + body, 40)
                pos = re.search(r':w(\d+)', original)
                stored = {**chunk, 'chunk_id_original': original, 'chunk_id': original + ':h' + sha(body, 12)}
                doc = f"{chunk.get('collection')}:{chunk.get('document_id')}"
                cursor = db.execute('INSERT OR IGNORE INTO chunks(uid,doc,pos,body,payload) VALUES(?,?,?,?,?)',
                                    (uid, doc, int(pos[1]) if pos else -1, body, json.dumps(stored, ensure_ascii=False)))
                if cursor.rowcount:
                    db.execute('INSERT INTO search(rowid,body) VALUES(?,?)', (cursor.lastrowid, body))
                    inserted += 1
                    if inserted % 50000 == 0:
                        print(f'[índice] {inserted} trechos originais indexados', flush=True)
            for chunk in saved_chunks(self.origins):
                insert(chunk)
            if collections:
                from pipeline.domain_corpora.manifest import iter_units
                from pipeline.inventario.varredura import windows
                for cid, body, metadata in windows(iter_units(collections)):
                    insert({**metadata, 'chunk_id': cid, 'texto': body})
            count = db.execute('SELECT count(*) FROM chunks').fetchone()[0]
            db.commit()
        finally:
            db.close()
        temporary.replace(self.path)
        self.info = {'signature': signature, 'chunks': count, 'fontes': fingerprint,
                     'cobertura': 'manifesto_verificado_e_indices' if collections else 'indices_e_selecoes_salvos',
                     'corpus_bruto_completo': bool(collections), 'recuperador': 'SQLite FTS5 BM25 + verificação semântica LLM'}
        atomic_json(self.directory / 'indice.json', self.info)
        return self.info

    def search(self, query, limit=8, exclude=(), neighbors=True):
        terms = list(dict.fromkeys(content_words(query)))[:30]
        if not terms:
            return []
        match = ' OR '.join('"' + w.replace('"', '""') + '"' for w in terms)
        db = sqlite3.connect(f'{self.path.resolve().as_uri()}?mode=ro', uri=True)
        try:
            rows = db.execute('SELECT c.id,c.doc,c.pos,c.payload FROM search JOIN chunks c ON c.id=search.rowid '
                              'WHERE search MATCH ? ORDER BY bm25(search) LIMIT ?', (match, max(60, limit * 8))).fetchall()
            candidates, seen = [], set(exclude)
            def add(row, reason):
                payload = json.loads(row[3])
                digest = sha(payload['texto'], 64)
                if payload['chunk_id'] in seen or digest in seen:
                    return
                seen.update((payload['chunk_id'], digest))
                candidates.append({**payload, 'recuperacao': reason})
            # Primeiro os melhores documentos; contexto nunca toma toda a cota.
            for row in rows:
                add(row, 'bm25')
                if len(candidates) >= limit:
                    break
            primary = list(candidates)
            if neighbors:
                for p in primary[:2]:
                    if 'unknown' in p.get('source_boundary', ''):
                        continue
                    pos = re.search(r':w(\d+)', p['chunk_id_original'])
                    if not pos:
                        continue
                    doc = f"{p.get('collection')}:{p.get('document_id')}"
                    adjacent = db.execute('SELECT id,doc,pos,payload FROM chunks WHERE doc=? AND pos BETWEEN ? AND ? '
                                          'ORDER BY abs(pos-?) LIMIT 3', (doc, int(pos[1])-350, int(pos[1])+350, int(pos[1]))).fetchall()
                    for row in adjacent:
                        add(row, 'contexto_vizinho_separado')
            return candidates[:limit + 4]
        finally:
            db.close()


def load_topics(origins, filters, max_units):
    found = {}
    for origin in origins:
        for folder in sorted(Path(origin).glob('subtopicos/*')):
            metadata = read_json(folder / 'assuntos.json')
            concepts = read_json(folder / 'conceitos.json')
            if not metadata or not concepts:
                continue
            sub = metadata['subtopico']
            if not any(norm(f) == norm(sub['subtopico']) or norm(sub['subtopico']).startswith(norm(f)) for f in filters):
                continue
            if sub['key'] in found:
                raise ValueError(f'subtópico duplicado nas origens: {sub["subtopico"]}')
            subjects = {a['id']: a for a in metadata['assuntos']}
            queues = {aid: list(plan['conceitos']) for aid, plan in concepts.items() if aid in subjects}
            units = []
            while any(queues.values()) and len(units) < max_units:
                for aid, queue in queues.items():
                    if queue and len(units) < max_units:
                        concept = queue.pop(0)
                        units.append({'id': concept['kid'], 'conceito': concept['nome'],
                                      'foco': concept.get('foco') or concept['nome'],
                                      'assunto': subjects[aid], 'origem': folder.as_posix()})
            found[sub['key']] = {**sub, 'unidades': units}
    for f in filters:
        matches = [s for s in found.values() if norm(s['subtopico']) == norm(f) or norm(s['subtopico']).startswith(norm(f))]
        if len(matches) != 1:
            raise ValueError(f'filtro deve identificar exatamente um subtópico: {f} ({len(matches)} encontrados)')
    return list(found.values())
