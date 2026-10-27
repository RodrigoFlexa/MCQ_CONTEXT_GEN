"""Os dois respondentes trabalham no mesmo grupo, em paralelo, sem ver MCQ ou gabarito."""
import csv
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.geracao_tipos.avaliacao import AvaliacaoModelos, JUIZ
from pipeline.qa_research.geracao_tipos.core import prompt
from .core import ler_linhas, sha, agora
from .extracao import jsonl
from .revisadas import CONJUNTO_AUTORAL, ROTULOS

RESPONDENTES = {'gpt-5-4-nano': 'gpt-5-4-nano-petrobras:low', 'gpt-5-4': 'gpt-5-4-petrobras:low'}


class AvaliacaoObrigatoria(AvaliacaoModelos):
    def checar_modelos(self):
        required = set(self.respondentes)
        super().checar_modelos()
        missing = required-set(self.respondentes)
        if missing:
            raise RuntimeError('Respondente obrigatório indisponível: '+', '.join(sorted(missing)))

    def tabela(self):
        res = super().tabela()
        groups = {}
        for key in dict.fromkeys(q.get('conjunto_especialista', CONJUNTO_AUTORAL) for q in self.questoes.values()):
            models = {}
            for model in self.respondentes:
                vs = [v for uid, v in self.vereditos[model].items() if uid in self.questoes
                      and self.questoes[uid].get('conjunto_especialista', CONJUNTO_AUTORAL) == key]
                n, c, p = len(vs), vs.count('correta'), vs.count('parcial')
                models[model] = {'n': n, 'corretas': c, 'parciais': p,
                    'acuracia': round(100*c/n, 1) if n else None,
                    'com_parcial': round(100*(c+.5*p)/n, 1) if n else None}
            groups[key] = models
        res['por_conjunto_especialista'] = groups
        atomic_json(self.saida/'acuracia.json', res)
        with (self.saida/'acuracia_por_conjunto.csv').open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['conjunto_especialista', 'rotulo', 'modelo', 'julgadas', 'acuracia',
                             'com_parcial', 'corretas', 'parciais'])
            for key, models in groups.items():
                for model, d in models.items():
                    writer.writerow([key, ROTULOS[key], model, d['n'], d['acuracia'], d['com_parcial'], d['corretas'], d['parciais']])
        report = self.saida/'ACURACIA.md'
        lines = ['', '## Por conjunto de origem', '',
                 '| Conjunto | Modelo | Julgadas | Acurácia (%) | Com parcial (%) |', '|---|---|---:|---:|---:|']
        for key, models in groups.items():
            for model, d in models.items():
                lines.append(f"| {ROTULOS[key]} | {model} | {d['n']} | {d['acuracia']} | {d['com_parcial']} |")
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
            return 0
        e = AvaliacaoObrigatoria(saida, respondentes=RESPONDENTES, juiz=JUIZ,
             grupos=[tuple(RESPONDENTES)], workers=max(2, workers), lote_juiz=lote_juiz,
             clientes=clientes, progress=progress)
        try:
            failures = e.run()
            summary = read_json(directory/'acuracia.json')
            complete = all(summary['geral'].get(m, {}).get('n') == len(approved) for m in RESPONDENTES)
            if sha(ler_linhas(source)) != fingerprint:
                raise RuntimeError('O banco aprovado foi alterado durante a avaliação')
            if not failures and complete:
                atomic_json(marker, {'em': agora(), 'questoes': len(approved), 'modelos': list(RESPONDENTES),
                                     'aprovadas_sha256': fingerprint})
                return 0
            return 2
        except Exception as exc:
            atomic_json(directory/'falha_execucao.json', {'erro': type(exc).__name__, 'mensagem': str(exc)[:1500]})
            return 2
        finally:
            for c in e.clientes.values():
                if hasattr(c, 'close'):
                    c.close()
