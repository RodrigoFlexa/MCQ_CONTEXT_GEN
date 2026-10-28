"""Os dois respondentes trabalham no mesmo grupo, em paralelo, sem ver MCQ ou gabarito."""
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.geracao_tipos.avaliacao import AvaliacaoModelos, JUIZ, validar_resposta, validar_juiz
from pipeline.qa_research.geracao_tipos.core import prompt
from pipeline.qa_research.geracao_tipos.rodadas import _filtrado, _nome_arq
from pipeline.qa_research.tipos import TIPOS
from .core import ler_linhas, sha, agora
from .extracao import jsonl
from .revisadas import CONJUNTO_AUTORAL, ROTULOS

RESPONDENTES = {'gpt-5-4-nano': 'gpt-5-4-nano-petrobras:low', 'gpt-5-4': 'gpt-5-4-petrobras:low'}


class AvaliacaoObrigatoria(AvaliacaoModelos):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.estados = defaultdict(dict)

    def checar_modelos(self):
        required = set(self.respondentes)
        super().checar_modelos()
        missing = required-set(self.respondentes)
        if missing:
            raise RuntimeError('Respondente obrigatório indisponível: '+', '.join(sorted(missing)))

    def _carregar_vereditos(self):
        super()._carregar_vereditos()
        for model in self.respondentes:
            for path in (self.saida/'juiz'/model).glob('*.json'):
                for a in read_json(path)['avaliacoes']:
                    self.estados[model][a['uid']] = a.get('status_avaliacao', 'julgada')

    def responder(self, modelos=None, questoes=None):
        modelos = [m for m in (modelos or self.respondentes) if m in self.respondentes]
        qs = list(questoes if questoes is not None else self.questoes.values())
        tarefas = [(m, q) for q in qs for m in modelos if not self._arq_resposta(m, q['uid']).exists()]

        def um(t):
            m, q = t
            name = f"resposta_{m}_{_nome_arq(q['uid'])}"
            try:
                d = self.cliente('resp_'+m, self.respondentes[m]).json(prompt('respondente'), q['pergunta'],
                    tag='resposta_'+m, max_tokens=4000, item=q['item'], validate=validar_resposta)
                record = {'uid': q['uid'], 'modelo': m, 'resposta': d['resposta'], 'status_avaliacao': 'respondida'}
            except Exception as exc:
                if not _filtrado(exc):
                    self._falha(name, exc)
                    return False
                record = {'uid': q['uid'], 'modelo': m, 'resposta': None,
                          'status_avaliacao': 'bloqueio_respondente', 'erro': 'ContentFiltered', 'mensagem': str(exc)[:1500]}
            atomic_json(self._arq_resposta(m, q['uid']), record)
            self._ok(name)
            return True

        return self._paralelo(tarefas, um, 'respostas') if tarefas else 0

    @staticmethod
    def _lote_nome(model, rows):
        return hashlib.sha256((model+'|'+'|'.join(q['uid'] for q in rows)).encode()).hexdigest()[:16]

    def _registrar(self, model, rows, decisions):
        atomic_json(self.saida/'juiz'/model/(self._lote_nome(model, rows)+'.json'),
                    {'modelo': model, 'avaliacoes': decisions})
        with self.lock:
            for a in decisions:
                self.vereditos[model][a['uid']] = a['veredito']
                self.estados[model][a['uid']] = a['status_avaliacao']
            self.tabela()

    def julgar(self, final, modelos=None):
        lotes = []
        for model in (modelos or self.respondentes):
            if model not in self.respondentes:
                continue
            qs = sorted((q for q in self.questoes.values() if q['uid'] not in self.vereditos[model]
                         and self._arq_resposta(model, q['uid']).exists()),
                        key=lambda q: hashlib.sha256(f"{model}|{q['uid']}".encode()).hexdigest())
            for i in range(0, len(qs), self.lote_juiz):
                rows = qs[i:i+self.lote_juiz]
                if final or len(rows) == self.lote_juiz:
                    lotes.append((model, rows))

        def um(t):
            model, rows = t
            name = 'juiz_'+model+'_'+self._lote_nome(model, rows)
            available, blocked = [], []
            for q in rows:
                r = read_json(self._arq_resposta(model, q['uid']))
                if r.get('status_avaliacao') == 'bloqueio_respondente':
                    blocked.append(q)
                else:
                    available.append(q)
            if blocked:
                self._registrar(model, blocked, [{'uid': q['uid'], 'veredito': None,
                    'status_avaliacao': 'bloqueio_respondente',
                    'justificativa': 'Sem resposta: bloqueio do provedor. Não há julgamento técnico.'} for q in blocked])
            if available:
                ids = [f'Q{i}' for i in range(1, len(available)+1)]
                payload = [{'id': i, 'pergunta': q['pergunta'], 'resposta_referencia': q['resposta'],
                            'resposta_candidato': read_json(self._arq_resposta(model, q['uid']))['resposta']}
                           for i, q in zip(ids, available)]
                try:
                    d = self.cliente('juiz', self.juiz).json(prompt('juiz_respostas'), json.dumps(payload, ensure_ascii=False),
                        tag='juiz_respostas', max_tokens=8000, validate=lambda d: validar_juiz(d, ids))
                    decisions = [{'uid': q['uid'], 'veredito': a['veredito'], 'status_avaliacao': 'julgada',
                                  'justificativa': a.get('justificativa', '')} for q, a in zip(available, d['avaliacoes'])]
                except Exception as exc:
                    if not _filtrado(exc):
                        self._falha(name, exc)
                        return False
                    # O lote bloqueado não é reescrito, dividido ou reenviado para contornar o filtro.
                    decisions = [{'uid': q['uid'], 'veredito': None, 'status_avaliacao': 'bloqueio_juiz',
                                  'justificativa': 'Lote bloqueado pelo provedor; sem julgamento técnico.',
                                  'erro': 'ContentFiltered', 'mensagem': str(exc)[:1500]} for q in available]
                self._registrar(model, available, decisions)
            self._ok(name)
            return True

        return self._paralelo(lotes, um, 'juiz') if lotes else 0

    def _acc(self, model):
        values = [v for u, v in self.vereditos[model].items() if u in self.questoes and v is not None]
        return f'{100*values.count("correta")/len(values):.1f}% ({len(values)})' if values else '-'

    def tabela(self):
        def agrega(predicate):
            models = {}
            for model in self.respondentes:
                target = {u for u, q in self.questoes.items() if predicate(q)}
                done = [u for u in target if u in self.vereditos[model]]
                vs = [self.vereditos[model][u] for u in done if self.vereditos[model][u] is not None]
                n, c, p = len(vs), vs.count('correta'), vs.count('parcial')
                models[model] = {'total': len(target), 'processadas': len(done), 'n': n, 'nao_avaliadas': len(done)-n,
                    'cobertura': round(100*n/len(target), 1) if target else None,
                    'bloqueios_respondente': sum(self.estados[model].get(u) == 'bloqueio_respondente' for u in done),
                    'bloqueios_juiz': sum(self.estados[model].get(u) == 'bloqueio_juiz' for u in done),
                    'corretas': c, 'parciais': p,
                    'acuracia': round(100*c/n, 1) if n else None,
                    'com_parcial': round(100*(c+.5*p)/n, 1) if n else None}
            return models
        groups = {key: agrega(lambda q, key=key: q.get('conjunto_especialista', CONJUNTO_AUTORAL) == key)
                  for key in dict.fromkeys(q.get('conjunto_especialista', CONJUNTO_AUTORAL) for q in self.questoes.values())}
        res = {'atualizado': agora(), 'questoes': len(self.questoes), 'topicos': len({q['item'] for q in self.questoes.values()}),
               'juiz': self.juiz, 'respondentes': self.respondentes, 'geral': agrega(lambda q: True),
               'por_tipo': {t: agrega(lambda q, t=t: q['tipo'] == t) for t in TIPOS},
               'por_composicao': {c: agrega(lambda q, c=c: q.get('composicao') == c) for c in ('simples', 'composta')},
               'por_conjunto_especialista': groups,
               'politica_bloqueios': 'Bloqueios são resultados terminais sem nota técnica; ficam fora do denominador da acurácia e são mostrados na cobertura.'}
        atomic_json(self.saida/'acuracia.json', res)
        self._markdown(res)
        self._csv(res)
        with (self.saida/'acuracia_por_conjunto.csv').open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['conjunto_especialista', 'rotulo', 'modelo', 'julgadas', 'acuracia',
                             'com_parcial', 'corretas', 'parciais', 'total', 'processadas', 'nao_avaliadas', 'cobertura'])
            for key, models in groups.items():
                for model, d in models.items():
                    writer.writerow([key, ROTULOS[key], model, d['n'], d['acuracia'], d['com_parcial'], d['corretas'], d['parciais'],
                                     d['total'], d['processadas'], d['nao_avaliadas'], d['cobertura']])
        report = self.saida/'ACURACIA.md'
        lines = ['', '## Por conjunto de origem', '',
                 '| Conjunto | Modelo | Julgadas | Acurácia (%) | Com parcial (%) |', '|---|---|---:|---:|---:|']
        for key, models in groups.items():
            for model, d in models.items():
                lines.append(f"| {ROTULOS[key]} | {model} | {d['n']} | {d['acuracia']} | {d['com_parcial']} |")
        lines += ['', '## Cobertura da avaliação', '', res['politica_bloqueios'], '',
                  '| Modelo | Total | Processadas | Julgadas | Bloqueio respondente | Bloqueio juiz | Cobertura (%) |',
                  '|---|---:|---:|---:|---:|---:|---:|']
        for model, d in res['geral'].items():
            lines.append(f"| {model} | {d['total']} | {d['processadas']} | {d['n']} | {d['bloqueios_respondente']} | {d['bloqueios_juiz']} | {d['cobertura']} |")
        report.write_text(report.read_text(encoding='utf-8')+'\n'.join(lines)+'\n', encoding='utf-8')
        return res

    def exportar(self):
        super().exportar()
        target = self.saida/'avaliacoes.jsonl'
        rows = ler_linhas(target)
        for row in rows:
            q = self.questoes[row['uid']]
            row.update({k: q.get(k) for k in ('conjunto_especialista', 'fonte_uid', 'agrupamento_original',
                                             'subtopico_original', 'revisao_humana')})
            for model in self.respondentes:
                row['status_avaliacao_'+model] = self.estados[model].get(row['uid'], 'pendente')
        jsonl(target, rows)


def avaliar(saida, *, workers=8, lote_juiz=8, clientes=None, progress=print):
    saida = Path(saida)
    if not (saida/'conversao_concluida.json').exists():
        raise ValueError('Conclua a conversão antes de avaliar')
    source = saida/'aprovadas.jsonl'
    approved = ler_linhas(source)
    fingerprint = sha(approved)
    directory = saida/'avaliacao'
    with output_lock(directory):
        protocol = {'schema': 'avaliacao-especialista-v2', 'aprovadas_sha256': fingerprint,
                    'respondentes': RESPONDENTES, 'juiz': JUIZ, 'lote_juiz': lote_juiz,
                    'prompt_respondente_sha256': sha(prompt('respondente')),
                    'prompt_juiz_sha256': sha(prompt('juiz_respostas')),
                    'politica_bloqueios': 'terminais_sem_nota_com_cobertura_v1',
                    'codigo_sha256': sha(Path(__file__).read_text(encoding='utf-8'))}
        ppath = directory/'protocolo_experimento.json'
        old = read_json(ppath)
        if old is not None and old != protocol:
            raise ValueError('Questões ou protocolo de avaliação mudaram; use outra saída para não misturar resultados')
        if old is None:
            atomic_json(ppath, protocol)
        # Cria os pais antes das escritas paralelas, inclusive para checkouts Windows/OneDrive.
        for model in RESPONDENTES:
            (directory/'respostas'/model).mkdir(parents=True, exist_ok=True)
            (directory/'juiz'/model).mkdir(parents=True, exist_ok=True)
        (directory/'falhas').mkdir(parents=True, exist_ok=True)
        marker = directory/'avaliacao_concluida.json'
        marker.unlink(missing_ok=True)
        (directory/'falha_execucao.json').unlink(missing_ok=True)
        if not approved:
            atomic_json(directory/'sem_questoes.json', {'motivo': 'Nenhuma QA aprovada para responder'})
            atomic_json(marker, {'em': agora(), 'questoes': 0, 'modelos': list(RESPONDENTES),
                                 'aprovadas_sha256': fingerprint})
            return 0
        e = AvaliacaoObrigatoria(saida, respondentes=RESPONDENTES, juiz=JUIZ,
             grupos=[tuple(RESPONDENTES)], workers=max(2, workers), lote_juiz=lote_juiz,
             clientes=clientes, progress=progress)
        try:
            failures = e.run()
            summary = read_json(directory/'acuracia.json')
            complete = all(summary['geral'].get(m, {}).get('processadas') == len(approved)
                           and all(e._arq_resposta(m, q['uid']).exists() for q in approved) for m in RESPONDENTES)
            if sha(ler_linhas(source)) != fingerprint:
                raise RuntimeError('O banco aprovado foi alterado durante a avaliação')
            if complete:
                atomic_json(marker, {'em': agora(), 'questoes': len(approved), 'modelos': list(RESPONDENTES),
                                     'status': 'concluida_com_bloqueios' if any(d['nao_avaliadas'] for d in summary['geral'].values()) else 'concluida',
                                     'aprovadas_sha256': fingerprint, 'cobertura_por_modelo': summary['geral'],
                                     'falhas_transitorias_na_passagem': failures})
                return 0
            return 2
        except Exception as exc:
            atomic_json(directory/'falha_execucao.json', {'erro': type(exc).__name__, 'mensagem': str(exc)[:1500]})
            return 2
        finally:
            for c in e.clientes.values():
                if hasattr(c, 'close'):
                    c.close()
