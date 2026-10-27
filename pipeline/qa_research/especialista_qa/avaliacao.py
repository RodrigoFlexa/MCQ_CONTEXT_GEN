"""Os dois respondentes trabalham no mesmo grupo, em paralelo, sem ver MCQ ou gabarito."""
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.geracao_tipos.avaliacao import AvaliacaoModelos, JUIZ
from pipeline.qa_research.geracao_tipos.core import prompt
from .core import ler_linhas, sha, agora

RESPONDENTES = {'gpt-5-4-nano': 'gpt-5-4-nano-petrobras:low', 'gpt-5-4': 'gpt-5-4-petrobras:low'}


class AvaliacaoObrigatoria(AvaliacaoModelos):
    def checar_modelos(self):
        required = set(self.respondentes)
        super().checar_modelos()
        missing = required-set(self.respondentes)
        if missing:
            raise RuntimeError('Respondente obrigatório indisponível: '+', '.join(sorted(missing)))


def avaliar(saida, *, workers=8, lote_juiz=8, clientes=None, progress=print):
    saida = Path(saida)
    if not (saida/'conversao_concluida.json').exists():
        raise ValueError('Conclua a conversão antes de avaliar')
    source = saida/'aprovadas.jsonl'
    approved = ler_linhas(source)
    fingerprint = sha(approved)
    directory = saida/'avaliacao'
    with output_lock(directory):
        protocol = {'schema': 'avaliacao-especialista-v1', 'aprovadas_sha256': fingerprint,
                    'respondentes': RESPONDENTES, 'juiz': JUIZ, 'lote_juiz': lote_juiz,
                    'prompt_respondente_sha256': sha(prompt('respondente')),
                    'prompt_juiz_sha256': sha(prompt('juiz_respostas'))}
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
