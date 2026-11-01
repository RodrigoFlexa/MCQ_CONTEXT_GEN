"""Pesquisa por intervenção: passagens herdadas + corpus instalado, até duas leituras."""
import asyncio
import json
import threading
from pathlib import Path

from pipeline.domain_corpora.io_utils import file_hash
from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.corpus import CorpusIndex
from pipeline.qa_research.v2.language import bilingual_search
from pipeline.qa_research.v2.navigation import navigation_reason
from pipeline.qa_research.v3.runtime import digest, CallFailure, Fatal
from pipeline.inventario.llm import BudgetExceeded
from . import VERSION, contracts as C, prompts as P


class CombinedIndex:
    """Fusão RRF dos índices existentes; não reconstrói o motor de recuperação."""
    def __init__(self, indexes):
        self.indexes = indexes
        self.last_query_trace = {}
        self.lock = threading.Lock()

    def query(self, pairs, limit):
        # last_query_trace pertence ao indexador; manter cada busca bilíngue atômica.
        with self.lock:
            return bilingual_search(self, pairs, limit)

    def search(self, query, limit=8, exclude=()):
        ranked = {}
        traces = []
        for origin, index in self.indexes:
            for rank, row in enumerate(index.search(query, limit=limit, exclude=exclude), 1):
                key = row['content_hash']
                entry = ranked.setdefault(key, dict(row=dict(row, evidence_origin=origin), score=0.))
                entry['score'] += 1 / (60 + rank)
            traces.append(dict(origem=origin, **index.last_query_trace))
        result = [r['row'] for r in sorted(ranked.values(), key=lambda r: (-r['score'], r['row']['chunk_id']))][:limit]
        self.last_query_trace = dict(query=query, engine='RRF de índices BM25', indices=traces,
                                     chunk_ids=[r['chunk_id'] for r in result])
        return result


def inherited_index(base, output):
    evidence = Path(base['evidencias'])
    if not evidence.is_file():
        return None
    root = Path(output) / '.local' / 'herdadas'
    root.mkdir(parents=True, exist_ok=True)
    path = root / 'pages.jsonl'
    records = []
    original_hash = file_hash(evidence)
    for line in evidence.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        C.require(C.text(row.get('texto')), 'Evidência herdada sem passagem original')
        # A seleção antiga não é um documento contínuo. Dar a cada passagem uma
        # unidade de indexação impede colar trechos não adjacentes do mesmo TXT/PDF.
        records.append(dict(collection='evidencias_herdadas', document_id='selection-' + row['id'],
            text=row['texto'], title=row.get('title') or evidence.name, page=row.get('page_ini'),
            language=row.get('language', 'und'), jurisdiction=row.get('jurisdiction'),
            source_boundary='selected_passage; not a complete document', source_sha256=row.get('source_sha256'),
            original_document_id=row.get('document_id'), original_source_boundary=row.get('source_boundary', 'unknown'),
            original_page_ini=row.get('page_ini'), original_page_fim=row.get('page_fim', row.get('page_ini')),
            original_collection=row.get('collection'), original_evidence_id=row['id'],
            original_chunk_id=row.get('chunk_id'), url=row.get('url'),
            original_evidence_file_sha256=original_hash))
    if not records:
        return None
    path.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in records), encoding='utf-8')
    manifest = root / 'manifest.json'
    atomic_json(manifest, dict(schema='petroquest-professional-corpora-v1', ready=True, partial=True,
        coverage='Seleção original herdada, sem presumir corpus completo', collections=[dict(id='evidencias_herdadas',
            format='pages_jsonl', path=path.name, sha256=file_hash(path), documents=len({r['document_id'] for r in records}))]))
    index = CorpusIndex(root / 'index', manifest=manifest)
    index.build()
    return index


def source(row):
    sid = 'S' + digest([row['chunk_id'], row['content_hash']])[:20]
    # O modelo cita um ID; o programa conserva o texto e seu intervalo exatos.
    # Cada chunk já tem tamanho limitado pelo indexador. Não corta a passagem.
    paragraph = dict(id=sid + 'P01', fonte=sid, inicio=0, fim=len(row['texto']), texto=row['texto'])
    return dict(id=sid, collection=row.get('original_collection') or row.get('collection'),
        origem=row.get('evidence_origin'), title=(row.get('title') or '')[:1000],
        url=row.get('url'), document_id=row.get('original_document_id') or row.get('document_id'), chunk_id=row['chunk_id'],
        original_evidence_id=row.get('original_evidence_id'), source_boundary=row.get('original_source_boundary', row.get('source_boundary')),
        retrieval_boundary=row.get('source_boundary'), original_evidence_file_sha256=row.get('original_evidence_file_sha256'),
        source_sha256=row.get('source_sha256'), content_hash=row['content_hash'],
        language=row.get('language'), jurisdiction=row.get('jurisdiction'),
        page_ini=row.get('original_page_ini', row.get('page_ini')),
        page_fim=row.get('original_page_fim', row.get('page_fim')), paragrafos=[paragraph])


def public_research(result):
    return dict(result, fontes=[dict(s, paragrafos=[{k: v for k, v in p.items() if k != 'texto'}
        for p in s['paragrafos']]) for s in result['fontes']])


async def investigate(intervention, base, index, config, calls):
    findings, sources, traces, reports, pending, errors = [], {}, [], [], [], []
    pairs, done_queries = intervention['consultas'], set()
    if not pairs:
        return dict(id=intervention['id'], achados=[], fontes=[], consultas=[], leituras=0,
            pendencias=[] if intervention.get('tipo') == 'editorial' else ['Pesquisa não executada: consultas ausentes'],
            erros=[], status='dispensada_editorial' if intervention.get('tipo') == 'editorial' else 'nao_executada')
    seen = set()
    for turn in range(config['research_rounds']):
        pairs = [p for p in pairs if (p['pt'].casefold(), p['en'].casefold()) not in done_queries]
        if not pairs:
            break
        done_queries.update((p['pt'].casefold(), p['en'].casefold()) for p in pairs)
        hits, queries = await asyncio.to_thread(index.query, pairs, config['retrieval_candidates'])
        traces.extend(dict(rodada=turn + 1, **q) for q in queries)
        selected, counts = [], {}
        for hit in hits:
            if navigation_reason(hit):
                continue
            row = source(hit)
            if row['id'] in seen or counts.get(row['document_id'], 0) >= config['max_per_document']:
                continue
            candidate = selected + [row]
            payload = dict(schema=VERSION, entrada=base['entrada'], intervencao=intervention,
                anteriores=findings, fontes=candidate)
            if len(json.dumps(payload, ensure_ascii=False)) + len(P.RESEARCH) > config['max_input_chars']:
                continue
            selected.append(row)
            counts[row['document_id']] = counts.get(row['document_id'], 0) + 1
            if len(selected) >= config['research_candidates']:
                break
        if not selected:
            pending.append('Sem passagens novas pertinentes à consulta; pesquisa encerrada')
            break
        sources.update((s['id'], s) for s in selected)
        seen.update(sources)
        paragraphs = {p['id']: p for s in selected for p in s['paragrafos']}
        payload = dict(schema=VERSION, entrada=base['entrada'], intervencao=intervention,
            anteriores=findings, fontes=selected)
        try:
            result = await calls.call('write', intervention['id'] + '_pesquisa_' + str(turn + 1), payload,
                lambda d: C.research(d, paragraphs), system=P.RESEARCH)
        except (Fatal, BudgetExceeded):
            raise
        except (CallFailure, ValueError) as exc:
            # Uma segunda leitura malsucedida não apaga achados já validados.
            errors.append(dict(intervencao=intervention['id'], etapa='pesquisa', rodada=turn + 1, erro=str(exc)))
            pending.append('Leitura não concluída: ' + str(exc))
            break
        reports.append(result)
        for finding in result['achados']:
            if finding['pertinencia'] != 'direta':
                continue
            if any(digest({k: v for k, v in old.items() if k != 'id'}) == digest(finding) for old in findings):
                continue
            findings.append(dict(id=intervention['id'] + '_A' + str(len(findings) + 1).zfill(2), **finding))
        pending.extend(result['pendencias'])
        if result['suficiente'] and findings:
            break
        pairs = result['consultas_adicionais']
    status = 'com_achados' if findings else 'sem_evidencia_pertinente' if reports else 'sem_passagens' if done_queries else 'nao_executada'
    if errors:
        status = 'parcial' if findings else 'falha_leitura'
    if not findings:
        pending.append('Não foi obtida evidência diretamente pertinente ao objetivo: ' + status)
    return dict(id=intervention['id'], status=status, achados=findings, fontes=list(sources.values()),
                consultas=traces, leituras=len(reports), pendencias=sorted(set(pending)), erros=errors)


def evidence_payload(research):
    """Somente fontes citadas em achados entram na redação e na revisão."""
    used = {p for r in research.values() for f in r['achados'] for p in f['citacoes']}
    sources = {s['id']: s for r in research.values() for s in r['fontes']
               if any(p['id'] in used for p in s['paragrafos'])}
    return list(sources.values())
