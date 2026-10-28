"""Avalia apenas a amostra fixa de 1.000 QAs sem contexto, sem gerar questões."""
import argparse
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.especialista_qa.avaliacao import RESPONDENTES, JUIZ
from pipeline.qa_research.especialista_qa import avaliacao as motor_bloqueios
from pipeline.qa_research.geracao_tipos.core import prompt
from . import core as C
from . import avaliacao_full as motor
from .full import linhas, SEMENTE

MANIFESTO = C.HERE/'amostra_1000.json'
SAIDA = C.ROOT/'pipeline/qa_research/relatorios/sem_conteudo_amostra_1000'


def carregar(manifesto=MANIFESTO, fonte=SEMENTE):
    data = read_json(manifesto)
    if not data or data.get('schema') != 'amostra-sem-conteudo-v1':
        raise ValueError('Manifesto de amostra inválido')
    ids = data.get('uids', [])
    if not ids or len(ids) != data.get('n') or len(set(ids)) != len(ids):
        raise ValueError('IDs ou tamanho da amostra inválidos')
    rows = linhas(fonte)
    byid = {q['uid']: q for q in rows}
    if len(byid) != len(rows) or len(rows) != data.get('fonte_n') or C.sha(rows) != data.get('fonte_sha256'):
        raise ValueError('Fonte mudou em relação à amostra congelada')
    if set(ids)-set(byid):
        raise ValueError('Amostra contém IDs ausentes da fonte')
    selected = [byid[u] for u in ids]
    if C.sha(selected) != data.get('amostra_sha256'):
        raise ValueError('Conteúdo da amostra mudou')
    for q in selected:
        C.validar_questao({k:q[k] for k in C.CAMPOS})
    return data, selected


def preparar(saida, data, selected):
    """Chamado sob lock da saída. Mantém exatamente IDs, textos e ordem congelados."""
    saida = Path(saida)
    cfg = dict(schema='avaliacao-amostra-sem-conteudo-v1',manifesto_sha256=C.sha(data),
               questoes_sha256=C.sha(selected),n=len(selected),geracao=False,refinamento=False,deduplicacao=False)
    old = read_json(saida/'config.json')
    if old is not None and old != cfg:
        raise ValueError('Amostra/configuração mudou: use outra saída')
    path = saida/'questoes.jsonl'
    if path.exists() and linhas(path) != selected:
        raise ValueError('Questões salvas foram alteradas: não substituir a amostra')
    # Não aproveita checkpoints sem um protocolo de seleção reconhecido.
    if old is None and (saida/'avaliacao').exists():
        raise ValueError('Avaliação existente sem protocolo da amostra; use outra saída')
    atomic_json(saida/'config.json',cfg)
    atomic_json(saida/'amostra.json',data)
    if not path.exists():
        C.GeracaoSemConteudo.jsonl(path,selected)


def avaliar(saida=SAIDA, *, manifesto=MANIFESTO, fonte=SEMENTE, workers=8, lote_juiz=8,
            clientes=None, progress=print):
    if workers < 1 or lote_juiz < 1:
        raise ValueError('Workers e lote do juiz devem ser positivos')
    saida, fonte = Path(saida), Path(fonte)
    if saida.resolve() == fonte.parent.resolve() or fonte.parent.resolve() in saida.resolve().parents:
        raise ValueError('Use outra saída, fora da run original')
    data, rows = carregar(manifesto,fonte)
    fingerprint = C.sha(rows)
    with output_lock(saida):
        preparar(saida,data,rows)
        directory = saida/'avaliacao'
        with output_lock(directory):
            protocol = dict(schema='avaliacao-sem-conteudo-amostra-v1',questoes_sha256=fingerprint,
                manifesto_sha256=C.sha(data),respondentes=RESPONDENTES,juiz=JUIZ,lote_juiz=lote_juiz,
                prompt_respondente_sha256=C.sha(prompt('respondente')),
                prompt_juiz_sha256=C.sha(prompt('juiz_respostas')),
                politica_bloqueios='terminais_sem_nota_com_cobertura_v1',
                codigo_sha256=C.sha(Path(__file__).read_text(encoding='utf-8')),
                motor_sha256=C.sha(Path(motor.__file__).read_text(encoding='utf-8')),
                bloqueios_sha256=C.sha(Path(motor_bloqueios.__file__).read_text(encoding='utf-8')))
            path = directory/'protocolo_experimento.json'
            old = read_json(path)
            if old is not None and old != protocol:
                raise ValueError('Questões ou protocolo de avaliação mudaram: use outra saída')
            if old is None:
                atomic_json(path,protocol)
            for m in RESPONDENTES:
                for name in ('respostas','juiz'):(directory/name/m).mkdir(parents=True,exist_ok=True)
            (directory/'falhas').mkdir(parents=True,exist_ok=True)
            marker = directory/'avaliacao_concluida.json'
            marker.unlink(missing_ok=True)
            (directory/'falha_execucao.json').unlink(missing_ok=True)
            e = motor.AvaliacaoFullSemConteudo(saida,respondentes=RESPONDENTES,juiz=JUIZ,
                grupos=[tuple(RESPONDENTES)],workers=max(2,workers),lote_juiz=lote_juiz,
                clientes=clientes,progress=progress)
            try:
                failures = e.run()
                summary = read_json(directory/'acuracia.json')['geral']
                if C.sha(linhas(saida/'questoes.jsonl')) != fingerprint:
                    raise RuntimeError('Banco alterado durante a avaliação')
                complete = all(summary[m]['processadas']==len(rows) and
                    all(e._arq_resposta(m,q['uid']).exists() for q in rows) for m in RESPONDENTES)
                if complete:
                    atomic_json(marker,dict(em=C.agora(),questoes=len(rows),questoes_sha256=fingerprint,
                        modelos=list(RESPONDENTES),
                        status='concluida_com_bloqueios' if any(d['nao_avaliadas'] for d in summary.values()) else 'concluida',
                        cobertura_por_modelo=summary,falhas_transitorias_na_passagem=failures))
                return 0 if complete else 2
            except Exception as exc:
                atomic_json(directory/'falha_execucao.json',dict(erro=type(exc).__name__,mensagem=str(exc)[:1500]))
                return 2
            finally:
                for c in e.clientes.values():
                    if hasattr(c,'close'):c.close()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--saida',type=Path,default=SAIDA)
    p.add_argument('--manifesto',type=Path,default=MANIFESTO)
    p.add_argument('--fonte',type=Path,default=SEMENTE)
    p.add_argument('--workers',type=int,default=8)
    p.add_argument('--lote-juiz',type=int,default=8)
    p.add_argument('--plano',action='store_true')
    a = p.parse_args(argv)
    data, rows = carregar(a.manifesto,a.fonte)
    print(f"Amostra fixa: {len(rows)} questões de {data['fonte_n']}; sorteio {data['repeticao']}; semente {data['semente']}.",flush=True)
    print(f'Saída: {a.saida}',flush=True)
    if a.plano:
        print(f'Plano sem API e sem criar saída: {len(rows)*2} respostas, mais julgamentos. Nenhuma geração de questões.')
        return 0
    return avaliar(a.saida,manifesto=a.manifesto,fonte=a.fonte,workers=a.workers,lote_juiz=a.lote_juiz)


if __name__=='__main__':raise SystemExit(main())
