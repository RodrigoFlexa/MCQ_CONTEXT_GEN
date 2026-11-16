"""Acervo de busca: todos os corpora instalados + evidências herdadas, fundidos por RRF.

Reaproveita o índice BM25 persistente (`CorpusIndex`) e a busca bilíngue PT/EN
(`bilingual_search`). Cada manifesto vira um índice; a fusão é por posição (RRF)
e deduplica passagens idênticas entre coleções pelo hash do conteúdo.
"""
import json
import threading
from pathlib import Path

from pipeline.domain_corpora.io_utils import file_hash
from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.corpus import CorpusIndex
from pipeline.qa_research.v2.language import bilingual_search
from pipeline.qa_research.v2.navigation import navigation_reason
from pipeline.qa_research.v3.runtime import digest

# Candidatos procurados em locais conhecidos quando --manifest auto.
KNOWN = ('dataset/domain_corpora/manifest.json', 'dataset/professional_corpora_v3/manifest.json',
         'dataset/professional_corpora_v2/manifest.json')
META = ('collection', 'document_id', 'chunk_id', 'language', 'title', 'url', 'page_ini', 'page_fim',
        'source_boundary', 'jurisdiction', 'document_type', 'year', 'license', 'evidence_origin')


def discover(root, explicit=None):
    """Manifestos prontos. Explícitos que não existem são erro; os automáticos, aviso."""
    found, notes = [], []
    candidates = explicit if explicit and explicit != ['auto'] else [str(Path(root) / k) for k in KNOWN]
    for raw in candidates:
        path = Path(raw)
        if not path.is_file():
            if explicit and explicit != ['auto']:
                raise FileNotFoundError('Manifesto ausente: ' + str(path))
            notes.append(dict(manifesto=str(path), estado='ausente'))
            continue
        data = json.loads(path.read_text(encoding='utf-8'))
        if data.get('ready') is not True or data.get('sample'):
            notes.append(dict(manifesto=str(path), estado='não pronto ou amostra; ignorado'))
            continue
        found.append(path.resolve())
        notes.append(dict(manifesto=str(path), estado='usado', status=data.get('status'),
                          colecoes=[c['id'] for c in data.get('collections', [])]))
    return found, notes


class Acervo:
    """Índices BM25 independentes fundidos por RRF; a busca é atômica entre threads."""
    def __init__(self, indexes, info=None):
        self.indexes = indexes
        self.info = info or []
        self.last_query_trace = {}
        self.lock = threading.Lock()

    @classmethod
    def from_manifests(cls, manifests, cache):
        indexes, info = [], []
        for path in manifests:
            name = Path(path).parent.name
            index = CorpusIndex(Path(cache) / name, manifest=path)
            built = index.build()
            indexes.append((name, index))
            info.append(dict(origem=name, manifesto=str(path), manifesto_sha256=file_hash(path),
                             trechos=built['chunks'], colecoes=built['collections'], completo=built['complete_corpus']))
        return cls(indexes, info)

    def with_inherited(self, evidence_file, cache):
        """Passagens citadas pela geração antiga do mesmo documento (dez_areas_v1)."""
        evidence = Path(evidence_file)
        if not evidence.is_file():
            return Acervo(self.indexes, self.info + [dict(origem='evidencias_herdadas', estado='ausente', arquivo=str(evidence))])
        root = Path(cache) / 'herdadas' / digest(str(evidence.resolve()))[:16]
        root.mkdir(parents=True, exist_ok=True)
        records = []
        for line in evidence.read_text(encoding='utf-8-sig').splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row.get('texto'), str) or not row['texto'].strip():
                continue
            records.append(dict(collection='evidencias_herdadas', document_id='selection-' + str(row.get('id')),
                text=row['texto'], title=row.get('title') or evidence.name, page=row.get('page_ini'),
                language=row.get('language', 'und'), jurisdiction=row.get('jurisdiction'),
                source_boundary='selected_passage; not a complete document', url=row.get('url'),
                original_collection=row.get('collection'), original_document_id=row.get('document_id')))
        if not records:
            return Acervo(self.indexes, self.info + [dict(origem='evidencias_herdadas', estado='vazio', arquivo=str(evidence))])
        pages = root / 'pages.jsonl'
        pages.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in records), encoding='utf-8')
        manifest = root / 'manifest.json'
        atomic_json(manifest, dict(schema='petroquest-professional-corpora-v1', ready=True, partial=True,
            coverage='Seleção original herdada', collections=[dict(id='evidencias_herdadas', format='pages_jsonl',
                path=pages.name, sha256=file_hash(pages), documents=len({r['document_id'] for r in records}))]))
        index = CorpusIndex(root / 'index', manifest=manifest)
        built = index.build()
        return Acervo(self.indexes + [('evidencias_herdadas', index)],
                      self.info + [dict(origem='evidencias_herdadas', arquivo=str(evidence), trechos=built['chunks'])])

    def search(self, query, limit=8, exclude=()):
        ranked, traces = {}, []
        for origin, index in self.indexes:
            for rank, row in enumerate(index.search(query, limit=limit, exclude=exclude), 1):
                entry = ranked.setdefault(row['content_hash'], dict(row=dict(row, evidence_origin=origin), score=0.))
                entry['score'] += 1 / (60 + rank)
            traces.append(dict(origem=origin, **(index.last_query_trace or {})))
        result = [r['row'] for r in sorted(ranked.values(), key=lambda r: (-r['score'], r['row']['chunk_id']))][:limit]
        self.last_query_trace = dict(query=query, engine='RRF de índices BM25', indices=[
            {k: t.get(k) for k in ('origem', 'match_expression', 'chunk_ids', 'duration_seconds')} for t in traces],
            chunk_ids=[r['chunk_id'] for r in result])
        return result

    def query(self, pairs, limit, seen=(), max_per_document=3, keep=16):
        """Busca PT/EN e seleção diversificada: uma passagem por coleção primeiro."""
        with self.lock:
            hits, traces = bilingual_search(self, pairs, limit)
        seen = set(seen)
        clean, excluded = [], []
        for row in hits:
            reason = navigation_reason(row)
            if reason:
                excluded.append(dict(chunk_id=row['chunk_id'], motivo=reason))
                continue
            pid = 'E' + digest([row['chunk_id'], row['content_hash']])[:16]
            if pid in seen:
                continue
            clean.append(dict(id=pid, texto=row['texto'], content_hash=row['content_hash'],
                              **{k: row.get(k) for k in META}))
        first, collections = [], set()
        for row in clean:
            if row['collection'] not in collections:
                first.append(row)
                collections.add(row['collection'])
        chosen, ids, per_doc = [], set(), {}
        for row in first + clean:
            if row['id'] in ids:
                continue
            key = (row['collection'], row['document_id'])
            if per_doc.get(key, 0) >= max_per_document:
                continue
            chosen.append(row)
            ids.add(row['id'])
            per_doc[key] = per_doc.get(key, 0) + 1
            if len(chosen) >= keep:
                break
        return chosen, dict(consultas=[{k: t.get(k) for k in ('query', 'query_language', 'chunk_ids')} for t in traces],
                            excluidas=excluded, candidatas=len(clean))


def public(passage):
    """Metadados para os auxiliares; o texto original fica fora da coleta."""
    return {k: passage.get(k) for k in ('id', 'content_hash', *META)}
