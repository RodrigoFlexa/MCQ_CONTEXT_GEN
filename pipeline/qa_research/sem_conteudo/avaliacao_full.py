"""Mesmos dois respondentes/juiz do Full, para todas as QAs brutas, sem aprovação fictícia."""
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.especialista_qa.avaliacao import AvaliacaoObrigatoria, RESPONDENTES, JUIZ
from pipeline.qa_research.especialista_qa import avaliacao as motor_avaliacao
from pipeline.qa_research.geracao_tipos.avaliacao import AvaliacaoModelos
from pipeline.qa_research.geracao_tipos.core import prompt
from pipeline.qa_research.tipos import TIPOS
from .core import sha, agora
from .full import linhas


class AvaliacaoFullSemConteudo(AvaliacaoObrigatoria):
    def carregar_questoes(self):
        return {q['uid']: q for q in linhas(self.rodada/'questoes.jsonl')}

    def tabela(self):
        def agrega(predicate):
            out = {}
            for m in self.respondentes:
                target = [u for u,q in self.questoes.items() if predicate(q)]
                done = [u for u in target if u in self.vereditos[m]]
                vs = [self.vereditos[m][u] for u in done if self.vereditos[m][u] is not None]
                n, c, p = len(vs), vs.count('correta'), vs.count('parcial')
                out[m] = dict(total=len(target), processadas=len(done), n=n, nao_avaliadas=len(done)-n,
                    cobertura=round(100*n/len(target), 1) if target else None,
                    bloqueios_respondente=sum(self.estados[m].get(u)=='bloqueio_respondente' for u in done),
                    bloqueios_juiz=sum(self.estados[m].get(u)=='bloqueio_juiz' for u in done),
                    corretas=c, parciais=p, incorretas=vs.count('incorreta'),
                    acuracia=round(100*c/n, 1) if n else None,
                    com_parcial=round(100*(c+.5*p)/n, 1) if n else None)
            return out
        res = dict(atualizado=agora(), questoes=len(self.questoes),
            topicos=len({q['item'] for q in self.questoes.values()}), juiz=self.juiz, respondentes=self.respondentes,
            geral=agrega(lambda q: True),
            por_tipo={t:agrega(lambda q,t=t:q['tipo']==t) for t in TIPOS},
            por_composicao={c:agrega(lambda q,c=c:q['composicao']==c) for c in ('simples','composta')},
            por_subtopico={i:agrega(lambda q,i=i:q['item']==i) for i in sorted({q['item'] for q in self.questoes.values()})},
            politica_bloqueios='Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.')
        atomic_json(self.saida/'acuracia.json', res)
        self._markdown(res)
        self._csv(res)
        with (self.saida/'ACURACIA.md').open('a',encoding='utf-8') as f:
            f.write('\n## Cobertura\n\n| Modelo | Total | Com nota | Sem nota | Cobertura (%) |\n|---|---:|---:|---:|---:|\n')
            for m,d in res['geral'].items():
                f.write(f"| {m} | {d['total']} | {d['n']} | {d['nao_avaliadas']} | {d['cobertura']} |\n")
            f.write('\n'+res['politica_bloqueios']+'\n')
        return res

    def exportar(self):
        AvaliacaoModelos.exportar(self)
        target = self.saida/'avaliacoes.jsonl'
        rows = linhas(target)
        for r in rows:
            for m in self.respondentes:
                r['status_avaliacao_'+m] = self.estados[m].get(r['uid'],'pendente')
        from .core import GeracaoSemConteudo
        GeracaoSemConteudo.jsonl(target, rows)


def avaliar(saida, *, workers=8, lote_juiz=8, clientes=None, progress=print):
    saida = Path(saida)
    cfg, metas = read_json(saida/'config.json') or {}, read_json(saida/'metas.json') or {}
    rows = linhas(saida/'questoes.jsonl')
    from collections import Counter
    counts = Counter(q['item'] for q in rows)
    expected = {i['id']:i['meta'] for i in metas.get('itens',[])}
    result = read_json(saida/'resultado.json') or {}
    if not (saida/'geracao_concluida.json').exists() or cfg.get('extensao_sem_contexto') != 'full-v1':
        raise ValueError('Conclua a extensão do baseline antes de avaliar')
    if not rows or len({q['uid'] for q in rows})!=len(rows) or dict(counts)!=expected or len(rows)!=metas.get('total'):
        raise ValueError('Banco incompleto ou metas incompatíveis')
    fingerprint = sha(rows)
    if fingerprint != result.get('questoes_sha256') or sha(metas)!=cfg.get('manifesto_sha256'):
        raise ValueError('Banco ou metas alterados após a geração')
    directory = saida/'avaliacao'
    with output_lock(directory):
        protocol = dict(schema='avaliacao-sem-conteudo-full-v1', questoes_sha256=fingerprint,
            respondentes=RESPONDENTES, juiz=JUIZ, lote_juiz=lote_juiz,
            prompt_respondente_sha256=sha(prompt('respondente')),prompt_juiz_sha256=sha(prompt('juiz_respostas')),
            politica_bloqueios='terminais_sem_nota_com_cobertura_v1',
            codigo_sha256=sha(Path(__file__).read_text(encoding='utf-8')),
            motor_bloqueios_sha256=sha(Path(motor_avaliacao.__file__).read_text(encoding='utf-8')))
        old = read_json(directory/'protocolo_experimento.json')
        if old is not None and old != protocol:
            raise ValueError('Questões ou protocolo mudaram: use outra saída')
        if old is None:
            atomic_json(directory/'protocolo_experimento.json',protocol)
        for m in RESPONDENTES:
            for name in ('respostas','juiz'):(directory/name/m).mkdir(parents=True,exist_ok=True)
        (directory/'falhas').mkdir(parents=True,exist_ok=True)
        marker = directory/'avaliacao_concluida.json'
        marker.unlink(missing_ok=True)
        (directory/'falha_execucao.json').unlink(missing_ok=True)
        e = AvaliacaoFullSemConteudo(saida,respondentes=RESPONDENTES,juiz=JUIZ,
            grupos=[tuple(RESPONDENTES)],workers=max(2,workers),lote_juiz=lote_juiz,clientes=clientes,progress=progress)
        try:
            failures = e.run()
            summary = read_json(directory/'acuracia.json')['geral']
            complete = all(summary[m]['processadas']==len(rows) and
                all(e._arq_resposta(m,q['uid']).exists() for q in rows) for m in RESPONDENTES)
            if sha(linhas(saida/'questoes.jsonl')) != fingerprint:
                raise RuntimeError('Banco alterado durante a avaliação')
            if complete:
                atomic_json(marker,dict(em=agora(),questoes=len(rows),questoes_sha256=fingerprint,modelos=list(RESPONDENTES),
                    status='concluida_com_bloqueios' if any(d['nao_avaliadas'] for d in summary.values()) else 'concluida',
                    cobertura_por_modelo=summary,falhas_transitorias_na_passagem=failures))
                return 0
            return 2
        except Exception as exc:
            atomic_json(directory/'falha_execucao.json',dict(erro=type(exc).__name__,mensagem=str(exc)[:1500]))
            return 2
        finally:
            for c in e.clientes.values():
                if hasattr(c,'close'):c.close()
