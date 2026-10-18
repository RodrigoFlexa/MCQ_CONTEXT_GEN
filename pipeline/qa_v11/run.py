"""Piloto v11 e ablações: evidência direta, nota, nota com complemento. Execute no servidor."""
import argparse
import csv
import json
import re
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from pipeline.inventario.llm import LLMClient, CallBudget, BudgetExceeded, CallFailed, ContentFiltered, load_dotenv
from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json, read_jsonl, sha, write_jsonl
from . import VERSION
from .engine import Engine
from .examples import ExampleBank
from .retrieval import CorpusIndex, file_hash, load_topics, source_files

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ORIGINS = ['pipeline/inventario/' + x for x in (
    'saida_sistemas_de_lastro_v4_notas', 'saida_mais_4_topicos_v4_nano_low', 'saida_ultimos_5_topicos_v4_nano_low')]
DEFAULT_TOPICS = ['Operação de Separadores Trifásicos', 'SGSO', 'Operação de Tanques de Carga']


def parse(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--origens', nargs='+', default=DEFAULT_ORIGINS)
    p.add_argument('--subtopicos', nargs='+', default=DEFAULT_TOPICS)
    p.add_argument('--saida', required=True)
    p.add_argument('--cache-dir', default='pipeline/qa_v11/cache_compartilhado')
    p.add_argument('--manifest', help='Manifesto completo instalado; ausente: somente todo o acervo salvo nas origens')
    p.add_argument('--configuracao', choices=('direta', 'nota', 'nota_complemento'), default='nota_complemento')
    p.add_argument('--modo', choices=('cota', 'fixo'), default='cota')
    p.add_argument('--por-topico', type=int, default=10)
    p.add_argument('--max-unidades', type=int, default=20)
    p.add_argument('--max-candidatas', type=int, default=50, help='Limite por subtópico, sem relaxar qualidade')
    p.add_argument('--max-chamadas', type=int, default=900, help='Teto global cumulativo de tentativas de API por saída')
    p.add_argument('--workers', type=int, default=3)
    p.add_argument('--redator', default='gpt-5-4-petrobras:low')
    p.add_argument('--juiz', default='gpt-5-4-petrobras:low')
    p.add_argument('--respondente', default='gpt-5-2-petrobras:low')
    p.add_argument('--novidade', default='gpt-5-4-nano-petrobras:low')
    p.add_argument('--provider', choices=('azure', 'openai'), default='azure')
    p.add_argument('--exemplos-externos', default='pipeline/qa_references/data/qa_examples_v11.jsonl')
    p.add_argument('--pareceres', default='pipeline/qa_references/review/questoes_revisadas_classificadas.jsonl')
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--plan', action='store_true', help='Inspeção de entradas e metas sem rede, clientes ou geração')
    a = p.parse_args(argv)
    for k in ('por_topico', 'max_unidades', 'max_candidatas', 'max_chamadas', 'workers'):
        if getattr(a, k) < 1:
            p.error(f'{k} deve ser positivo')
    if a.max_candidatas < a.por_topico:
        p.error('--max-candidatas deve ser >= --por-topico')
    for name in ('redator', 'juiz', 'respondente', 'novidade'):
        spec = getattr(a, name).rsplit(':', 1)
        if len(spec) != 2 or not spec[0] or spec[1] not in ('none', 'low', 'medium', 'high'):
            p.error(f'--{name}: use deployment:low|medium|high|none')
    out = Path(a.saida).resolve()
    for origin in a.origens:
        src = Path(origin).resolve()
        if out == src or src in out.parents:
            p.error('saída deve ser nova, fora dos inventários de origem')
    if Path(a.cache_dir).resolve() == out or out in Path(a.cache_dir).resolve().parents:
        p.error('use cache compartilhado fora da saída experimental')
    return a


def log(message):
    print(time.strftime('%H:%M:%S') + ' ' + message, flush=True)


def progress(state, args):
    rows = state.get('registros', [])
    completed = [r for r in rows if r.get('status') not in ('falha_execucao', 'pendente_validacao')]
    approved = sum(r['status'] == 'aprovada' for r in rows)
    reached = approved >= args.por_topico if args.modo == 'cota' else (
        len(rows) >= args.por_topico and len(completed) == len(rows))
    return approved, len(rows), reached, len(completed)


def run_topic(engine, topic, args, out, stop):
    key = topic['key']
    state_path = out / 'estados' / (sha(key, 20) + '.json')
    state = read_json(state_path) or {'topico': topic['topico'], 'subtopico': topic['subtopico'],
                                    'sub_key': key, 'registros': [], 'unidades_sem_objetivo': [], 'falhas': []}
    def save():
        atomic_json(state_path, state)
    for unit in topic['unidades']:
        if stop.is_set() or progress(state, args)[2]:
            break
        limit = min(args.max_candidatas, args.por_topico) if args.modo == 'fixo' else args.max_candidatas
        retry_units = {r['unidade'] for r in state['registros'] if r['status'] in ('falha_execucao', 'pendente_validacao')}
        if len(state['registros']) >= limit and not retry_units:
            break
        if len(state['registros']) >= limit and unit['id'] not in retry_units:
            continue
        try:
            log(f"[{topic['subtopico']}] preparando {unit['conceito']}")
            pack = engine.prepare(topic, unit, out / 'unidades')
        except BudgetExceeded:
            stop.set()
            state['interrupcao'] = 'orcamento'
            save()
            return state
        except (CallFailed, ContentFiltered) as exc:
            state['falhas'].append({'unidade': unit['id'], 'etapa': 'preparacao',
                                    'classe': type(exc).__name__, 'motivo': str(exc)[:500]})
            save()
            continue
        objectives = pack['nota']['objetivos']
        if not objectives:
            row = {'unidade': unit['id'], 'motivo': pack['nota'].get('motivo') or 'nenhum objetivo passou pela revisão',
                   'afirmacoes_avaliaveis': sum(a.get('verificacao', {}).get('decisao_uso') == 'avaliavel_no_escopo'
                                               for a in pack['afirmacoes'])}
            if not any(r['unidade'] == unit['id'] for r in state['unidades_sem_objetivo']):
                state['unidades_sem_objetivo'].append(row)
            save()
        for objective in objectives:
            if stop.is_set() or progress(state, args)[2]:
                break
            qid = objective['id'] + ':Q'
            position = next((i for i, q in enumerate(state['registros']) if q['id'] == qid), None)
            if position is not None and state['registros'][position]['status'] not in ('falha_execucao', 'pendente_validacao'):
                continue
            if position is None and len(state['registros']) >= limit:
                break
            previous = state['registros'] if position is None else state['registros'][:position]
            try:
                row = engine.generate_item(pack, objective, previous, qid)
            except BudgetExceeded:
                stop.set()
                state['interrupcao'] = 'orcamento'
                save()
                return state
            except (CallFailed, ContentFiltered) as exc:
                # Jamais transforma falha do juiz/cego/novidade em aprovação.
                checkpoint = read_json(out / 'artefatos_qa' / (sha(qid, 32) + '.json')) or {}
                row = {**checkpoint, 'id': qid, 'objetivo_id': objective['id'], 'objetivo': objective,
                       'unidade': unit['id'], 'status': 'pendente_validacao',
                       'motivo': str(exc)[:500], 'classe_erro': type(exc).__name__, 'validacao_humana': 'pendente'}
            row.update(topico=topic['topico'], subtopico=topic['subtopico'], sub_key=key,
                       configuracao=args.configuracao, ordem=position if position is not None else len(state['registros']))
            if position is None:
                state['registros'].append(row)
            else:
                state['registros'][position] = row
            save()
            approved, attempts, _, _ = progress(state, args)
            log(f"[{topic['subtopico']}] {approved}/{args.por_topico} aprovadas; {attempts} candidatas; {row['status']}")
    state['resultado'] = ('meta_atingida' if progress(state, args)[2] else
                          'limite_candidatas' if len(state['registros']) >= args.max_candidatas else 'fila_esgotada')
    save()
    return state


def collect_states(out):
    return [read_json(p) for p in sorted((out / 'estados').glob('*.json'))]


def report(out, args, started, error=None):
    states = collect_states(out)
    rows = [r for s in states for r in s['registros']]
    good = [r for r in rows if r['status'] == 'aprovada']
    calls = read_jsonl(out / 'chamadas_llm.jsonl')
    summaries = []
    for s in states:
        accepted, attempts, reached, _ = progress(s, args)
        summaries.append({'subtopico': s['subtopico'], 'aprovadas': accepted, 'candidatas': attempts,
                          'meta_aprovadas' if args.modo == 'cota' else 'meta_candidatas': args.por_topico,
                          'meta_atingida': reached, 'status': dict(Counter(r['status'] for r in s['registros'])),
                          'unidades_sem_objetivo': len(s['unidades_sem_objetivo']),
                          'falhas_preparacao': len(s['falhas']), 'encerramento': s.get('interrupcao') or s.get('resultado')})
    total_usage = {'tentativas_api': len(calls), 'prompt_tokens': sum(c.get('prompt_tokens', 0) for c in calls),
                   'completion_tokens': sum(c.get('completion_tokens', 0) for c in calls)}
    stage_usage = {}
    for c in calls:
        usage = stage_usage.setdefault(c.get('tag', ''), Counter())
        usage['tentativas_api'] += 1
        usage['prompt_tokens'] += c.get('prompt_tokens', 0)
        usage['completion_tokens'] += c.get('completion_tokens', 0)
    summary = {'version': VERSION, 'configuracao': args.configuracao, 'modo': args.modo,
               'subtopicos': summaries, 'total_aprovadas_automaticamente': len(good),
               'validacao_humana': 'pendente; aprovação automática não equivale a validação de especialista',
               'metas_atingidas': len(states) == len(args.subtopicos) and all(s['meta_atingida'] for s in summaries),
               'status': dict(Counter(r['status'] for r in rows)), 'uso': total_usage,
               'uso_por_etapa': {k: dict(v) for k, v in stage_usage.items()},
               'cache_nesta_execucao': read_json(out / 'uso_cache.json'),
               'segundos_desta_execucao': round(time.time() - started, 2), 'erro_execucao': error,
               'fontes': read_json(Path(args.cache_dir) / 'indice/indice.json'),
               'modelos': {k: getattr(args, k) for k in ('redator', 'juiz', 'respondente', 'novidade')}}
    write_jsonl(out / 'questoes_todas.jsonl', rows)
    write_jsonl(out / 'questoes_aprovadas.jsonl', good)
    atomic_json(out / 'resumo.json', summary)
    md = ['# QA v11 — ' + args.configuracao, '', 'Aprovação automática; revisão humana pendente.', '',
          '| Subtópico | Aprovadas | Candidatas | Meta atingida |', '|---|---:|---:|---|']
    for s in summaries:
        md.append(f"| {s['subtopico']} | {s['aprovadas']} | {s['candidatas']} | {'sim' if s['meta_atingida'] else 'não'} |")
    for q in good:
        md += ['', '## ' + q['subtopico'] + ' — ' + q['id'], '', q['pergunta'], '',
               '**Resposta:** ' + q['resposta'], '', '**Explicação:** ' + q['explicacao'], '',
               '**Rubrica:** ' + '; '.join(q['rubrica'])]
    (out / 'questoes.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    # Identidades cegas preservam o mapeamento fora do arquivo entregue ao revisor.
    review = out / 'revisao_humana.csv'
    fields = ['id_cego', 'pergunta', 'resposta', 'explicacao', 'rubrica',
              'correta', 'sustentada', 'autonoma', 'competencia', 'sem_pista', 'escopo', 'nao_redundante', 'comentario']
    old_review = {}
    if review.exists():
        with review.open(encoding='utf-8-sig', newline='') as stream:
            old_review = {r['id_cego']: r for r in csv.DictReader(stream)}
    mapping, blind_sources = [], []
    # Inclui também reprovadas e pendentes com texto, para medir descarte indevido.
    samples = sorted([q for q in rows if q.get('pergunta')], key=lambda q: sha(str(args.seed) + q['id'], 40))
    with review.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for q in samples:
            anonymous = sha(str(args.seed) + args.configuracao + q['id'] + q['pergunta'] + q['resposta'], 16)
            human = {k: old_review.get(anonymous, {}).get(k, '') for k in fields}
            human.update(id_cego=anonymous, pergunta=q['pergunta'], resposta=q['resposta'],
                         explicacao=q['explicacao'], rubrica='; '.join(q['rubrica']))
            writer.writerow(human)
            mapping.append({'id_cego': anonymous, 'id': q['id'], 'status_automatico': q['status']})
            blind_sources.append({'id_cego': anonymous, 'evidencias': q.get('evidencias', []),
                                  'nota': 'Textos originais para conferir sustentação; sem parecer automático.'})
    write_jsonl(out / 'mapa_revisao.jsonl', mapping)
    write_jsonl(out / 'evidencias_revisao.jsonl', blind_sources)
    return summary


def main(argv=None):
    args = parse(argv)
    topics = load_topics(args.origens, args.subtopicos, args.max_unidades)
    plan = {'version': VERSION, 'configuracao': args.configuracao, 'modo': args.modo,
            'meta': args.por_topico, 'total_meta': args.por_topico * len(topics),
            'meta_significa': 'aprovadas automaticamente' if args.modo == 'cota' else 'candidatas',
            'unidades_disponiveis': {s['subtopico']: len(s['unidades']) for s in topics},
            'max_candidatas_por_subtopico': args.max_candidatas,
            'max_tentativas_api_global': args.max_chamadas,
            'manifesto': args.manifest, 'exemplos_externos_presentes': Path(args.exemplos_externos).is_file(),
            'usa_rede': False}
    if args.plan:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    started = time.time()
    out, cache = Path(args.saida).resolve(), Path(args.cache_dir).resolve()
    # Falha cedo, antes de indexar ou gerar, se exemplos/configuração não estiverem presentes.
    examples = ExampleBank(args.pareceres, args.exemplos_externos, args.seed)
    load_dotenv(ROOT)
    if args.provider == 'azure':
        from azure_openai_backend import AzureSettings
        AzureSettings.load().require()
    identity = {k: v for k, v in vars(args).items()
                if k not in ('saida', 'cache_dir', 'workers', 'max_chamadas', 'max_unidades', 'max_candidatas', 'por_topico', 'plan')}
    implementation = [[p.name, file_hash(p)] for p in sorted(Path(__file__).parent.glob('*.py'))]
    fingerprints = [[p.as_posix(), file_hash(p)] for p in source_files(args.origens)]
    for origin in args.origens:
        for name in ('assuntos.json', 'conceitos.json'):
            fingerprints.extend([[p.as_posix(), file_hash(p)] for p in sorted(Path(origin).glob('subtopicos/*/' + name))])
    for name in (args.pareceres, args.exemplos_externos, args.manifest):
        if name:
            fingerprints.append([name, file_hash(name)])
    signature = sha(json.dumps([identity, implementation, fingerprints], sort_keys=True), 40)
    clients = {}
    error = None
    with output_lock(out):
        previous = read_json(out / 'run_config.json')
        if previous and previous.get('signature') != signature:
            raise ValueError('Código, fontes ou configuração mudaram. Use outra saída; não misture versões.')
        if not previous and any(p.name != '.run.lock' for p in out.iterdir()):
            raise ValueError('Saída não vazia sem assinatura compatível; escolha outra pasta')
        atomic_json(out / 'run_config.json', {'signature': signature, 'args': vars(args),
                                             'implementation': implementation, 'fontes': fingerprints, 'plano': plan})
        examples.export(out / 'referencias_avaliacao')
        index = CorpusIndex(cache / 'indice', args.origens, args.manifest)
        log('Preparando índice BM25 e conferindo fontes; esta etapa não chama modelos.')
        with output_lock(cache / 'indice'):
            info = index.build()
        log(f"Índice: {info['chunks']} trechos; cobertura: {info['cobertura']}")
        attempts = len(read_jsonl(out / 'chamadas_llm.jsonl'))
        remaining = args.max_chamadas - attempts
        if remaining <= 0:
            summary = report(out, args, started, 'Teto cumulativo atingido; amplie --max-chamadas para retomar')
            return 2
        budget, log_lock = CallBudget(remaining), threading.Lock()
        try:
            for role in ('redator', 'juiz', 'respondente', 'novidade'):
                model, effort = getattr(args, role).rsplit(':', 1)
                safe = re.sub(r'[^\w.-]', '_', model + '_' + effort)
                clients[role] = LLMClient(model, None if effort == 'none' else effort,
                                          cache / 'llm' / f'{role}_{safe}.sqlite3', out / 'chamadas_llm.jsonl',
                                          provider=args.provider, max_calls=remaining, budget=budget, log_lock=log_lock,
                                          max_attempts=3, max_tokens_cap=24000)
            engine = Engine(clients['redator'], clients['juiz'], clients['respondente'], clients['novidade'],
                            index, examples, complement=args.configuracao == 'nota_complemento',
                            input_mode='direta' if args.configuracao == 'direta' else 'nota')
            engine.checkpoint_dir = out / 'artefatos_qa'
            stop = threading.Event()
            with ThreadPoolExecutor(max_workers=min(args.workers, len(topics))) as pool:
                jobs = [pool.submit(run_topic, engine, topic, args, out, stop) for topic in topics]
                for future in as_completed(jobs):
                    try:
                        future.result()
                    except Exception:
                        stop.set()
                        raise
        except Exception as exc:
            error = f'{type(exc).__name__}: {str(exc)[:500]}'
            raise
        finally:
            atomic_json(out / 'uso_cache.json', {role: {'cache_hits': client.usage.get('cached', 0),
                                                       'por_etapa': client.usage_by_stage}
                                                for role, client in clients.items()})
            for client in clients.values():
                client.close()
            summary = report(out, args, started, error)
            log(f"Saída: {out}; aprovadas: {summary['total_aprovadas_automaticamente']}; metas: {summary['metas_atingidas']}")
    return 0 if summary['metas_atingidas'] else 2


if __name__ == '__main__':
    sys.exit(main())
