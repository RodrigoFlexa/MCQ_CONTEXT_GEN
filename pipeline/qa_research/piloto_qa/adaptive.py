"""Geração contínua com falhas, reparos e checkpoints por candidata."""
import asyncio
from collections import Counter
from pathlib import Path
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.inventario.llm import BudgetExceeded
from pipeline.qa_research.v3.runtime import Calls, digest, topic
from . import contracts as C, prompts as P, prompts_fluxo as F
from .contextos import packages
from .generate import jsonl
from .rounds import CandidateRound
from .validation import source_with_passages


def memory(bank, package, similarity, limit):
    recent = [q for q in bank if q.get('pacote') == package['id'] and q.get('item') == package.get('item')][-min(5, limit):]
    nearest = similarity.nearest(package['nome'], bank, limit)
    result, seen = [], set()
    for q in recent + nearest:
        if q['id'] not in seen: result.append(q['pergunta']); seen.add(q['id'])
        if len(result) >= limit: break
    return result


def priorities(bank, item, round_number):
    counts = Counter(q['tipo'] for q in bank if q.get('item') == item and q.get('nova'))
    rotation = list(C.TYPES); offset = (round_number - 1) % len(rotation)
    rotation = rotation[offset:] + rotation[:offset]
    return sorted(rotation, key=lambda t: counts[t])


async def generate(document, item, group, config, output, bank, similarity, examples=(), pending=(), transport=None):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    contexts = [dict(p, item=item) for p in packages(document, config['context_chars'])]
    identity = dict(schema='qa-continuo-1', documento=digest(document), banco=digest(bank),
        config={k: v for k, v in config.items() if k not in ('max_calls', 'heartbeat', 'workers')},
        item=item, grupo=group, exemplos=list(examples), pendencias=list(pending), semantica=similarity.protocol,
        prompts={k: digest(v) for k, v in dict(gerar=F.GENERATE, reparar=F.REPAIR, auditar=F.AUDIT, refinar=P.AUTHOR, resolver=P.SOLVE).items()},
        codigo={p.name: digest(p.read_text(encoding='utf-8')) for p in Path(__file__).parent.glob('*.py')})
    old = read_json(output / 'identidade.json'); C.require(old is None or old == identity, 'Fluxo/entradas mudaram; use nova saída')
    atomic_json(output / 'identidade.json', identity); atomic_json(output / 'contextos.json', contexts)
    state = read_json(output / 'estado.json') or dict(rodada=0, proximo=0, vazias={p['id']: 0 for p in contexts}, records=[], historico=[])
    state.setdefault('falhas_contexto', {p['id']: 0 for p in contexts})
    calls = Calls(output, config, transport=transport)
    unfinished, reason, error = [], 'em_andamento', None

    def accepted(): return [r['questao'] for r in state['records'] if r['decisao'] == 'admitir']

    def save():
        records = state['records'] + unfinished
        admitted = [r['questao'] for r in records if r['decisao'] == 'admitir']
        jsonl(output / 'aprovadas.jsonl', admitted); atomic_json(output / 'decisoes.json', records)
        report = dict(schema='qa-continuo-1', item=item, grupo=group,
            status='concluido' if reason == 'contextos_sem_ganho' else 'parcial', motivo_parada=reason, erro=error,
            admitidas=len(admitted), candidatas=len(records), invalidas_contrato=sum(r['decisao'] == 'invalida_contrato' for r in records),
            falhas_validacao=[dict(id=r['id'], decisao=r['decisao'], erros=r['erros_validacao'])
                             for r in records if r.get('erros_validacao')],
            por_classe=dict(Counter(q['tipo'] for q in admitted)), tentativas=calls.budget.used,
            contextos=[dict(id=p['id'], nome=p['nome'], tipo=p['tipo'], rodadas_sem_ganho=state['vazias'][p['id']],
                           falhas_contrato=state['falhas_contexto'][p['id']]) for p in contexts],
            historico=state['historico'], nota='Baixa produtividade observada; falhas de contrato não certificam esgotamento conceitual.')
        atomic_json(output / 'resumo.json', report)
        return report

    def progress(data):
        nonlocal unfinished
        unfinished = data['records']
        save()

    try:
        while True:
            max_failures = config.get('max_invalid_rounds', 3)
            active = [i for i, p in enumerate(contexts) if state['vazias'][p['id']] < config['patience']
                      and state['falhas_contexto'][p['id']] < max_failures]
            if not active:
                reason = 'contextos_com_falhas' if any(n >= max_failures for n in state['falhas_contexto'].values()) else 'contextos_sem_ganho'
                break
            i = next((j for j in active if j >= state['proximo']), active[0]); package = contexts[i]; source = package['blocos']
            number = state['rodada'] + 1; prefix = f'{item}_{number:06}_'; tag = f'{package["id"]}_rodada_{number}'
            inventory = bank + accepted()
            print(f'[contexto {package["id"]}] {package["nome"]} | rodada {number} | aprovadas {len(accepted())}', flush=True)

            def enrich(q, targets):
                t = targets[q['id']]
                return dict(q, uid=f'{group}:{item}:{q["id"]}', item=item, grupo=group, origem=group, nova=True,
                    tipo=t['tipo'], composicao=t['composicao'], conhecimento=t['conhecimento'], ponte=t['ponte'],
                    afirmacoes_alvo=t['afirmacoes'], documento_sha256=digest(document), pacote=package['id'],
                    blocos_contexto=source, contexto_tecnico='\n\n'.join(f"{b['capitulo']} / {b['subtitulo']}\n{b['texto']}" for b in source))

            processor = CandidateRound(calls, output / 'rodadas' / f'{number:06}_inicial.json', source, inventory,
                similarity, config, enrich, on_save=progress)
            progress(processor.data)
            payload = dict(entrada=topic(item), contexto=dict(package, blocos=source_with_passages(source)),
                rodada=number, prefixo=prefix, limite=config['batch_size'], prioridades_tipos=priorities(inventory, item, number),
                memoria=memory(inventory, package, similarity, config['memory_limit']), exemplos_de_forma=list(examples), pendencias=list(pending))
            result = await processor.process(payload, tag, prefix=prefix)
            gain = sum(r['decisao'] == 'admitir' for r in result['records'])
            valid_round = (any(r['decisao'] != 'invalida_contrato' for r in result['records'])
                           or (not result['records'] and not result['erros_entrada']))
            if valid_round:
                state['vazias'][package['id']] = 0 if gain else state['vazias'][package['id']] + 1
                state['falhas_contexto'][package['id']] = 0
            else:
                state['falhas_contexto'][package['id']] += 1
            state['records'].extend(result['records']); unfinished = []
            state.update(rodada=number, proximo=(i + 1) % len(contexts))
            state['historico'].append(dict(rodada=number, contexto=package['id'], ganho=gain,
                rodada_valida=valid_round, invalidas_contrato=sum(r['decisao'] == 'invalida_contrato' for r in result['records']),
                impedimentos=result['impedimentos'], erros_entrada=result['erros_entrada']))
            atomic_json(output / 'estado.json', state); save()
    except BudgetExceeded as exc:
        reason, error = 'suspenso_orcamento', str(exc)
    except (asyncio.CancelledError, KeyboardInterrupt) as exc:
        reason, error = 'interrompido', type(exc).__name__ + ': checkpoints individuais preservados'
        raise
    except Exception as exc:
        reason, error = 'falha_retomavel', type(exc).__name__ + ': ' + str(exc)
    finally:
        try:
            result = save()
        finally:
            await calls.close()
    return result
