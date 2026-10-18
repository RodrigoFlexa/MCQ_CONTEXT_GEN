"""Um tópico: pesquisa nos corpus, documentos técnicos revisados e, opcionalmente, QA."""
import argparse
import csv
import json
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pipeline.inventario.llm import BudgetExceeded, CallBudget, CallFailed, ContentFiltered, LLMClient, load_dotenv
from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, norm, read_json, read_jsonl, sha, write_jsonl
from pipeline.qa_v11.examples import ExampleBank
from pipeline.qa_v11.retrieval import CorpusIndex, file_hash, source_files
from . import VERSION
from .engine import Engine, ScopeExceeded
from .qa import generate

ROOT = Path(__file__).resolve().parents[2]
ORIGINS = ['pipeline/inventario/' + x for x in (
    'saida_sistemas_de_lastro_v4_notas', 'saida_mais_4_topicos_v4_nano_low', 'saida_ultimos_5_topicos_v4_nano_low')]


def log(message):
    print(time.strftime('%H:%M:%S') + ' ' + message, flush=True)


def parse(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--origens', nargs='+', default=ORIGINS)
    p.add_argument('--topico', default='Operação de Tanques de Carga')
    p.add_argument('--saida', required=True)
    p.add_argument('--etapa', choices=('documentos', 'completo'), default='completo')
    p.add_argument('--documentos', type=int, default=10, help='Número de pautas pesquisadas, sem garantir aprovação')
    p.add_argument('--questoes', type=int, default=10, help='Meta de questões aprovadas automaticamente')
    p.add_argument('--max-candidatas', type=int, default=40)
    p.add_argument('--max-pesquisas', type=int, default=4, help='Rodadas de busca por documento, incluindo complementos')
    p.add_argument('--max-fontes', type=int, default=32)
    p.add_argument('--trechos-por-busca', type=int, default=5)
    p.add_argument('--max-refinamentos', type=int, default=1)
    p.add_argument('--max-refinamentos-qa', type=int, default=1)
    p.add_argument('--max-chamadas', type=int, default=400, help='Teto cumulativo global, incluindo reparos')
    p.add_argument('--max-chamadas-documento', type=int, default=24)
    p.add_argument('--max-chamadas-questao', type=int, default=20)
    p.add_argument('--cache-dir', default='pipeline/documentos_tecnicos/cache_compartilhado')
    p.add_argument('--indice-dir', default='pipeline/qa_v11/cache_compartilhado/indice')
    p.add_argument('--manifest')
    for role in ('pesquisador', 'revisor', 'refinador'):
        p.add_argument('--' + role, default='gpt-5-4-petrobras:low')
    p.add_argument('--respondente', default='gpt-5-2-petrobras:low')
    p.add_argument('--novidade', default='gpt-5-4-nano-petrobras:low')
    p.add_argument('--provider', choices=('azure', 'openai'), default='azure')
    p.add_argument('--exemplos-externos', default='pipeline/qa_references/data/qa_examples_v11.jsonl')
    p.add_argument('--pareceres', default='pipeline/qa_references/review/questoes_revisadas_classificadas.jsonl')
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--revisitar-pendentes', action='store_true', help='Reabre documentos pendentes/insuficientes após ampliar limites')
    p.add_argument('--plan', action='store_true', help='Inspeciona pautas sem API, download ou indexação')
    a = p.parse_args(argv)
    for key in ('documentos', 'questoes', 'max_candidatas', 'max_pesquisas', 'max_fontes',
                'trechos_por_busca', 'max_chamadas', 'max_chamadas_documento', 'max_chamadas_questao'):
        if getattr(a, key) < 1:
            p.error(f'--{key.replace("_", "-")} deve ser positivo')
    for key in ('max_refinamentos', 'max_refinamentos_qa'):
        if getattr(a, key) < 0:
            p.error(f'--{key.replace("_", "-")} deve ser >= 0')
    if a.max_candidatas < a.questoes:
        p.error('--max-candidatas deve ser >= --questoes')
    for role in ('pesquisador', 'revisor', 'refinador', 'respondente', 'novidade'):
        model = getattr(a, role).rsplit(':', 1)
        if len(model) != 2 or not model[0] or model[1] not in ('none', 'low', 'medium', 'high'):
            p.error(f'--{role}: use deployment:low|medium|high|none')
    out = Path(a.saida).resolve()
    # Índice e caches devem ser disjuntos da saída, em ambas as direções.
    protected = [Path(v).resolve() for v in a.origens + [a.cache_dir, a.indice_dir]]
    for path in protected:
        if path == out or path in out.parents or out in path.parents:
            p.error(f'Saída deve ser separada de entradas, índice e caches: {path}')
    if a.manifest and not Path(a.manifest).is_file():
        p.error('Manifesto informado não existe')
    if a.manifest:
        corpus_dir = Path(a.manifest).resolve().parent
        if out == corpus_dir or corpus_dir in out.parents or out in corpus_dir.parents:
            p.error('Saída deve ser separada do corpus bruto')
    return a


def load_briefs(args):
    target = norm(args.topico)
    if target == 'operacao de tanques de carga e lastro':
        target = 'operacao de tanques de carga'
    matches = []
    for origin in args.origens:
        for path in sorted(Path(origin).glob('subtopicos/*/assuntos.json')):
            data = read_json(path)
            sub = data['subtopico']
            name = norm(sub['subtopico'])
            if name == target or name.startswith(target):
                matches.append((path, data))
    if len(matches) != 1:
        raise ValueError(f'--topico deve identificar exatamente um subtópico: {len(matches)} encontrados')
    path, data = matches[0]
    sub = data['subtopico']
    subjects = [s for s in data['assuntos'] if not s.get('generico')]
    if len(subjects) < args.documentos:
        raise ValueError(f'Só há {len(subjects)} pautas não genéricas no inventário; reduza --documentos')
    briefs = [{'id': f'D{i:02d}-' + sha(sub['key'] + ':' + s['id'], 12),
               'topico': sub['topico'], 'subtopico': sub['subtopico'],
               'assunto': s['texto'], 'consulta_pt': s.get('consulta_pt', ''),
               'consulta_en': s.get('consulta_en', ''),
               'termos': s.get('termos_pt', []) + s.get('termos_en', []),
               'origem_pauta': path.as_posix(), 'assunto_id': s['id']}
              for i, s in enumerate(subjects[:args.documentos], 1)]
    return sub, briefs, path


def snapshots(out, directory):
    return [read_json(p) for p in sorted((out / directory).glob('*.json'))]


def write_reading(out, document):
    body = document.get('documento')
    if not body:
        return
    lines = ['# ' + body['titulo'], '',
             f"Estado automático: {document['status']}. Validação humana pendente.", '',
             body['texto_markdown'], '', '## Fontes consultadas e citadas', '']
    sources = {e['id']: e for e in document['evidencias']}
    for eid in body['fontes']:
        e = sources[eid]
        meta = e['metadados']
        location = ', '.join(f'{key}={meta[key]}' for key in ('page_ini', 'page_fim', 'linha_ini', 'linha_fim')
                             if meta.get(key) is not None) or 'sem localização confiável'
        lines.append(f"- [{eid}] {meta.get('title') or e.get('documento_id')}; "
                     f"{meta.get('collection')}; {location}; {meta.get('url') or 'URL não disponível'}")
    if document['status'] != 'aprovado':
        lines += ['', '## Pendências', '', document.get('motivo') or document.get('erro') or 'Consulte o histórico.']
    folder = out / 'leitura'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / (document['id'] + '.md')).write_text('\n'.join(lines) + '\n', encoding='utf-8')


def report(out, args, error=None):
    docs, questions = snapshots(out, 'documentos'), snapshots(out, 'questoes')
    logs = read_jsonl(out / 'chamadas_llm.jsonl')
    approved = [q for q in questions if q['status'] == 'aprovada']
    good_docs = [d for d in docs if d['status'] == 'aprovado']
    usage = defaultdict(lambda: Counter())
    for row in logs:
        u = usage[row['tag']]
        u['tentativas'] += 1
        u['respostas_validas'] += row.get('ok') is True
        u['falhas_validacao'] += row.get('kind') == 'validacao'
        u['prompt_tokens'] += row.get('prompt_tokens', 0)
        u['completion_tokens'] += row.get('completion_tokens', 0)
    reached = len(good_docs) >= args.documentos and (args.etapa == 'documentos' or len(approved) >= args.questoes)
    summary = {'version': VERSION, 'topico': args.topico, 'etapa': args.etapa,
               'documentos': dict(Counter(d['status'] for d in docs)),
               'questoes': dict(Counter(q['status'] for q in questions)),
               'meta_documentos': args.documentos, 'meta_questoes': args.questoes if args.etapa == 'completo' else 0,
               'metas_atingidas': reached, 'tentativas_api': len(logs), 'uso_por_etapa': dict(usage),
               'tokens_totais': sum(r.get('prompt_tokens', 0) + r.get('completion_tokens', 0) for r in logs),
               'erro_ou_interrupcao': error, 'fontes': read_json(Path(args.indice_dir) / 'indice.json'),
               'validacao_humana': 'pendente; aprovação automática não substitui revisão de especialista',
               'modelos': {role: getattr(args, role) for role in
                           ('pesquisador', 'revisor', 'refinador', 'respondente', 'novidade')}}
    atomic_json(out / 'resumo.json', summary)
    write_jsonl(out / 'documentos_aprovados.jsonl', good_docs)
    write_jsonl(out / 'questoes_todas.jsonl', questions)
    write_jsonl(out / 'questoes_aprovadas.jsonl', approved)
    index = ['# Documentos técnicos', '', 'Aprovação automática; validação humana pendente.', '']
    for d in docs:
        write_reading(out, d)
        title = d.get('documento', {}).get('titulo', d['pauta']['assunto'])
        if d.get('documento'):
            index.append(f"- [{title}](leitura/{d['id']}.md) — {d['status']}")
        else:
            index.append(f"- {title} — {d['status']}: {d.get('motivo') or d.get('erro', '')}")
    (out / 'documentos.md').write_text('\n'.join(index) + '\n', encoding='utf-8')
    lines = ['# Questões aprovadas automaticamente', '', 'Validação humana pendente.', '']
    for q in approved:
        lines += [f"## {q['id']} — {q['competencia']}", '', q['pergunta'], '',
                  '**Resposta:** ' + q['resposta'], '', '**Explicação:** ' + q['explicacao'], '',
                  '**Rubrica:** ' + '; '.join(q['rubrica']), '', '**Documento:** ' + q['documento_id'], '']
    (out / 'questoes.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    # Uma versão alterada recebe outra identidade; rótulos humanos antigos não são reaplicados.
    review_path = out / 'revisao_humana.csv'
    old = {}
    if review_path.exists():
        with review_path.open(encoding='utf-8-sig', newline='') as stream:
            old = {r['id_revisao']: r for r in csv.DictReader(stream)}
    columns = ['id_revisao', 'id', 'status_automatico', 'pergunta', 'resposta', 'rubrica',
               'veredito_humano', 'comentario']
    with review_path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for q in questions:
            text = q.get('questao', {})
            if text.get('status') != 'ok':
                continue
            rid = sha(json.dumps([q['id'], text], sort_keys=True, ensure_ascii=False), 20)
            human = old.get(rid, {})
            writer.writerow({'id_revisao': rid, 'id': q['id'], 'status_automatico': q['status'],
                             'pergunta': text['pergunta'], 'resposta': text['resposta'],
                             'rubrica': '; '.join(text['rubrica']),
                             'veredito_humano': human.get('veredito_humano', ''),
                             'comentario': human.get('comentario', '')})
    return summary


def failure(path, identifier, exc):
    state = read_json(path) or {'id': identifier}
    state.update(status='limite_unidade' if isinstance(exc, ScopeExceeded) else 'falha_execucao',
                 erro=f'{type(exc).__name__}: {str(exc)[:800]}')
    atomic_json(path, state)


def main(argv=None):
    args = parse(argv)
    sub, briefs, topic_path = load_briefs(args)
    plan = {'version': VERSION, 'subtopico': sub['subtopico'], 'etapa': args.etapa,
            'pautas': briefs, 'meta_questoes_aprovadas': args.questoes if args.etapa == 'completo' else 0,
            'max_candidatas': args.max_candidatas, 'max_chamadas': args.max_chamadas,
            'manifesto': args.manifest, 'usa_rede_no_plano': False}
    if args.plan:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    load_dotenv(ROOT)
    out, cache = Path(args.saida).resolve(), Path(args.cache_dir).resolve()
    # Modelo, prompts, entradas e dependências entram na assinatura; limites podem aumentar.
    adjustable = {'saida', 'cache_dir', 'indice_dir', 'plan', 'revisitar_pendentes', 'documentos',
                  'questoes', 'max_candidatas', 'max_pesquisas', 'max_fontes', 'max_refinamentos',
                  'max_refinamentos_qa', 'max_chamadas', 'max_chamadas_documento', 'max_chamadas_questao'}
    identity = {k: v for k, v in vars(args).items() if k not in adjustable}
    implementation_paths = sorted(Path(__file__).parent.glob('*.py')) + [
        ROOT / 'pipeline/inventario/llm.py', ROOT / 'pipeline/inventario/textutil.py',
        ROOT / 'pipeline/inventario/locking.py', ROOT / 'pipeline/qa_v11/retrieval.py',
        ROOT / 'pipeline/qa_v11/contracts.py', ROOT / 'pipeline/qa_v11/examples.py',
        ROOT / 'pipeline/qa_v11/prompts.py', ROOT / 'azure_openai_backend.py',
        ROOT / 'pipeline/qa_references/download_qa_examples.py',
        ROOT / 'pipeline/domain_corpora/manifest.py', ROOT / 'pipeline/inventario/varredura.py']
    implementation = [[p.relative_to(ROOT).as_posix(), file_hash(p)] for p in implementation_paths]
    inputs = list(dict.fromkeys(source_files(args.origens) + [topic_path]))
    if args.manifest:
        inputs.append(Path(args.manifest))
    if args.etapa == 'completo':
        inputs += [Path(args.exemplos_externos), Path(args.pareceres)]
    fingerprints = [[p.as_posix(), file_hash(p)] for p in inputs]
    signature = sha(json.dumps([identity, implementation, fingerprints], sort_keys=True), 40)
    clients, error, interrupted = {}, None, False
    with output_lock(out):
        config = read_json(out / 'run_config.json')
        if config and config['assinatura'] != signature:
            raise ValueError('Código, fontes ou condição mudaram. Use outra pasta de saída para não misturar versões.')
        if not config and any(p.name != '.run.lock' for p in out.iterdir()):
            raise ValueError('Saída não vazia sem assinatura; escolha outra pasta')
        config = config or {'assinatura': signature, 'version': VERSION, 'implementacao': implementation,
                            'fontes': fingerprints, 'execucoes': []}
        config['execucoes'].append({'at': datetime.now(timezone.utc).isoformat(), 'args': vars(args)})
        atomic_json(out / 'run_config.json', config)
        atomic_json(out / 'pautas.json', plan)
        if report(out, args)['metas_atingidas']:
            log('Metas já atingidas nesta saída; artefatos preservados, sem novas chamadas.')
            return 0
        try:
            if args.provider == 'azure':
                from azure_openai_backend import AzureSettings
                AzureSettings.load().require()
            examples = ExampleBank(args.pareceres, args.exemplos_externos, args.seed) if args.etapa == 'completo' else None
            if examples:
                examples.export(out / 'referencias_avaliacao')
            index = CorpusIndex(args.indice_dir, args.origens, args.manifest)
            log('Conferindo e preparando índice do acervo; sem chamadas a modelos nesta etapa.')
            with output_lock(args.indice_dir):
                info = index.build()
            log(f"Acervo: {info['chunks']} trechos; cobertura {info['cobertura']}")
            remaining = args.max_chamadas - len(read_jsonl(out / 'chamadas_llm.jsonl'))
            if remaining <= 0:
                raise BudgetExceeded('Teto global cumulativo atingido; amplie --max-chamadas para retomar')
            budget = CallBudget(remaining)
            roles = ['pesquisador', 'revisor', 'refinador']
            if args.etapa == 'completo':
                roles += ['respondente', 'novidade']
            for role in roles:
                model, effort = getattr(args, role).rsplit(':', 1)
                clients[role] = LLMClient(model, None if effort == 'none' else effort,
                                          cache / 'llm' / (role + '_' + sha(getattr(args, role)) + '.sqlite3'),
                                          out / 'chamadas_llm.jsonl', provider=args.provider, budget=budget,
                                          max_calls=remaining, max_attempts=2, max_tokens_cap=24000,
                                          response_dir=out / 'respostas_modelos')
            engine = Engine(clients, index, out, args, budget)
            for brief in briefs:
                path = out / 'documentos' / (brief['id'] + '.json')
                stored = read_json(path)
                if args.revisitar_pendentes and stored and stored['status'] in ('pendente_revisao', 'insuficiente'):
                    stored.update(status='em_andamento', etapa='pesquisa')
                    atomic_json(path, stored)
                previous = [{'id': d['id'], 'titulo': d['documento']['titulo'],
                             'recorte': d['pauta']['assunto'], 'resumo_exposicao': d['documento']['texto_markdown'][:2200]}
                            for d in snapshots(out, 'documentos') if d['status'] == 'aprovado' and d['id'] != brief['id']]
                log(f"Documento {brief['id']}: {brief['assunto']}")
                try:
                    doc = engine.process_document(brief, previous)
                    log(f"Documento {brief['id']}: {doc['status']}")
                except (ScopeExceeded, CallFailed, ContentFiltered) as exc:
                    failure(path, brief['id'], exc)
                    log(f"Documento {brief['id']}: {type(exc).__name__}: {exc}")
                    if isinstance(exc, CallFailed):
                        # Duas tentativas já falharam; nunca percorre todas as pautas com o mesmo contrato quebrado.
                        raise
                except BudgetExceeded as exc:
                    failure(path, brief['id'], exc)
                    raise
                except Exception as exc:
                    failure(path, brief['id'], exc)
                    raise
                finally:
                    report(out, args)
            if args.etapa == 'completo':
                approved_docs = [d for d in snapshots(out, 'documentos') if d['status'] == 'aprovado']
                if not approved_docs:
                    error = 'Nenhum documento aprovado; QA não foi iniciado'
                else:
                    for number in range(1, args.max_candidatas + 1):
                        questions = snapshots(out, 'questoes')
                        if sum(q['status'] == 'aprovada' for q in questions) >= args.questoes:
                            break
                        qid = f'Q{number:03d}'
                        path = out / 'questoes' / (qid + '.json')
                        old = read_json(path)
                        if old:
                            document = next(d for d in approved_docs if d['id'] == old['documento_id'])
                        else:
                            document = approved_docs[(number - 1) % len(approved_docs)]
                        previous = [q for q in questions if q['id'] != qid]
                        log(f"Questão {qid}, documento {document['id']}")
                        try:
                            q = generate(engine, document, qid, previous, examples)
                            log(f"Questão {qid}: {q['status']}")
                        except (ScopeExceeded, CallFailed, ContentFiltered) as exc:
                            failure(path, qid, exc)
                            log(f"Questão {qid}: {type(exc).__name__}: {exc}")
                            if isinstance(exc, CallFailed):
                                raise
                        except BudgetExceeded as exc:
                            failure(path, qid, exc)
                            raise
                        except Exception as exc:
                            failure(path, qid, exc)
                            raise
                        finally:
                            report(out, args)
        except KeyboardInterrupt:
            error, interrupted = 'Execução interrompida; checkpoints preservados', True
        except BudgetExceeded as exc:
            error = str(exc)
        except Exception as exc:
            error = f'{type(exc).__name__}: {str(exc)[:800]}'
        finally:
            atomic_json(out / 'uso_cache.json', {role: {'cache_hits': client.usage.get('cached', 0),
                                                      'por_etapa': client.usage_by_stage}
                                               for role, client in clients.items()})
            for client in clients.values():
                client.close()
            summary = report(out, args, error)
            if error:
                log('Interrupção: ' + error)
            log(f"Saída: {out}; documentos: {summary['documentos']}; questões: {summary['questoes']}")
    if interrupted:
        return 130
    return 0 if summary['metas_atingidas'] and error is None else 2


if __name__ == '__main__':
    sys.exit(main())
