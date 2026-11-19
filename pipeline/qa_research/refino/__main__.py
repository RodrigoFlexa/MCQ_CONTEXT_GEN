"""CLI do refino dos contextos: python -m pipeline.qa_research.refino."""
import argparse
import asyncio
import json
import shlex
import shutil
from pathlib import Path

from pipeline.domain_corpora.io_utils import file_hash
from pipeline.inventario.llm import BudgetExceeded
from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.v3.runtime import ROOT, Calls, Fatal, digest, stamp
from . import VERSION, contracts as C, semantica as S, textos as T
from .flow import Refino, concept_map, gap_rows
from .retrieval import Acervo, discover

HERE = Path(__file__).parent
DEFAULT_LEGACY = ROOT / 'pipeline/qa_research/relatorios/dez_areas_v1'
INT_KEYS = ('workers', 'max_calls', 'request_timeout', 'heartbeat', 'output_tokens', 'retry_tokens', 'max_input_chars',
            'min_sections', 'max_sections', 'min_claims', 'max_claims', 'research_rounds', 'retrieval_candidates',
            'read_candidates', 'max_per_document', 'max_passage_chars', 'consolidation_rounds')
ROLES = {'plan', 'draft', 'read', 'consolidate', 'write', 'edit', 'review'}


def configuration(path):
    config = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    for key in INT_KEYS:
        C.require(type(config.get(key)) is int and config[key] > 0, 'Configuração inteira positiva: ' + key)
    C.require(config['min_sections'] <= config['max_sections'], 'min_sections > max_sections')
    C.require(config['retry_tokens'] >= config['output_tokens'], 'retry_tokens menor que output_tokens')
    C.require(set(config.get('models', {})) == ROLES, 'Configure os papéis: ' + ', '.join(sorted(ROLES)))
    for value in config['models'].values():
        C.require(isinstance(value, str) and ':' in value and value.rsplit(':', 1)[1] in ('low', 'medium', 'high'),
                  'Use deployment:esforço (low, medium, high)')
    from .prompts import PERSPECTIVAS
    writers = config.get('writers')
    C.require(isinstance(writers, list) and writers, 'Informe ao menos um redator')
    C.require(all(w.get('perspectiva') in PERSPECTIVAS and C.ID.match(w.get('id', '')) for w in writers),
              'Redator: id seguro e perspectiva em ' + ', '.join(PERSPECTIVAS))
    C.require(len({w['id'] for w in writers}) == len(writers), 'IDs de redator repetidos')
    C.require(0 < config['redundancy_threshold'] < 1, 'redundancy_threshold entre 0 e 1')
    for key in ('allow_values_without_source', 'evaluate_base'):
        C.require(type(config.get(key)) is bool, key + ' booleano')
    sem = config.get('semantic')
    C.require(sem is None or (isinstance(sem, dict) and isinstance(sem.get('deployment'), str)
              and type(sem.get('dimensions')) is int and 0 < sem.get('threshold', 0) < 1),
              'semantic: null ou {deployment, dimensions, threshold}')
    return config


def load_entradas(folder):
    folder = Path(folder)
    index = json.loads((folder / 'indice.json').read_text(encoding='utf-8'))
    out = {}
    for row in index['documentos']:
        path = folder / f"{row['id']}.json"
        C.require(file_hash(path) == row['sha256'], 'Entrada alterada sem regenerar indice.json: ' + path.name)
        out[row['id']] = json.loads(path.read_text(encoding='utf-8'))
    return out


def finished_texts(output, items):
    """Sentenças dos documentos já refinados nesta saída, para a redundância entre documentos."""
    texts = {}
    for item in items:
        doc = read_json(Path(output) / item / 'documento.json')
        if doc:
            texts[item] = [s for _, _, t in T.blocks_of(doc) for s in T.sentences(t)]
    return texts


async def execute(entradas, items, manifests, output, config, cache, legacy, mapa_file=None, transport=None):
    output = Path(output).resolve()
    C.require(output != ROOT and output not in ROOT.parents, 'A saída não pode ser a raiz do projeto')
    selected = [entradas[i] for i in items]
    result = dict(schema=VERSION, status='em_andamento', inicio=stamp(), items=items, documentos={})
    with output_lock(output):
        identity = dict(schema=VERSION, entradas={k: digest(v) for k, v in sorted(entradas.items())})
        previous = read_json(output / 'identidade.json')
        C.require(previous is None or previous == identity, 'Entradas mudaram; escolha nova saída')
        atomic_json(output / 'identidade.json', identity)
        print('[preparação] verificando e indexando os corpora (o índice fica em cache)', flush=True)
        acervo = await asyncio.to_thread(Acervo.from_manifests, manifests, cache, config.get('index_workers'))
        atomic_json(output / 'preparacao_corpus.json', dict(indices=acervo.info))
        cfg = dict(config, verbose=config.get('verbose', False))
        try:
            if mapa_file:
                mapa = json.loads(Path(mapa_file).read_text(encoding='utf-8'))
                C.mapa(mapa, list(entradas))
            else:
                calls = Calls(output / '_mapa', dict(cfg, max_calls=4), transport=transport)
                try:
                    mapa = await concept_map(list(entradas.values()), calls, cfg)
                finally:
                    await calls.close()
            atomic_json(output / 'mapa_conceitos.json', mapa)
            for entrada in selected:
                item = entrada['id']
                folder = output / item
                print(f'\n[documento:{item}] {entrada["titulo"]}', flush=True)
                previous_doc = read_json(folder / 'resumo.json')
                if previous_doc and previous_doc.get('status') == 'concluido' and (folder / 'documento.json').is_file():
                    print(f'[documento:{item}] já concluído nesta saída; mantido', flush=True)
                    result['documentos'][item] = previous_doc
                    continue
                local = await asyncio.to_thread(acervo.with_inherited, Path(legacy) / item / 'evidencias_citadas.jsonl', cache)
                calls = Calls(folder, cfg, transport=transport)
                try:
                    with output_lock(folder):
                        # Só os anteriores na ordem do lote: a retomada recebe a mesma entrada.
                        others = finished_texts(output, items[:items.index(item)])
                        summary = await Refino(entrada, local, calls, cfg, folder, mapa, others).run()
                except (Fatal, KeyboardInterrupt, asyncio.CancelledError):
                    raise
                except BudgetExceeded as exc:
                    summary = read_json(folder / 'resumo.json') or dict(item=item)
                    summary.update(status='parcial', erro='Orçamento do documento atingido: ' + str(exc))
                    atomic_json(folder / 'resumo.json', summary)
                except Exception as exc:
                    summary = read_json(folder / 'resumo.json') or dict(item=item)
                    summary.update(status='parcial', erro=type(exc).__name__ + ': ' + str(exc)[:900])
                    atomic_json(folder / 'resumo.json', summary)
                finally:
                    await calls.close()
                if summary.get('status') == 'concluido' and config.get('limpar_local', True):
                    freed = clean_local(folder)
                    print(f'[documento:{item}] cache local apagado ({freed / 2**20:.0f} MB)', flush=True)
                result['documentos'][item] = summary
                atomic_json(output / 'resumo_lote.json', result)
            result['status'] = 'concluido' if all(r.get('status') == 'concluido' for r in result['documentos'].values()) else 'parcial'
        except (KeyboardInterrupt, asyncio.CancelledError):
            result.update(status='interrompido', erro='Interrompido; a retomada reaproveita as chamadas concluídas')
        except Exception as exc:
            result.update(status='interrompido', erro=type(exc).__name__ + ': ' + str(exc)[:900])
        finally:
            result['fim'] = stamp()
            result['lote'] = batch_metrics(output, entradas, items, config['redundancy_threshold'], config.get('semantic'))
            atomic_json(output / 'resumo_lote.json', result)
            (output / 'RELATORIO.md').write_text(batch_report(result), encoding='utf-8')
    return result


def batch_metrics(output, entradas, items, threshold, spec=None):
    base, new = {}, {}
    rows = []
    for item in items:
        m = read_json(Path(output) / item / 'metricas.json')
        if m:
            rows.append(m)
        b = read_json(Path(output) / item / 'documento_base.json')
        n = read_json(Path(output) / item / 'documento.json')
        if b and n:
            base[item], new[item] = b, n
    if not rows:
        return {}
    sem_before = sem_after = None
    if spec:
        sem_before = S.cross({i: S.load_vectors(Path(output) / i, spec, 'documento_base.json') for i in base}, spec['threshold'])
        sem_after = S.cross({i: S.load_vectors(Path(output) / i, spec, 'documento.json') for i in new}, spec['threshold'])
    cross_before = T.cross_redundancy(base, threshold) if len(base) > 1 else {}
    cross_after = T.cross_redundancy(new, threshold) if len(new) > 1 else {}
    total = lambda side, key: sum(m[side][key] for m in rows)
    mean = lambda values: round(sum(values) / len(values), 4) if values else None
    cov = lambda side: [m['cobertura'][side] for m in rows if m['cobertura'][side]]
    return dict(documentos=len(rows), palavras_antes=total('antes', 'palavras'), palavras_depois=total('depois', 'palavras'),
        redundancia_media_antes=mean([m['antes']['taxa_redundancia'] for m in rows]),
        redundancia_media_depois=mean([m['depois']['taxa_redundancia'] for m in rows]),
        redundancia_entre_documentos_antes=cross_before, redundancia_entre_documentos_depois=cross_after,
        parafrase_entre_documentos_antes=sem_before, parafrase_entre_documentos_depois=sem_after,
        lacunas_atendidas_antes=sum(c['atendido'] for c in cov('antes')), lacunas_atendidas_depois=sum(c['atendido'] for c in cov('depois')),
        lacunas_parciais_antes=sum(c['parcial'] for c in cov('antes')), lacunas_parciais_depois=sum(c['parcial'] for c in cov('depois')),
        lacunas_total=sum(len(gap_rows(entradas[m['item']])) for m in rows),
        unidades_por_estatuto={k: sum(m['proveniencia']['por_estatuto'].get(k, 0) for m in rows)
                               for k in ('evidencia', 'base_revisada', 'consenso_modelos', 'modelo')},
        chamadas=sum(m['chamadas_reservadas'] for m in rows))


def batch_report(result):
    lines = ['# Refino dos contextos: lote', '', f"**Estado:** {result['status']}", '',
             '| Documento | Estado | Palavras (antes → depois) | Redundância (antes → depois) | Lacunas atendidas (antes → depois) |',
             '|---|---|---|---|---|']
    for item, s in result['documentos'].items():
        m = s.get('metricas') or {}
        a, d, cov = m.get('antes'), m.get('depois'), m.get('cobertura', {})
        ca, cd = cov.get('antes'), cov.get('depois')
        words = f"{a['palavras']} → {d['palavras']}" if a and d else '-'
        red = f"{a['taxa_redundancia']:.1%} → {d['taxa_redundancia']:.1%}" if a and d else '-'
        gaps = f"{ca['atendido'] if ca else '-'} → {cd['atendido'] if cd else '-'} de {(cd or ca or {}).get('total', '-')}"
        lines.append(f"| [{item}]({item}/RELATORIO.md) | {s.get('status')} | {words} | {red} | {gaps} |")
    lote = result.get('lote') or {}
    if lote:
        lines += ['', f"Redundância média dentro do documento: {lote['redundancia_media_antes']} → {lote['redundancia_media_depois']}.",
                  f"Redundância entre documentos (fração de sentenças com quase-duplicata em outro documento do lote): "
                  f"{lote['redundancia_entre_documentos_antes']} → {lote['redundancia_entre_documentos_depois']}.",
                  f"Unidades por origem: {lote['unidades_por_estatuto']}. Chamadas reservadas: {lote['chamadas']}."]
    if result.get('erro'):
        lines += ['', '**Erro:** ' + result['erro']]
    lines += ['', 'Nenhuma questão é gerada por este programa. A QA continua apontando para a versão anterior até decisão explícita.']
    return '\n'.join(lines) + '\n'


def clean_local(folder):
    """Apaga .local (respostas brutas, cache de chamadas e embeddings) de um documento concluído."""
    local = Path(folder) / '.local'
    if not local.is_dir():
        return 0
    size = sum(p.stat().st_size for p in local.rglob('*') if p.is_file())
    shutil.rmtree(local, ignore_errors=True)
    return size


def collect(output, destination, remove=False):
    output, destination = Path(output).resolve(), Path(destination).resolve()
    C.require(output != destination and output not in destination.parents and destination not in output.parents,
              'Origem e destino da coleta devem ser separados')
    C.require(not destination.exists(), 'Coleta imutável: escolha destino novo')
    with output_lock(output):
        summary = read_json(output / 'resumo_lote.json')
        C.require(summary and summary['status'] != 'em_andamento', 'Aguarde o lote encerrar antes de coletar')
        for source in sorted(output.rglob('*')):
            rel = source.relative_to(output)
            if (not source.is_file() or source.is_symlink() or rel.parts[0] in ('.local',) or '.local' in rel.parts
                    or source.suffix not in ('.json', '.jsonl', '.md') or source.name == '.run.lock'):
                continue
            target = destination / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        atomic_json(destination / 'manifest_resultados.json', dict(schema=VERSION,
            files={p.relative_to(destination).as_posix(): file_hash(p) for p in destination.rglob('*') if p.is_file()}))
    if remove:
        C.require(summary['status'] == 'concluido', 'Só apago a saída de um lote concluído (a retomada precisa dela)')
        shutil.rmtree(output)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=HERE / 'config_piloto.json')
    parser.add_argument('--items', nargs='+', help='IDs (ex.: 02_06 02_08) ou all')
    parser.add_argument('--entradas', type=Path, default=HERE / 'entradas')
    parser.add_argument('--manifest', nargs='+', default=['auto'],
                        help='Manifestos dos corpora; "auto" usa todos os prontos em dataset/ (padrão)')
    parser.add_argument('--index-cache', type=Path, default=ROOT / 'dataset/indices_refino')
    parser.add_argument('--legacy', type=Path, default=DEFAULT_LEGACY)
    parser.add_argument('--mapa', type=Path, help='mapa_conceitos.json de execução anterior, para manter os mesmos donos')
    parser.add_argument('--output', type=Path, default=Path('pipeline/qa_research/saida_refino/piloto_01'))
    parser.add_argument('--plan', action='store_true')
    parser.add_argument('--collect', type=Path)
    parser.add_argument('--apagar-saida', action='store_true',
                        help='Com --collect: apaga a pasta de saída depois da coleta (só lote concluído)')
    parser.add_argument('--manter-local', action='store_true',
                        help='Não apagar o cache .local dos documentos concluídos')
    parser.add_argument('--max-calls', type=int, help='Teto de chamadas por documento')
    parser.add_argument('--workers', type=int, help='Chamadas simultâneas ao modelo (sobrepõe a configuração)')
    parser.add_argument('--index-workers', type=int, help='Processos para construir os índices (padrão: núcleos - 1, até 16)')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args(argv)
    if args.collect:
        collect(args.output, args.collect, args.apagar_saida)
        print(f'Coleta: {args.collect}' + (' | saída apagada' if args.apagar_saida else ''))
        return 0
    config = configuration(args.config)
    if args.max_calls is not None:
        C.require(args.max_calls > 0, 'Orçamento positivo obrigatório')
        config['max_calls'] = args.max_calls
    config['verbose'] = args.verbose
    if args.manter_local:
        config['limpar_local'] = False
    if args.workers is not None:
        C.require(args.workers > 0, '--workers positivo')
        config['workers'] = args.workers
    if args.index_workers is not None:
        C.require(args.index_workers > 0, '--index-workers positivo')
        config['index_workers'] = args.index_workers
    entradas = load_entradas(args.entradas)
    items = args.items or config['items']
    if items == ['all']:
        items = sorted(entradas)
    C.require(items and len(set(items)) == len(items) and set(items) <= set(entradas), 'Itens vazios, repetidos ou desconhecidos')
    manifests, notes = discover(ROOT, args.manifest)
    if args.plan:
        sections = (config['min_sections'] + config['max_sections']) // 2
        per_doc = 1 + 2 + sections * (len(config['writers']) + config['research_rounds'] + 2) + config['consolidation_rounds'] + sections
        print(json.dumps(dict(items=items, output=str(args.output), manifestos=notes, cache=str(args.index_cache),
            documentos=[dict(item=i, titulo=entradas[i]['titulo'], blocos_base=sum(len(c['blocos']) for c in entradas[i]['base']['capitulos']),
                             lacunas=len(gap_rows(entradas[i])), removidos=len(entradas[i]['removidos'])) for i in items],
            chamadas_estimadas_por_documento=f'~{per_doc} (teto {config["max_calls"]})', config=config),
            ensure_ascii=False, indent=2))
        return 0
    C.require(manifests, 'Nenhum manifesto de corpus pronto. Instale os corpora ou informe --manifest')
    result = asyncio.run(execute(entradas, items, manifests, args.output, config, args.index_cache, args.legacy, args.mapa))
    print('O código acabou de rodar no terminal 🙂')
    print('Estado real:', result['status'], '|', args.output / 'RELATORIO.md')
    destination = Path('pipeline/qa_research/relatorios') / ('refino_contextos_' + stamp().split('.')[0].replace(':', '').replace('-', ''))
    path = shlex.quote(destination.as_posix())
    print('Comandos de coleta, commit e push:')
    print('"${DOCUMENT_PYTHON:-python3}" -m pipeline.qa_research.refino --output ' + shlex.quote(args.output.as_posix()) + ' --collect ' + path
          + (' --apagar-saida' if result['status'] == 'concluido' else ''))
    print('git add -- ' + path)
    print('git commit -m "Resultados do refino dos contextos"')
    print('git push origin codex/qa-evidencias-verificadas')
    return 0 if result['status'] == 'concluido' else 2


if __name__ == '__main__':
    raise SystemExit(main())
