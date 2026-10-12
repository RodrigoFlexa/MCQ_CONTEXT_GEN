"""Etapa 2: uma passada pelo corpus inteiro, guardando candidatos lexicais por assunto.

O corpus é grande demais para embutir por completo; esta passada barata (CPU)
seleciona, para cada (assunto, coleção), os melhores trechos por termos técnicos
em português e inglês. A ordenação fina é feita depois, na GPU.
"""
import hashlib
import heapq
import json
import re
import time
from collections import defaultdict
from contextlib import closing
from itertools import islice

from .textutil import GENERIC_TERMS, content_words, tokens

VERSION = 'varredura-v2'


def iter_limited_units(collections, limit_units=None):
    """Encerra a leitura de cada coleção após N unidades; não percorre o restante só para ignorá-lo."""
    from pipeline.domain_corpora.manifest import iter_units
    for collection in collections:
        with closing(iter_units([collection])) as rows:
            yield from (islice(rows, limit_units) if limit_units is not None else rows)

_STRUCT = re.compile(r'^\s*(?:sum[aá]rio|lista de (?:figuras|tabelas|abreviaturas|siglas)|table of contents|'
                     r'list of (?:figures|tables|abbreviations)|refer[eê]ncias(?: bibliogr[aá]ficas)?|bibliography|'
                     r'references|agradecimentos|acknowledg)', re.I)
_CITATION = re.compile(r'\(\s*[A-ZÀ-Ú][A-Za-zÀ-ú]+(?: et al\.?)?,? \d{4}\)|\b\d{4}[a-z]?\.\s*$')


class TermIndex:
    """Índice de termos (1 a 5 tokens) para todos os assuntos selecionados."""

    def __init__(self, assuntos):
        self.first = defaultdict(list)   # primeiro token -> [(tupla, [(akey, tipo)])]
        terms = defaultdict(set)
        for a in assuntos:
            for t in a['termos_pt'] + a['termos_en']:
                tup = tuple(tokens(t))
                if tup and ' '.join(tup) not in GENERIC_TERMS:
                    terms[tup].add((a['key'], 's'))
            for w in set(content_words(a['consulta_pt'] + ' ' + a['consulta_en'])):
                terms[(w,)].add((a['key'], 'q'))
        for tup, entries in terms.items():
            self.first[tup[0]].append((tup, sorted(entries)))
        self.n_terms = len(terms)

    def match(self, toks):
        found = defaultdict(lambda: [set(), set()])
        first = self.first
        n = len(toks)
        for i, tok in enumerate(toks):
            cands = first.get(tok)
            if not cands:
                continue
            for tup, entries in cands:
                L = len(tup)
                if L == 1 or (i + L <= n and tuple(toks[i:i + L]) == tup):
                    for akey, kind in entries:
                        found[akey][0 if kind == 's' else 1].add(tup)
        return found


def windows(units, chunk_words=350, stride=250, min_words=80, limit_units=None):
    """Janelas de palavras que não atravessam documentos. Petrolês (sem fronteiras
    confiáveis) é tratado como um documento por arquivo, como no restante do projeto."""
    if not 1 <= stride <= chunk_words or chunk_words < min_words:
        raise ValueError('Tamanho/stride de janela inválido')
    buf = []          # (palavra, página, linha)
    meta = None
    key = None
    offset = 0        # posição (em palavras) do início do buffer dentro do documento
    fresh = 0         # palavras ainda não emitidas em nenhuma janela
    count = {}
    previous_page = None

    def emit(part):
        words = [w for w, _, _ in part]
        pages = [p for _, p, _ in part if p is not None]
        lines = [l for _, _, l in part if l is not None]
        prov = {k: v for k, v in meta.items() if k not in ('text', 'line', 'extraction_issues', 'page')}
        prov['page_ini'] = pages[0] if pages else None
        prov['page_fim'] = pages[-1] if pages else None
        prov['linha_ini'] = lines[0] if lines else None
        prov['linha_fim'] = lines[-1] if lines else None
        cid = f"{meta['collection']}:{meta['document_id']}:p{prov['page_ini']}:w{offset}"
        return cid, ' '.join(words), prov

    for unit in units:
        coll = unit['collection']
        if limit_units:
            count[coll] = count.get(coll, 0) + 1
            if count[coll] > limit_units:
                continue
        k = (coll, unit['document_id'])
        page = unit.get('page')
        gap = (k == key and isinstance(page, int) and isinstance(previous_page, int) and
               page not in (previous_page, previous_page + 1))
        if k != key or gap:
            if meta is not None and fresh >= 40 and len(buf) >= min_words:
                yield emit(buf)
            buf, key, meta, offset, fresh = [], k, unit, 0, 0
        previous_page = page
        page, line = unit.get('page'), unit.get('line')
        for w in unit['text'].split():
            buf.append((w, page, line))
            fresh += 1
            if len(buf) >= chunk_words:
                yield emit(buf)
                buf = buf[stride:]
                offset += stride
                fresh = 0  # tudo que restou no buffer já saiu na janela emitida
    if meta is not None and fresh >= 40 and len(buf) >= min_words:
        yield emit(buf)


def noisy(text, toks):
    if not toks:
        return True
    digits = sum(t.isdigit() for t in toks) / len(toks)
    if digits > 0.30:
        return True
    alpha = sum(c.isalpha() for c in text) / max(1, len(text))
    if alpha < 0.55:
        return True
    if _STRUCT.search(text[:160]):
        return True
    # Listas de referências: muitas citações autor-ano.
    if len(re.findall(r'\b(?:19|20)\d{2}\b', text)) > 12 and text.count('.') > 25:
        return True
    return False


def scan(units, assuntos, quota=40, chunk_words=350, stride=250, min_words=80, limit_units=None,
         progress_every=200000, log=print):
    """Retorna {akey: [candidatos]} com até `quota` por (assunto, coleção)."""
    index = TermIndex(assuntos)
    heaps = defaultdict(list)
    texts = {}
    refs = defaultdict(int)
    stats = {'janelas': 0, 'ruido': 0, 'com_termos': 0, 'por_colecao': defaultdict(int)}
    started = time.time()
    seq = 0
    for cid, text, prov in windows(units, chunk_words, stride, min_words, limit_units):
        stats['janelas'] += 1
        coll = prov['collection']
        stats['por_colecao'][coll] += 1
        if stats['janelas'] % progress_every == 0:
            rate = stats['janelas'] / max(1e-6, time.time() - started)
            log(f"[varredura] {stats['janelas']:,} janelas ({rate:,.0f}/s) | coleção atual: {coll} | "
                f"candidatos retidos: {len(texts):,}")
        toks = tokens(text)
        if noisy(text, toks):
            stats['ruido'] += 1
            continue
        found = index.match(toks)
        if not found:
            continue
        stats['com_termos'] += 1
        for akey, (strong, query) in found.items():
            if not strong and len(query) < 3:
                continue
            score = 3.0 * min(len(strong), 6) + 1.0 * min(len(query), 8)
            heap = heaps[(akey, coll)]
            tie = int(hashlib.sha256((akey + cid).encode()).hexdigest()[:12], 16)
            item = (score, tie, cid)
            if len(heap) < quota:
                heapq.heappush(heap, item)
            elif item > heap[0]:
                old = heapq.heapreplace(heap, item)
                refs[old[2]] -= 1
                if refs[old[2]] <= 0:
                    texts.pop(old[2], None)
                    refs.pop(old[2], None)
            else:
                continue
            seq += 1
            refs[cid] += 1
            if cid not in texts:
                texts[cid] = (text, prov)
    result = defaultdict(list)
    for (akey, coll), heap in heaps.items():
        for score, _, cid in sorted(heap, reverse=True):
            text, prov = texts[cid]
            result[akey].append({'chunk_id': cid, 'lex_score': score, 'texto': text, **prov})
    stats['por_colecao'] = dict(stats['por_colecao'])
    stats['segundos'] = round(time.time() - started, 1)
    stats['termos_indexados'] = index.n_terms
    stats['candidatos_unicos'] = len(texts)
    return dict(result), stats


def signature(assuntos, manifest_path, params):
    from pathlib import Path
    manifest_path = Path(manifest_path).resolve()
    payload = {'v': VERSION, 'manifest': str(manifest_path), 'params': params,
               'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
               'a': [(a['key'], a['termos_pt'], a['termos_en'], a['consulta_pt'], a['consulta_en']) for a in assuntos]}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
