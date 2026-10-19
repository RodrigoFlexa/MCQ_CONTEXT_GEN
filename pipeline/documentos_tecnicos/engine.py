"""Pesquisa adaptativa limitada, revisão independente e checkpoints por documento."""
import json
from pathlib import Path

from pipeline.inventario.llm import BudgetExceeded
from pipeline.inventario.textutil import atomic_json, norm, read_json, read_jsonl, sha
from pipeline.qa_v11.contracts import evidence
from . import contracts as C, prompts as P
from .profiles import source_context


class ScopeExceeded(BudgetExceeded):
    """Limite cumulativo de um documento/candidata, separado do limite global."""


class ScopedBudget:
    def __init__(self, global_budget, limit, used):
        self.global_budget, self.limit, self.used = global_budget, limit, used

    def reserve(self):
        if self.used >= self.limit:
            raise ScopeExceeded(f'Limite cumulativo de {self.limit} tentativas nesta unidade atingido')
        self.global_budget.reserve()
        self.used += 1


class Engine:
    def __init__(self, clients, index, out, args, budget):
        self.clients, self.index, self.out, self.args = clients, index, Path(out), args
        self.budget = budget
        self.scope = None

    def begin_scope(self, identifier, maximum):
        previous = read_jsonl(self.out / 'chamadas_llm.jsonl')
        used = sum(str(r.get('item', '')).split(':', 1)[0] == identifier for r in previous)
        self.scope = ScopedBudget(self.budget, maximum, used)

    def call(self, role, prompt, payload, tag, item, validator, tokens=9000):
        client = self.clients[role]
        client.budget = self.scope or self.budget
        def validate(data):
            try:
                validator(data)
            except (TypeError, KeyError, AttributeError, IndexError) as exc:
                raise ValueError(f'Estrutura incompatível ({type(exc).__name__}); use os campos e tipos '
                                 'do objeto JSON completo declarado no prompt.') from exc
        return client.json(prompt, json.dumps(payload, ensure_ascii=False), tag=tag,
                           item=item, max_tokens=tokens, validate=validate)

    def retrieve(self, state, queries):
        """Guarda buscas inclusive vazias; evidências nunca são substituídas pelo resumo."""
        state.setdefault('consultas_realizadas', [])
        state.setdefault('evidencias', [])
        old_queries = {norm(q['consulta']) for q in state['consultas_realizadas']}
        known = {v for e in state['evidencias'] for v in (e['chunk_id'], e['texto_sha256'])}
        next_id = max((int(e['id'][1:]) for e in state['evidencias']), default=0)
        additions = 0
        for query in queries[:3]:
            if norm(query) in old_queries:
                continue
            old_queries.add(norm(query))
            chunks = self.index.search(query, limit=self.args.trechos_por_busca, exclude=known)
            trace = {'consulta': query, 'retornados': len(chunks), 'incluidos': []}
            # Contexto vizinho conta dentro do orçamento, sem consumir sozinho toda a rodada.
            primary = [c for c in chunks if c.get('recuperacao') == 'bm25']
            neighbors = [c for c in chunks if c.get('recuperacao') != 'bm25']
            n_context = min(2, len(neighbors), max(0, self.args.trechos_por_busca - 1))
            selected = primary[:self.args.trechos_por_busca - n_context] + neighbors[:n_context]
            for chunk in selected:
                if len(state['evidencias']) >= self.args.max_fontes:
                    break
                digest = sha(chunk['texto'], 64)
                if chunk['chunk_id'] in known or digest in known:
                    continue
                next_id += 1
                source = evidence(chunk, f'E{next_id}')
                state['evidencias'].append(source)
                known.update((source['chunk_id'], source['texto_sha256']))
                trace['incluidos'].append(source['id'])
                additions += 1
            state['consultas_realizadas'].append(trace)
        return additions

    def process_document(self, brief, previous):
        path = self.out / 'documentos' / (brief['id'] + '.json')
        state = read_json(path) or {
            'id': brief['id'], 'pauta': brief, 'etapa': 'pesquisa', 'status': 'em_andamento',
            'evidencias': [], 'consultas_realizadas': [], 'investigacao': [], 'versoes': [],
            'revisoes': [], 'rodadas_pesquisa': 0, 'refinamentos': 0,
            'validacao_humana': 'pendente',
        }
        if state['status'] in ('aprovado', 'pendente_revisao', 'insuficiente'):
            return state
        self.begin_scope(brief['id'], self.args.max_chamadas_documento)
        state['status'] = 'em_andamento'
        state.pop('erro', None)

        def save():
            atomic_json(path, state)

        def finish(status, reason):
            state.update(status=status, motivo=reason, etapa='concluida')
            save()
            return state

        def payload(stage):
            # O histórico completo permanece no checkpoint; cada papel recebe sua tarefa atual.
            data = {'pauta': {k: brief[k] for k in ('topico', 'subtopico', 'assunto', 'frase_especialista')},
                    **source_context(state['evidencias'])}
            review = state['revisoes'][-1] if state['revisoes'] else None
            review = {k: review[k] for k in ('decisao', 'parecer', 'consultas')} if review else None
            if stage == 'pesquisa':
                data.update(
                    orientacao=state.get('orientacao', ''),
                    consultas_sugeridas={k: brief.get(k) for k in ('consulta_pt', 'consulta_en', 'termos')},
                    buscas_realizadas=state['consultas_realizadas'],
                    parecer=review,
                    pedido_refinador=state.get('pedidos_refinador', [None])[-1],
                    cobertura_anterior=previous,
                    limites_restantes={
                        'rodadas_pesquisa': max(0, self.args.max_pesquisas - state['rodadas_pesquisa']),
                        'fontes': max(0, self.args.max_fontes - len(state['evidencias']))})
            elif stage == 'redacao':
                data.update(orientacao=state.get('orientacao', ''), cobertura_anterior=previous)
            elif stage == 'revisao':
                data.update(documento=state['documento'], parecer_anterior=review,
                            limites_restantes={
                                'rodadas_pesquisa': max(0, self.args.max_pesquisas - state['rodadas_pesquisa']),
                                'fontes': max(0, self.args.max_fontes - len(state['evidencias']))})
            elif stage == 'refino':
                data.update(documento=state['documento'], parecer=review,
                            orientacao=state.get('orientacao', ''),
                            pedido_refinador=state.get('pedidos_refinador', [None])[-1],
                            limites_restantes={
                                'rodadas_pesquisa': max(0, self.args.max_pesquisas - state['rodadas_pesquisa']),
                                'fontes': max(0, self.args.max_fontes - len(state['evidencias']))})
            else:
                raise ValueError(f'Papel de documento desconhecido: {stage}')
            return data

        save()
        while True:
            stage = state['etapa']
            if stage == 'pesquisa':
                at_limit = (state['rodadas_pesquisa'] >= self.args.max_pesquisas
                            or len(state['evidencias']) >= self.args.max_fontes)
                if at_limit and not state['evidencias']:
                    return finish('insuficiente', 'Pesquisa sem fontes úteis disponíveis')
                # Mesmo após a última busca, o pesquisador examina os achados antes de redigir.
                action = self.call('pesquisador', P.PESQUISAR, payload(stage), 'doc_pesquisa',
                                   brief['id'] + ':pesquisa', C.research, 6000)
                state['investigacao'].append(action)
                state['orientacao'] = action['orientacao']
                if action['acao'] == 'insuficiente':
                    return finish('insuficiente', action['orientacao'])
                if action['acao'] == 'redigir' and state['evidencias']:
                    state['etapa'] = ('refino' if state['refinamentos'] < self.args.max_refinamentos
                                      else 'revisao') if state.get('documento') else 'redacao'
                else:
                    if at_limit:
                        return finish('pendente_revisao' if state.get('documento') else 'insuficiente',
                                      'Limite de pesquisa; informação ainda solicitada: ' + action['orientacao'])
                    queries = action['consultas'] or [brief['assunto'], brief.get('consulta_en', '')]
                    queries = [q for q in queries if q.strip()]
                    state['rodadas_pesquisa'] += 1
                    self.retrieve(state, queries)
                save()
            elif stage in ('redacao', 'refino'):
                if stage == 'refino' and state['refinamentos'] >= self.args.max_refinamentos:
                    return finish('pendente_revisao', 'Limite de refinamentos; consulte o último parecer')
                role = 'pesquisador' if stage == 'redacao' else 'refinador'
                prompt = P.REDIGIR if stage == 'redacao' else P.REFINAR
                validator = C.document if stage == 'redacao' else C.refinement
                doc = self.call(role, prompt, payload(stage), 'doc_' + stage, brief['id'] + ':' + stage,
                                lambda d: validator(d, state['evidencias']), 14000)
                if stage == 'refino' and doc.get('acao') == 'pesquisar':
                    state.setdefault('pedidos_refinador', []).append(doc)
                    if state['rodadas_pesquisa'] >= self.args.max_pesquisas or len(state['evidencias']) >= self.args.max_fontes:
                        return finish('pendente_revisao', doc['orientacao'])
                    state['orientacao'] = doc['orientacao']
                    self.retrieve(state, doc['consultas'])
                    state['rodadas_pesquisa'] += 1
                    state['etapa'] = 'pesquisa'
                    save()
                    continue
                # IDs, estados e histórico pertencem ao código, nunca à saída do modelo.
                state['documento'] = {k: doc[k] for k in ('titulo', 'texto_markdown', 'fontes')}
                state['versoes'].append(dict(state['documento']))
                if stage == 'refino':
                    state['refinamentos'] += 1
                state['etapa'] = 'revisao'
                save()
            elif stage == 'revisao':
                review = self.call('revisor', P.REVISAR, payload(stage), 'doc_revisao',
                                   brief['id'] + ':revisao', C.review, 10000)
                state['revisoes'].append({**review, 'versao': len(state['versoes']) - 1,
                                          'fontes_disponiveis': [e['id'] for e in state['evidencias']]})
                if review['decisao'] == 'aprovar':
                    return finish('aprovado', review['parecer'])
                if review['decisao'] == 'insuficiente':
                    return finish('insuficiente', review['parecer'])
                if review['decisao'] == 'pesquisar':
                    if state['rodadas_pesquisa'] >= self.args.max_pesquisas or len(state['evidencias']) >= self.args.max_fontes:
                        return finish('pendente_revisao', review['parecer'])
                    # O pedido do revisor inicia nova busca; o pesquisador examina os achados.
                    self.retrieve(state, review['consultas'])
                    state['rodadas_pesquisa'] += 1
                    state['etapa'] = 'pesquisa'
                else:
                    state['etapa'] = 'refino'
                save()
            else:
                raise ValueError(f'Etapa de documento desconhecida: {stage}')
