"""Geração bruta por quantidade: sem auditoria, refino ou exclusão de questões."""
from __future__ import annotations

import copy
import hashlib
import json
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.tipos import TIPOS

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
METAS = HERE / 'metas_geracao_final_20261024.json'
SCHEMA = 'geracao-sem-conteudo-v2'
MODELOS = {'geracao': 'gpt-5-4-petrobras:high'}
CAMPOS = {'tipo', 'cenario', 'composicao', 'pergunta', 'resposta'}


def sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def agora():
    return datetime.now(timezone.utc).isoformat()


def carregar_metas(path=METAS):
    data = read_json(path)
    if not data or data.get('schema') != 'metas-sem-conteudo-v1':
        raise ValueError('Manifesto de metas inválido')
    items = data.get('itens', [])
    ids = [r['id'] for r in items]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError('Metas vazias ou IDs repetidos')
    for r in items:
        if set(r) != {'id', 'topico', 'subtopico', 'frase_especialista', 'meta'}:
            raise ValueError('As metas devem conter somente rótulos, frase e quantidade')
        if type(r['meta']) is not int or r['meta'] < 1 or any(
                not isinstance(r[k], str) or not r[k].strip()
                for k in ('id', 'topico', 'subtopico', 'frase_especialista')):
            raise ValueError('Meta e escopo devem estar preenchidos')
    if sum(r['meta'] for r in items) != data.get('total'):
        raise ValueError('Total do manifesto não confere')
    return data


def validar_questao(q):
    """Somente estrutura utilizável; não julga qualidade, forma ou semelhança."""
    if not isinstance(q, dict) or set(q) != CAMPOS:
        raise ValueError('Questão deve ter exatamente tipo, cenario, composicao, pergunta e resposta')
    if q['tipo'] not in TIPOS or type(q['cenario']) is not bool or q['composicao'] not in ('simples', 'composta'):
        raise ValueError('Tipo, cenário ou composição inválidos no JSON')
    if any(not isinstance(q[k], str) or not q[k].strip() for k in ('pergunta', 'resposta')):
        raise ValueError('Pergunta e resposta devem ser textos preenchidos')


def validar_geracao(d, quantidade):
    if not isinstance(d, dict) or set(d) != {'questoes'} or not isinstance(d['questoes'], list):
        raise ValueError('Retorne um objeto com questoes como lista')
    if len(d['questoes']) != quantidade:
        raise ValueError(f'Retorne exatamente {quantidade} questões; diversidade não é condição para completar o lote')
    for q in d['questoes']:
        validar_questao(q)


class GeracaoSemConteudo:
    def __init__(self, saida, *, metas=METAS, itens=None, lote=5, memoria=20,
                 workers=5, max_lotes=100, max_chamadas=30000,
                 modelos=None, clientes=None, progress=print):
        self.saida = Path(saida)
        self.manifesto = carregar_metas(metas)
        stored = read_json(self.saida / 'config.json') or {}
        ids = list(itens or stored.get('itens') or [r['id'] for r in self.manifesto['itens']])
        if len(ids) != len(set(ids)) or set(ids) - {r['id'] for r in self.manifesto['itens']}:
            raise ValueError('Lista de tópicos inválida')
        self.itens = [next(r for r in self.manifesto['itens'] if r['id'] == i) for i in ids]
        for k, v in dict(lote=lote, memoria=memoria, workers=workers,
                         max_lotes=max_lotes, max_chamadas=max_chamadas).items():
            if type(v) is not int or v < 1:
                raise ValueError(k + ' deve ser inteiro positivo')
        self.lote, self.memoria, self.workers = lote, memoria, workers
        self.max_lotes, self.max_chamadas = max_lotes, max_chamadas
        self.modelos = {**MODELOS, **(modelos or {})}
        if set(self.modelos) != {'geracao'}:
            raise ValueError('Este modo utiliza somente o gerador')
        self.clientes = dict(clientes or {})
        self.progress = progress
        self.lock = threading.Lock()
        self.budget = None
        self.prompt = (HERE / 'prompts/geracao.md').read_text(encoding='utf-8')

    def config(self):
        cfg = {'schema': SCHEMA, 'itens': [r['id'] for r in self.itens],
               'escopos_e_metas': self.itens, 'manifesto_sha256': sha(self.manifesto),
               'modelos': self.modelos, 'lote': self.lote, 'memoria': self.memoria,
               'prompt_sha256': sha(self.prompt), 'motor_sha256': sha(Path(__file__).read_text(encoding='utf-8')),
               'tipos': list(TIPOS), 'criterio_parada': 'quantidade_gerada',
               'conteudo_externo': False, 'exemplos_herdados': False,
               'auditoria': False, 'refinamento': False, 'deduplicacao': False, 'filtro_qualidade': False}
        old = read_json(self.saida / 'config.json')
        if old and {k: v for k, v in old.items() if k != 'criado_em'} != cfg:
            raise ValueError('Configuração mudou: use outra --saida; não misture geração bruta com a run filtrada')
        if not old:
            atomic_json(self.saida / 'config.json', {**cfg, 'criado_em': agora()})
        atomic_json(self.saida / 'metas.json', self.manifesto)
        atomic_json(self.saida / 'limites_execucao.json', {
            'max_lotes_por_topico': self.max_lotes, 'max_chamadas_cumulativas': self.max_chamadas})

    def cliente(self):
        with self.lock:
            if 'geracao' not in self.clientes:
                from pipeline.qa_research.runtime import PersistentBudget
                from pipeline.inventario.llm import LLMClient, load_dotenv
                load_dotenv(ROOT)
                self.budget = PersistentBudget(self.saida / 'orcamento.json', self.max_chamadas)
                model, effort = self.modelos['geracao'].rsplit(':', 1)
                self.clientes['geracao'] = LLMClient(
                    model, effort, self.saida / '.local/geracao.sqlite3',
                    self.saida / 'chamadas/geracao.jsonl', provider='azure', budget=self.budget,
                    max_attempts=3, max_calls=self.max_chamadas, max_tokens_cap=32000, timeout=600,
                    response_dir=self.saida / '.local/respostas/geracao')
            return self.clientes['geracao']

    def lote_novo(self, item, state):
        state = copy.deepcopy(state)
        n = min(self.lote, item['meta'] - len(state['questoes']))
        rodada = state['lotes'] + 1
        payload = {'escopo': {k: item[k] for k in ('topico', 'subtopico', 'frase_especialista')},
                   'lote': rodada, 'quantidade': n,
                   'recentes': [{k: q[k] for k in ('pergunta', 'resposta')} for q in state['recentes']]}
        result = self.cliente().json(
            self.prompt, json.dumps(payload, ensure_ascii=False, sort_keys=True),
            tag='sem_conteudo_geracao', max_tokens=16000, item=item['id'],
            validate=lambda d: validar_geracao(d, n))
        for i, q in enumerate(result['questoes'], 1):
            # Conteúdo e classificações são preservados, inclusive se forem fracos ou repetidos.
            q = {**q, 'uid': f"{item['id']}:sc:{rodada:04}:{i}", 'item': item['id'],
                 'origem': 'sem_conteudo', 'rodada': rodada,
                 'avaliacao_qualidade': 'nao_realizada'}
            state['questoes'].append(q)
            state['recentes'] = (state['recentes'] + [
                {k: q[k] for k in ('uid', 'pergunta', 'resposta')}])[-self.memoria:]
        state['lotes'] = rodada
        return state

    def topico(self, item):
        directory = self.saida / 'topicos' / item['id']
        path = directory / 'estado.json'
        state = read_json(path) or {'lotes': 0, 'questoes': [], 'recentes': [], 'concluido': False}
        while True:
            try:
                n = len(state['questoes'])
                if n > item['meta'] or len({q['uid'] for q in state['questoes']}) != n:
                    raise ValueError('Checkpoint inconsistente: contagem ou IDs inválidos')
                if n == item['meta']:
                    state['concluido'] = True
                    state.pop('erro', None)
                    atomic_json(path, state)
                    self.publicar(item, state)
                    self.progress(f"[{item['id']}] concluído: {n}/{item['meta']} geradas", flush=True)
                    return True
                if state['lotes'] >= self.max_lotes:
                    state['erro'] = 'Meta incompleta: limite cumulativo de lotes atingido'
                    atomic_json(path, state)
                    self.publicar(item, state)
                    return False
                state = self.lote_novo(item, state)
                state.pop('erro', None)
                atomic_json(path, state)
                self.publicar(item, state)
                self.progress(f"[{item['id']}] lote {state['lotes']}: {len(state['questoes'])}/{item['meta']} geradas", flush=True)
            except Exception as exc:
                state['erro'] = f'{type(exc).__name__}: {str(exc)[:1500]}'
                atomic_json(path, state)
                self.publicar(item, state)
                self.progress(f"[{item['id']}] interrompido; progresso salvo: {state['erro']}", flush=True)
                return False

    @staticmethod
    def jsonl(path, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix('.jsonl.tmp')
        tmp.write_text(''.join(json.dumps(q, ensure_ascii=False) + '\n' for q in rows), encoding='utf-8')
        tmp.replace(path)

    def publicar(self, item, state):
        directory = self.saida / 'topicos' / item['id']
        self.jsonl(directory / 'questoes.jsonl', state['questoes'])
        if state['concluido']:
            atomic_json(directory / 'finalizado.json', {
                'geradas': len(state['questoes']), 'meta': item['meta'], 'em': agora()})

    def relatorio(self):
        allqs, summaries = [], []
        for item in self.itens:
            s = read_json(self.saida / 'topicos' / item['id'] / 'estado.json') or {}
            allqs += s.get('questoes', [])
            summaries.append({'id': item['id'], 'subtopico': item['subtopico'], 'meta': item['meta'],
                              'geradas': len(s.get('questoes', [])), 'lotes': s.get('lotes', 0),
                              'concluido': s.get('concluido', False), 'erro': s.get('erro')})
        self.jsonl(self.saida / 'questoes.jsonl', allqs)
        summary = {'meta_total': sum(i['meta'] for i in self.itens), 'geradas': len(allqs),
                   'tipos_declarados': dict(Counter(q['tipo'] for q in allqs)),
                   'composicoes_declaradas': dict(Counter(q['composicao'] for q in allqs)), 'topicos': summaries,
                   'auditoria': False, 'refinamento': False, 'deduplicacao': False, 'filtro_qualidade': False}
        atomic_json(self.saida / 'resultado.json', summary)
        lines = ['# Geração bruta sem conteúdo externo', '',
                 f"Geradas: **{len(allqs)}/{summary['meta_total']}**. Metas copiadas de {self.manifesto['run_referencia']}.",
                 '', 'Entradas: tópico, subtópico, frase do especialista e questões recentes desta run. '
                 'Todas as questões geradas são preservadas, inclusive repetições e questões fracas. '
                 'Sem auditoria, refinamento, filtros de qualidade ou deduplicação. A única validação é '
                 'estrutural (JSON, campos, classificações e contagem). Tipos, cenário e composição são '
                 'declarados pelo gerador, sem correção posterior e sem cotas. Qualidade e semelhança '
                 'são resultados a medir depois e não interferem na conclusão da geração.', '',
                 '| ID | Subtópico | Meta | Geradas | Lotes | Situação |', '|---|---|---:|---:|---:|---|']
        for s in summaries:
            status = 'concluído' if s['concluido'] else (s['erro'] or 'pendente')
            lines.append(f"| {s['id']} | {s['subtopico']} | {s['meta']} | {s['geradas']} | {s['lotes']} | {status.replace('|', '/')} |")
        (self.saida / 'RELATORIO.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
        return summary

    def run(self):
        with output_lock(self.saida):
            self.config()
            marker = self.saida / 'geracao_concluida.json'
            marker.unlink(missing_ok=True)
            try:
                with ThreadPoolExecutor(max_workers=self.workers) as pool:
                    ok = list(pool.map(self.topico, self.itens))
                result = self.relatorio()
                if all(ok):
                    atomic_json(marker, {'em': agora(), 'geradas': result['geradas']})
                return 0 if all(ok) else 2
            finally:
                for c in self.clientes.values():
                    if hasattr(c, 'close'):
                        c.close()
