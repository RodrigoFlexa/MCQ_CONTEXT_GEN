"""Dois conjuntos congelados; respondentes medium e julgamento em fluxo contínuo."""
import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.sem_conteudo import core as C
from pipeline.qa_research.sem_conteudo.full import linhas
from pipeline.qa_research.sem_conteudo import avaliacao_full as motor
from pipeline.qa_research.especialista_qa import avaliacao as bloqueios
from pipeline.qa_research.geracao_tipos import avaliacao as base
from pipeline.qa_research.geracao_tipos.rodadas import _filtrado, _nome_arq

HERE = Path(__file__).resolve().parent
MANIFESTO = HERE/'amostras_1000.json'
SAIDA = C.ROOT/'pipeline/qa_research/relatorios/qa_100_palavras_medium_1000'
RESPONDENTES = {'gpt-5-4-nano':'gpt-5-4-nano-petrobras:medium','gpt-5-4':'gpt-5-4-petrobras:medium'}
JUIZ = 'gpt-5-4-petrobras:medium'


def prompt(nome):
    return (HERE/'prompts'/f'{nome}.md').read_text(encoding='utf-8').strip()


def validar_juiz(d,ids):
    base.validar_juiz(d,ids)
    for item in d['avaliacoes']:
        if not isinstance(item.get('justificativa'),str) or not item['justificativa'].strip():
            raise ValueError('Cada avaliação precisa de justificativa técnica preenchida')


def carregar(manifesto=MANIFESTO):
    data = read_json(manifesto)
    if not data or data.get('schema')!='qa-medium-amostras-v1':
        raise ValueError('Manifesto inválido')
    conditions = data.get('condicoes',[])
    if len(conditions)!=2 or len({c['id'] for c in conditions})!=2:
        raise ValueError('São obrigatórias duas condições distintas')
    selected=[]
    for cond in conditions:
        rows=[]
        for source in cond['fontes']:
            path=Path(source['path'])
            path=path if path.is_absolute() else C.ROOT/path
            qs=linhas(path)
            if len(qs)!=source['n'] or C.sha(qs)!=source['sha256']:
                raise ValueError('Fonte mudou: '+source['path'])
            rows+=qs
        byid={q['uid']:q for q in rows}
        ids=cond['uids']
        if not ids or len(byid)!=len(rows) or len(ids)!=cond['n'] or len(set(ids))!=len(ids) or set(ids)-set(byid):
            raise ValueError('IDs ou tamanho da amostra inválidos')
        qs=[byid[u] for u in ids]
        if C.sha(qs)!=cond['amostra_sha256']:
            raise ValueError('Amostra mudou')
        for q in qs:
            C.validar_questao({k:q[k] for k in C.CAMPOS})
        selected.append([{**q,'condicao':cond['id']} for q in qs])
    # Alterna condições: ambas aparecem desde os primeiros lotes do terminal.
    rows=[qs[i] for i in range(max(map(len,selected))) for qs in selected if i<len(qs)]
    if len({q['uid'] for q in rows})!=len(rows):
        raise ValueError('IDs se sobrepõem entre as duas condições')
    return data,rows


class AvaliacaoQA(motor.AvaliacaoFullSemConteudo):
    def __init__(self,*a,judge_workers=2,**kw):
        super().__init__(*a,**kw)
        self.judge_workers=judge_workers
        self.respondidas={m:set() for m in self.respondentes}
        self.inicio=time.monotonic()

    def checar_modelos(self):
        for m,alias in self.respondentes.items():
            # Uma sondagem por respondente; falha não remove o modelo.
            self.progress(f'[DISPONIBILIDADE] Verificando {m} com esforço medium...',flush=True)
            self.cliente('resp_'+m,alias).json(prompt('respondente'),
                'Qual é a função de um separador trifásico?',tag='teste_'+m,
                max_tokens=8000,validate=base.validar_resposta)

    def _markdown(self,res):
        super()._markdown(res)
        p=self.saida/'ACURACIA.md'
        text=p.read_text(encoding='utf-8').replace('Respondentes com esforço low (os gpt-4-1 não têm esforço).',
            'Respondentes com esforço medium e limite solicitado de 100 palavras.')
        p.write_text(text,encoding='utf-8')

    def tabela(self):
        res=super().tabela()
        conditions={q['condicao'] for q in self.questoes.values()}
        res['por_condicao']={}
        csvrows=[]
        for cond in sorted(conditions):
            ids=[u for u,q in self.questoes.items() if q['condicao']==cond]
            res['por_condicao'][cond]={}
            for m in self.respondentes:
                done=[u for u in ids if u in self.vereditos[m]]
                vals=[self.vereditos[m][u] for u in done if self.vereditos[m][u] is not None]
                n,c,p=len(vals),vals.count('correta'),vals.count('parcial')
                d=dict(total=len(ids),respondidas=sum(u in self.respondidas[m] for u in ids),processadas=len(done),
                    n=n,corretas=c,parciais=p,incorretas=vals.count('incorreta'),sem_nota=len(done)-n,
                    acuracia=100*c/n if n else None,com_parcial=100*(c+.5*p)/n if n else None)
                res['por_condicao'][cond][m]=d
                csvrows.append(dict(condicao=cond,modelo=m,**d))
                acc='—' if not n else f'{100*c/n:.2f}%'
                self.progress(f"[AO VIVO | {cond} | {m}] respostas {d['respondidas']}/{len(ids)} | "
                    f"julgadas {n} | C/P/I {c}/{p}/{d['incorretas']} | sem nota {d['sem_nota']} | acurácia {acc}",flush=True)
        atomic_json(self.saida/'acuracia.json',res)
        import csv
        with (self.saida/'acuracia_por_condicao.csv').open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(csvrows[0]));w.writeheader();w.writerows(csvrows)
        with (self.saida/'ACURACIA.md').open('a',encoding='utf-8') as f:
            f.write('\n## Por condição\n\n| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |\n|---|---|---:|---:|---:|---:|---:|---:|\n')
            for r in csvrows:
                acc='—' if r['acuracia'] is None else f"{r['acuracia']:.2f}"
                f.write(f"| {r['condicao']} | {r['modelo']} | {r['n']} | {r['corretas']} | {r['parciais']} | {r['incorretas']} | {r['sem_nota']} | {acc} |\n")
        return res

    def exportar(self):
        super().exportar()
        rows=linhas(self.saida/'avaliacoes.jsonl')
        for r in rows:
            r['condicao']=self.questoes[r['uid']]['condicao']
            for m in self.respondentes:
                response=read_json(self._arq_resposta(m,r['uid']))
                r['palavras_'+m]=len(response['resposta'].split()) if response and response['resposta'] else None
        C.GeracaoSemConteudo.jsonl(self.saida/'avaliacoes.jsonl',rows)

    def responder_um(self,m,q):
        name='resposta_'+m+'_'+_nome_arq(q['uid'])
        try:
            d=self.cliente('resp_'+m,self.respondentes[m]).json(prompt('respondente'),q['pergunta'],
                tag='resposta_'+m,max_tokens=8000,item=q['item'],validate=base.validar_resposta)
            record=dict(uid=q['uid'],modelo=m,resposta=d['resposta'],status_avaliacao='respondida',
                palavras=len(d['resposta'].split()),acima_limite_solicitado=len(d['resposta'].split())>100)
        except Exception as exc:
            if not _filtrado(exc):
                self._falha(name,exc);return False
            record=dict(uid=q['uid'],modelo=m,resposta=None,status_avaliacao='bloqueio_respondente',
                erro='ContentFiltered',mensagem=str(exc)[:1500])
        atomic_json(self._arq_resposta(m,q['uid']),record)
        self._ok(name)
        with self.lock:
            self.respondidas[m].add(q['uid'])
            n=len(self.respondidas[m])
        if n%10==0:
            self.progress(f'[RESPOSTAS | {m}] {n}/{len(self.questoes)} salvas; julgamento em andamento.',flush=True)
        return True

    def julgar_lote(self,m,rows):
        name='juiz_'+m+'_'+self._lote_nome(m,rows)
        available=[];blocked=[]
        for q in rows:
            r=read_json(self._arq_resposta(m,q['uid']))
            (blocked if r.get('status_avaliacao')=='bloqueio_respondente' else available).append(q)
        if blocked:
            self._registrar(m,blocked,[dict(uid=q['uid'],veredito=None,status_avaliacao='bloqueio_respondente',
                justificativa='Bloqueio do provedor; sem nota técnica.') for q in blocked])
        if available:
            ids=[f'Q{i}' for i in range(1,len(available)+1)]
            payload=[dict(id=i,pergunta=q['pergunta'],resposta_referencia=q['resposta'],
                resposta_candidato=read_json(self._arq_resposta(m,q['uid']))['resposta']) for i,q in zip(ids,available)]
            try:
                d=self.cliente('juiz',self.juiz).json(prompt('juiz'),json.dumps(payload,ensure_ascii=False),
                    tag='juiz_respostas',max_tokens=8000,validate=lambda d:validar_juiz(d,ids))
                decisions=[dict(uid=q['uid'],veredito=a['veredito'],status_avaliacao='julgada',
                    justificativa=a.get('justificativa','')) for q,a in zip(available,d['avaliacoes'])]
            except Exception as exc:
                if not _filtrado(exc):
                    self._falha(name,exc);return False
                decisions=[dict(uid=q['uid'],veredito=None,status_avaliacao='bloqueio_juiz',
                    justificativa='Lote bloqueado; sem nota técnica.',erro='ContentFiltered',mensagem=str(exc)[:1500]) for q in available]
            self._registrar(m,available,decisions)
        self._ok(name)
        return True

    def passagem(self,final=True):
        self.questoes=self.carregar_questoes()
        ready={m:[] for m in self.respondentes}
        for m in self.respondentes:
            for q in self.questoes.values():
                if self._arq_resposta(m,q['uid']).exists():
                    self.respondidas[m].add(q['uid'])
                    if q['uid'] not in self.vereditos[m]:ready[m].append(q)
        self.tabela()
        failures=0
        with ThreadPoolExecutor(max_workers=self.workers) as rp, ThreadPoolExecutor(max_workers=self.judge_workers) as jp:
            pending={rp.submit(self.responder_um,m,q):('resposta',m,q)
                for q in self.questoes.values() for m in self.respondentes if not self._arq_resposta(m,q['uid']).exists()}
            def dispatch(final=False):
                for m in ready:
                    while len(ready[m])>=self.lote_juiz or (final and ready[m]):
                        batch=ready[m][:self.lote_juiz];del ready[m][:len(batch)]
                        pending[jp.submit(self.julgar_lote,m,batch)]=('juiz',m,None)
            dispatch(not any(kind=='resposta' for kind,_,_ in pending.values()))
            while pending:
                if not any(kind=='resposta' for kind,_,_ in pending.values()):dispatch(True)
                done,_=wait(list(pending),timeout=15,return_when=FIRST_COMPLETED)
                if not done:
                    self.progress('[EM ANDAMENTO] Aguardando respostas/julgamentos; acurácia disponível em avaliacao/acuracia.json.',flush=True)
                for future in done:
                    kind,m,q=pending.pop(future)
                    try:ok=future.result()
                    except Exception as exc:
                        self._falha('fluxo_'+m+('_'+_nome_arq(q['uid']) if q else ''),exc);ok=False
                    if not ok:failures+=1
                    elif kind=='resposta':ready[m].append(q)
                dispatch(not any(kind=='resposta' for kind,_,_ in pending.values()))
        self.tabela();self.exportar()
        return failures


def avaliar(saida=SAIDA,*,manifesto=MANIFESTO,workers=8,judge_workers=2,lote_juiz=8,clientes=None,progress=print):
    if min(workers,judge_workers,lote_juiz)<1:raise ValueError('Limites devem ser positivos')
    data,rows=carregar(manifesto)
    saida=Path(saida)
    # Não escreve em nenhuma das runs de origem.
    for cond in data['condicoes']:
        for source in cond['fontes']:
            path=Path(source['path']);path=path if path.is_absolute() else C.ROOT/path
            if saida.resolve()==path.parent.resolve() or path.parent.resolve() in saida.resolve().parents:
                raise ValueError('Escolha saída fora das fontes')
    cfg=dict(schema='qa-100-medium-v1',amostras_sha256=C.sha(data),questoes_sha256=C.sha(rows),
        respondentes=RESPONDENTES,juiz=JUIZ,lote_juiz=lote_juiz,max_palavras=100,
        prompt_respondente_sha256=C.sha(prompt('respondente')),prompt_juiz_sha256=C.sha(prompt('juiz')),
        codigo_sha256=C.sha(Path(__file__).read_text(encoding='utf-8')),
        motor_sha256=C.sha(Path(motor.__file__).read_text(encoding='utf-8')),
        bloqueios_sha256=C.sha(Path(bloqueios.__file__).read_text(encoding='utf-8')),
        base_sha256=C.sha(Path(base.__file__).read_text(encoding='utf-8')))
    with output_lock(saida):
        old=read_json(saida/'config.json')
        if old is not None and old!=cfg:raise ValueError('Configuração mudou: use outra saída')
        if old is None and (saida/'avaliacao').exists():raise ValueError('Avaliação sem protocolo: use outra saída')
        target=saida/'questoes.jsonl'
        if target.exists() and linhas(target)!=rows:raise ValueError('Questões salvas alteradas')
        atomic_json(saida/'config.json',cfg);atomic_json(saida/'amostras.json',data)
        if not target.exists():C.GeracaoSemConteudo.jsonl(target,rows)
        directory=saida/'avaliacao'
        with output_lock(directory):
            pp=directory/'protocolo_experimento.json'
            if pp.exists() and read_json(pp)!=cfg:raise ValueError('Protocolo de avaliação mudou')
            atomic_json(pp,cfg)
            for m in RESPONDENTES:
                for name in ('respostas','juiz'):(directory/name/m).mkdir(parents=True,exist_ok=True)
            (directory/'falhas').mkdir(parents=True,exist_ok=True)
            marker=directory/'avaliacao_concluida.json';marker.unlink(missing_ok=True)
            (directory/'falha_execucao.json').unlink(missing_ok=True)
            e=AvaliacaoQA(saida,respondentes=RESPONDENTES,juiz=JUIZ,grupos=[tuple(RESPONDENTES)],
                workers=max(2,workers),judge_workers=judge_workers,lote_juiz=lote_juiz,clientes=clientes,progress=progress)
            try:
                failures=e.run()
                summary=read_json(directory/'acuracia.json')
                if C.sha(linhas(target))!=cfg['questoes_sha256']:raise RuntimeError('Banco alterado durante avaliação')
                complete=all(summary['geral'][m]['processadas']==len(rows) and
                    all(e._arq_resposta(m,q['uid']).exists() for q in rows) for m in RESPONDENTES)
                if complete:
                    atomic_json(marker,dict(em=C.agora(),questoes=len(rows),questoes_sha256=cfg['questoes_sha256'],
                        status='concluida_com_bloqueios' if any(d['nao_avaliadas'] for d in summary['geral'].values()) else 'concluida',
                        por_condicao=summary['por_condicao'],falhas_transitorias=failures))
                return 0 if complete else 2
            except Exception as exc:
                atomic_json(directory/'falha_execucao.json',dict(erro=type(exc).__name__,mensagem=str(exc)[:1500]));return 2
            finally:
                for c in e.clientes.values():
                    if hasattr(c,'close'):c.close()


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--saida',type=Path,default=SAIDA)
    p.add_argument('--manifesto',type=Path,default=MANIFESTO)
    p.add_argument('--workers',type=int,default=8)
    p.add_argument('--judge-workers',type=int,default=2)
    p.add_argument('--lote-juiz',type=int,default=8)
    p.add_argument('--plano',action='store_true')
    a=p.parse_args(argv);data,rows=carregar(a.manifesto)
    print('Condições: '+', '.join(f"{c['rotulo']} ({c['n']})" for c in data['condicoes']),flush=True)
    print('Respondentes medium; até 100 palavras. Juiz medium com rubrica revisada. Apenas perguntas são enviadas aos respondentes.',flush=True)
    print(f'Saída: {a.saida}',flush=True)
    if a.plano:
        print(f'Plano sem API e sem criar saída: {len(rows)*2} respostas, mais julgamentos.');return 0
    return avaliar(a.saida,manifesto=a.manifesto,workers=a.workers,judge_workers=a.judge_workers,lote_juiz=a.lote_juiz)
