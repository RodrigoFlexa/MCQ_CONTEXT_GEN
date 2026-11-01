"""CLI de polimento: python -m pipeline.qa_research.polimento."""
import argparse
import asyncio
import json
import shlex
import shutil
from pathlib import Path

from pipeline.domain_corpora.io_utils import file_hash
from pipeline.domain_corpora.manifest import load_manifest
from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.corpus import CorpusIndex
from pipeline.qa_research.v3.runtime import ROOT, Calls, digest, stamp, topic
from . import VERSION, contracts as C, prompts as P
from .documents import load_base, clean, markdown, catalog
from .flow import polish

HERE = Path(__file__).parent
DEFAULT_BASE = ROOT / 'pipeline/qa_research/relatorios/dez_areas_final_v2'
DEFAULT_LEGACY = ROOT / 'pipeline/qa_research/relatorios/dez_areas_v1'
DEFAULT_EXPERT = DEFAULT_BASE / 'revisao_especialista.json'


def configuration(path=HERE / 'piloto.json'):
    config = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    for key in ('workers', 'max_calls', 'request_timeout', 'heartbeat', 'output_tokens', 'retry_tokens',
                'max_input_chars', 'max_interventions', 'batch_size', 'research_candidates',
                'research_rounds', 'retrieval_candidates', 'max_per_document'):
        C.require(type(config.get(key)) is int and config[key] > 0, 'Configuração inteira positiva: ' + key)
    C.require(config['research_rounds'] <= 2 and config['batch_size'] <= 3, 'No máximo duas leituras e três intervenções por lote')
    C.require(config['max_interventions'] <= 12 and config['research_candidates'] <= 12, 'Até doze intervenções/candidatas')
    C.require(config['retry_tokens'] >= config['output_tokens'], 'retry_tokens menor que output_tokens')
    C.require(set(config.get('models', {})) == {'plan', 'write', 'review'}, 'Configure diagnóstico, edição/pesquisa e revisão')
    for value in config['models'].values():
        C.require(isinstance(value, str) and ':' in value and value.rsplit(':', 1)[1] in ('low', 'medium', 'high'), 'Deployment:esforço inválido')
    return config


def all_items():
    from pipeline.fase_3.topicos import TOPICOS
    return [f'{ai:02}_{si:02}' for ai, subjects in enumerate(TOPICOS.values(), 1) for si, _ in enumerate(subjects, 1)]


def report_document(folder, summary):
    lines = ['# Nova edição do contexto — polimento', '', '**Estado:** ' + summary['status'],
        '', 'Base: ' + summary['origem'], '',
        f"Intervenções aprovadas: {summary['intervencoes_aprovadas']} de {summary['intervencoes_planejadas']}.",
        f"Alterações aprovadas: {summary['alteracoes_aprovadas']}.",
        f"Palavras: {summary['palavras_antes']} → {summary['palavras_depois']}.",
        f"Tentativas externas cumulativas: {summary['tentativas']}.",
        'Documento publicado: ' + ('sim' if summary['documento_publicado'] else 'não; leia documento_para_revisao.md') + '.',
        'Elegível para QA: ' + ('sim, sujeito à validação especializada' if summary['qa_elegivel'] else 'não') + '.',
        '', 'A preservação de texto herdado não significa que todas as afirmações anteriores foram verificadas novamente.',
        '', '| Ponto estável | Cobertura | Motivo |', '|---|---|---|']
    lines += ['| ' + r['id'] + ' | ' + r['estado'] + ' | ' + r['motivo'].replace('|', '/') + ' |' for r in summary['cobertura']]
    if summary.get('erro'):
        lines += ['', 'Interrupção: ' + summary['erro']]
    if summary['pendencias']:
        lines += ['', 'Intervenções ainda pendentes:']
        lines += ['', *['- ' + r['id'] + ' (' + r['tipo'] + '): ' + r['objetivo'] for r in summary['pendencias']]]
    lines += ['', 'Pareceres, fontes, comparação antes/depois e decisões estão na pasta da versão: `versoes/' + summary['versao'] + '/`.']
    (folder / 'RELATORIO.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


async def execute(base_root, legacy_root, expert_file, manifest, output, items, config, transport=None):
    output, base_root, legacy_root = Path(output).resolve(), Path(base_root).resolve(), Path(legacy_root).resolve()
    C.require(output != ROOT and output not in ROOT.parents, 'A saída não pode ser raiz/ancestral do projeto')
    for source in (base_root, legacy_root, Path(manifest).resolve().parent):
        C.require(source != output and source not in output.parents and output not in source.parents, 'Saída precisa ficar separada da base e do corpus')
    C.require(items and len(set(items)) == len(items), 'Lista de itens vazia ou repetida')
    # Conferir todo o piloto antes da primeira chamada, incluindo correções herdadas.
    bases = [load_base(base_root, item, legacy_root, expert_file) for item in items]
    m, _ = await asyncio.to_thread(load_manifest, manifest)
    corpus_id = digest(m)
    result = dict(schema=VERSION, status='em_andamento', inicio=stamp(), items=items, documentos={})
    with output_lock(output):
        identity = dict(schema=VERSION, base=str(base_root), legacy=str(legacy_root))
        previous = read_json(output / 'identidade.json')
        C.require(previous is None or previous == identity, 'Origem da coleção mudou; escolha nova saída')
        atomic_json(output / 'identidade.json', identity)
        atomic_json(output / 'resumo_lote.json', result)
        atomic_json(output / 'preparacao_corpus.json', dict(manifest_sha256=file_hash(manifest), corpus=corpus_id,
            errors=m.get('errors', []), discovery=m.get('discovery', {}), collections=[
                {k: c[k] for k in ('id', 'format', 'documents', 'sha256') if k in c} for c in m['collections']]))
        print('[preparação] verificando e indexando o corpus para o lote', flush=True)
        index = CorpusIndex(output / '.local' / 'corpus', manifest=manifest)
        await asyncio.to_thread(index.build)
        active_item = None
        try:
            for base in bases:
                item, folder = base['item'], output / base['item']
                C.require(not folder.is_symlink() and folder.resolve().parent == output, 'Diretório de documento fora da saída')
                active_item = item
                print('\n[documento:' + item + '] ' + base['entrada']['subtopico'], flush=True)
                with output_lock(folder):
                    atomic_json(folder / 'documento_anterior.json', clean(base['documento']))
                    (folder / 'documento_anterior.md').write_text(markdown(base['documento']), encoding='utf-8')
                    atomic_json(folder / 'base.json', dict(origem=base['origem'], fingerprints=base['fingerprints'],
                        protecoes=base['protecoes'], pontos=base['pontos'], resumo_anterior=base['resumo_anterior']))
                    summary = await polish(base, index, corpus_id, config, folder, transport=transport)
                    report_document(folder, summary)
                result['documentos'][item] = summary
                atomic_json(output / 'resumo_lote.json', result)
            result['status'] = 'concluido' if all(r['status'] == 'concluido' for r in result['documentos'].values()) else 'parcial'
        except (KeyboardInterrupt, asyncio.CancelledError):
            result.update(status='interrompido', erro='Interrompido; retomada preserva chamadas concluídas')
        except Exception as exc:
            result.update(status='interrompido', erro=type(exc).__name__ + ': ' + str(exc)[:900])
        finally:
            if active_item is not None and active_item not in result['documentos']:
                saved = read_json(output / active_item / 'resumo.json')
                if saved and saved.get('status') != 'em_andamento':
                    result['documentos'][active_item] = saved
            result['fim'] = stamp()
            atomic_json(output / 'resumo_lote.json', result)
            lines = ['# Polimento dos contextos — lote', '', '**Estado:** ' + result['status'], '',
                '| Documento | Estado | Intervenções aprovadas | QA elegível |', '|---|---|---:|---|']
            lines += [f"| [{item}]({item}/RELATORIO.md) | {r['status']} | {r['intervencoes_aprovadas']} | {'sim' if r['qa_elegivel'] else 'não'} |"
                      for item, r in result['documentos'].items()]
            lines += ['', 'Leia documento_anterior.md, documento_para_revisao.md e versoes/.../comparacao.json por documento.',
                'Nenhuma questão é gerada por este programa.']
            (output / 'RELATORIO.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return result


def collect(output, destination):
    output, destination = Path(output).resolve(), Path(destination).resolve()
    C.require(output != destination and output not in destination.parents and destination not in output.parents, 'Origem e destino da coleta devem ser separados')
    C.require(not destination.exists(), 'Coleta imutável: escolha destino novo')
    with output_lock(output):
        summary = read_json(output / 'resumo_lote.json')
        C.require(summary and summary['status'] != 'em_andamento', 'Aguarde o lote encerrar antes de coletar')
        paths = [output / n for n in ('identidade.json', 'preparacao_corpus.json', 'resumo_lote.json', 'RELATORIO.md')]
        for item, row in summary['documentos'].items():
            folder = output / item
            paths += [folder / name for name in ('base.json', 'resumo.json', 'RELATORIO.md', 'orcamento.json',
                'chamadas_llm.jsonl', 'documento_anterior.json', 'documento_anterior.md',
                'documento_para_revisao.json', 'documento_para_revisao.md', 'documento.json', 'documento.md')]
            paths += list((folder / 'versoes' / row['versao']).glob('*.json'))
        for source in paths:
            if not source.is_file() or source.is_symlink() or source.suffix not in ('.json', '.jsonl', '.md'):
                continue
            target = destination / source.relative_to(output)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        atomic_json(destination / 'manifest_resultados.json', dict(schema=VERSION,
            files={p.relative_to(destination).as_posix(): file_hash(p) for p in destination.rglob('*') if p.is_file()}))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=HERE / 'piloto.json')
    parser.add_argument('--items', nargs='+', help='IDs, ou all para os 40 documentos')
    parser.add_argument('--base', type=Path, default=DEFAULT_BASE)
    parser.add_argument('--legacy', type=Path, default=DEFAULT_LEGACY)
    parser.add_argument('--expert', type=Path, default=DEFAULT_EXPERT)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--output', type=Path, default=Path('pipeline/qa_research/saida_polimento/piloto_3_documentos_01'))
    parser.add_argument('--plan', action='store_true')
    parser.add_argument('--collect', type=Path)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--max-calls', type=int)
    args = parser.parse_args(argv)
    if args.collect:
        collect(args.output, args.collect)
        print('Coleta:', args.collect)
        return 0
    config = configuration(args.config)
    if args.max_calls is not None:
        C.require(args.max_calls > 0, 'Orçamento positivo obrigatório')
        config['max_calls'] = args.max_calls
    config['verbose'] = args.verbose
    items = args.items or config['items']
    if items == ['all']:
        items = all_items()
    if args.plan:
        bases = [load_base(args.base, item, args.legacy, args.expert) for item in items]
        print(json.dumps(dict(items=items, config=config, manifest=str(args.manifest), output=str(args.output),
            documentos=[dict(item=b['item'], blocos=len(catalog(b['documento'])[1]),
                pontos=len(b['pontos']), correcoes_especialista=len(b['protecoes'])) for b in bases]), ensure_ascii=False, indent=2))
        return 0
    C.require(args.manifest is not None, 'Informe --manifest do corpus instalado')
    result = asyncio.run(execute(args.base, args.legacy, args.expert, args.manifest, args.output, items, config))
    print('O código acabou de rodar no terminal 🙂')
    print('Estado real:', result['status'], '|', args.output / 'RELATORIO.md')
    destination = Path('pipeline/qa_research/relatorios') / ('polimento_3_contextos_' + stamp().split('.')[0].replace(':', '').replace('-', ''))
    path = shlex.quote(destination.as_posix())
    print('Comandos de coleta, commit e push:')
    print('"${DOCUMENT_PYTHON:-python3}" -m pipeline.qa_research.polimento --output ' + shlex.quote(args.output.as_posix()) + ' --collect ' + path)
    print('git add -- ' + path)
    print('git commit -m "Resultados do piloto de polimento dos contextos"')
    print('git push origin codex/qa-evidencias-verificadas')
    return 0 if result['status'] == 'concluido' else 2


if __name__ == '__main__':
    raise SystemExit(main())
