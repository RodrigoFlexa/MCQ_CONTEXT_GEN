"""Ablação de extensão: 50, 100 e concisa livre, mesmos itens, medium e juiz fixo."""
import argparse
import copy
import csv
import statistics
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from . import core as Q

HERE=Path(__file__).resolve().parent
SAIDA=Q.C.ROOT/'pipeline/qa_research/relatorios/qa_exploratoria_limites_medium_1000'
REFERENCIA=Q.SAIDA
BRACOS={'p50':50,'p100':100,'concisa_livre':None}


def prompt_resposta(braco):
    if braco not in BRACOS:raise ValueError('Braço desconhecido')
    template=(HERE/'prompts/respondente_exploratorio.md').read_text(encoding='utf-8').strip()
    limit=BRACOS[braco]
    regra=f'com até {limit} palavras.' if limit else 'sem um limite numérico de palavras.'
    complemento='sem preencher\no limite com conteúdo opcional.' if limit else 'sem acrescentar conteúdo opcional.'
    return template.replace('{{REGRA_TAMANHO}}',regra).replace('{{CONCISAO}}',complemento)


def prompt_juiz():
    return (HERE/'prompts/juiz_exploratorio.md').read_text(encoding='utf-8').strip()


def carregar(manifesto=Q.MANIFESTO):
    data,originais=Q.carregar(manifesto)
    # Os únicos trechos que variam entre prompts são as instruções de extensão.
    if prompt_resposta('p100')!=Q.prompt('respondente') or prompt_juiz()!=Q.prompt('juiz'):
        raise ValueError('Prompts de referência mudaram; não misturar a ablação com a rodada anterior')
    rows=[]
    for q in originais:
        for braco,limite in BRACOS.items():
            rows.append({**q,'uid_original':q['uid'],'uid':f"{braco}:{q['uid']}",
                'conjunto':q['condicao'],'braco':braco,'limite_palavras':limite,
                'condicao':f"{q['condicao']} / {braco}"})
    assert len({q['uid'] for q in rows})==len(rows)
    return data,originais,rows


def referencia_100(path,data,originais):
    """Confere os checkpoints reais antes de reaproveitar; não chama modelos."""
    path=Path(path)
    cfg=read_json(path/'config.json') or {}
    marker=read_json(path/'avaliacao/avaliacao_concluida.json') or {}
    expected=dict(amostras_sha256=Q.C.sha(data),questoes_sha256=Q.C.sha(originais),
        respondentes=Q.RESPONDENTES,juiz=Q.JUIZ,lote_juiz=8,max_palavras=100,
        prompt_respondente_sha256=Q.C.sha(prompt_resposta('p100')),
        prompt_juiz_sha256=Q.C.sha(prompt_juiz()))
    if any(cfg.get(k)!=v for k,v in expected.items()):
        raise ValueError('Referência 100 incompatível: itens, modelos, esforço, prompts ou lote do juiz mudaram')
    if marker.get('status') not in ('concluida','concluida_com_bloqueios') or marker.get('questoes_sha256')!=expected['questoes_sha256']:
        raise ValueError('A rodada de 100 palavras precisa estar concluída')
    if Q.linhas(path/'questoes.jsonl')!=originais:
        raise ValueError('Questões da referência foram alteradas')
    exported=Q.linhas(path/'avaliacao/avaliacoes.jsonl')
    byid={q['uid']:q for q in exported}
    if len(exported)!=len(originais) or set(byid)!={q['uid'] for q in originais}:
        raise ValueError('Exportação da referência incompleta')
    responses={};batches=[]
    for m in Q.RESPONDENTES:
        judged={}
        for file in sorted((path/'avaliacao/juiz'/m).glob('*.json')):
            d=read_json(file)
            for item in d['avaliacoes']:
                if item['uid'] in judged:raise ValueError('Julgamentos duplicados na referência')
                judged[item['uid']]=item
            batches.append((m,copy.deepcopy(d)))
        if set(judged)!=set(byid):raise ValueError('Julgamentos da referência incompletos')
        for q in originais:
            u=q['uid'];r=read_json(path/'avaliacao/respostas'/m/(Q._nome_arq(u)+'.json'))
            if not r or r.get('uid')!=u or r.get('modelo')!=m or r.get('resposta')!=byid[u].get('resposta_'+m):
                raise ValueError('Resposta da referência inconsistente')
            if judged[u]['veredito']!=byid[u].get('veredito_'+m):raise ValueError('Nota da referência inconsistente')
            for k in ('pergunta','resposta','item','tipo','composicao','condicao'):
                if byid[u][k]!=q[k]:raise ValueError('Texto ou classificação da referência mudou')
            responses[(m,u)]=copy.deepcopy(r)
    proof=dict(config_sha256=Q.C.sha(cfg),questoes_sha256=expected['questoes_sha256'],
        respostas=len(responses),julgamentos=sum(len(d['avaliacoes']) for _,d in batches),
        respostas_sha256=Q.C.sha([responses[k] for k in sorted(responses)]),lotes_sha256=Q.C.sha(batches))
    return proof,responses,batches


def semear(saida,responses,batches,proof):
    directory=Path(saida)/'avaliacao'
    actions=[]
    for (m,u),r in responses.items():
        r={**r,'uid':'p100:'+u,'reaproveitada':True,'uid_original':u}
        actions.append((directory/'respostas'/m/(Q._nome_arq(r['uid'])+'.json'),r))
    for m,d in batches:
        d=copy.deepcopy(d)
        for a in d['avaliacoes']:a['uid']='p100:'+a['uid']
        name=Q.AvaliacaoQA._lote_nome(m,d['avaliacoes'])
        actions.append((directory/'juiz'/m/(name+'.json'),{**d,'reaproveitado':True}))
    # Confere conflitos antes de semear arquivos. Retomada pode completar uma cópia interrompida.
    for p,d in actions:
        old=read_json(p)
        if old is not None and old!=d:raise ValueError('Conflito com checkpoint do braço de 100 palavras')
    for p,d in actions:
        if not p.exists():atomic_json(p,d)
    atomic_json(directory/'reaproveitamento_p100.json',proof)


class AvaliacaoExploratoria(Q.AvaliacaoQA):
    def _markdown(self,res):
        super()._markdown(res)
        p=self.saida/'ACURACIA.md'
        p.write_text(p.read_text(encoding='utf-8').replace(
            'Respondentes com esforço medium e limite solicitado de 100 palavras.',
            'Respondentes medium; braços 50, 100 e concisa livre; mesmo juiz em todos.'),encoding='utf-8')

    def responder_um(self,m,q):
        name='resposta_'+m+'_'+Q._nome_arq(q['uid'])
        try:
            d=self.cliente('resp_'+m,self.respondentes[m]).json(prompt_resposta(q['braco']),q['pergunta'],
                tag='resposta_'+m,max_tokens=8000,item=q['item'],validate=Q.base.validar_resposta)
            n=len(d['resposta'].split());limit=q['limite_palavras']
            record=dict(uid=q['uid'],uid_original=q['uid_original'],modelo=m,braco=q['braco'],
                resposta=d['resposta'],status_avaliacao='respondida',palavras=n,reaproveitada=False,
                acima_limite_solicitado=n>limit if limit is not None else False)
        except Exception as exc:
            if not Q._filtrado(exc):self._falha(name,exc);return False
            record=dict(uid=q['uid'],uid_original=q['uid_original'],modelo=m,braco=q['braco'],resposta=None,
                status_avaliacao='bloqueio_respondente',erro='ContentFiltered',mensagem=str(exc)[:1500],reaproveitada=False)
        atomic_json(self._arq_resposta(m,q['uid']),record);self._ok(name)
        with self.lock:
            self.respondidas[m].add(q['uid']);n=len(self.respondidas[m])
        if n%10==0:self.progress(f'[RESPOSTAS | {m}] {n}/{len(self.questoes)} salvas; julgamentos em paralelo.',flush=True)
        return True

    def passagem(self,final=True):
        self.questoes=self.carregar_questoes()
        # O juiz não recebe variantes da mesma pergunta no mesmo lote.
        ready={(m,b):[] for m in self.respondentes for b in BRACOS}
        for m in self.respondentes:
            for q in self.questoes.values():
                if self._arq_resposta(m,q['uid']).exists():
                    self.respondidas[m].add(q['uid'])
                    if q['uid'] not in self.vereditos[m]:ready[(m,q['braco'])].append(q)
        self.tabela();failures=0
        with ThreadPoolExecutor(max_workers=self.workers) as rp,ThreadPoolExecutor(max_workers=self.judge_workers) as jp:
            pending={rp.submit(self.responder_um,m,q):('resposta',m,q) for q in self.questoes.values()
                for m in self.respondentes if not self._arq_resposta(m,q['uid']).exists()}
            def dispatch(final=False):
                for (m,b),qs in ready.items():
                    while len(qs)>=self.lote_juiz or (final and qs):
                        batch=qs[:self.lote_juiz];del qs[:len(batch)]
                        pending[jp.submit(self.julgar_lote,m,batch)]=('juiz',m,None)
            dispatch(not pending)
            while pending:
                if not any(k=='resposta' for k,_,_ in pending.values()):dispatch(True)
                done,_=wait(list(pending),timeout=15,return_when=FIRST_COMPLETED)
                if not done:self.progress('[EM ANDAMENTO] Aguardando respostas/julgamentos; checkpoints preservados.',flush=True)
                for f in done:
                    kind,m,q=pending.pop(f)
                    try:ok=f.result()
                    except Exception as exc:
                        self._falha('fluxo_'+m+('_'+Q._nome_arq(q['uid']) if q else ''),exc);ok=False
                    if not ok:failures+=1
                    elif kind=='resposta':ready[(m,q['braco'])].append(q)
                dispatch(not any(k=='resposta' for k,_,_ in pending.values()))
        self.tabela();self.exportar();return failures

    def exportar(self):
        super().exportar()
        path=self.saida/'avaliacoes.jsonl';rows=Q.linhas(path)
        notas={m:{} for m in self.respondentes}
        for m in notas:
            for p in (self.saida/'juiz'/m).glob('*.json'):
                for a in read_json(p)['avaliacoes']:notas[m][a['uid']]=a
        for r in rows:
            q=self.questoes[r['uid']]
            for key in ('uid_original','conjunto','braco','limite_palavras'):r[key]=q[key]
            for m in self.respondentes:
                rec=read_json(self._arq_resposta(m,r['uid'])) or {}
                r['reaproveitada_'+m]=rec.get('reaproveitada',False)
                r['justificativa_'+m]=notas[m].get(r['uid'],{}).get('justificativa')
        Q.C.GeracaoSemConteudo.jsonl(path,rows)
        resumo=[];pares=[]
        bykey={(r['conjunto'],r['braco'],r['uid_original']):r for r in rows}
        for conjunto in sorted({r['conjunto'] for r in rows}):
            for braco,limite in BRACOS.items():
                qs=[r for r in rows if r['conjunto']==conjunto and r['braco']==braco]
                for m in self.respondentes:
                    grades=[r['veredito_'+m] for r in qs if r['veredito_'+m] is not None]
                    words=[r['palavras_'+m] for r in qs if r['palavras_'+m] is not None]
                    resumo.append(dict(conjunto=conjunto,braco=braco,modelo=m,total=len(qs),julgadas=len(grades),
                        sem_nota=len(qs)-len(grades),corretas=grades.count('correta'),parciais=grades.count('parcial'),
                        incorretas=grades.count('incorreta'),acuracia=100*grades.count('correta')/len(grades) if grades else None,
                        palavras_media=statistics.mean(words) if words else None,palavras_max=max(words) if words else None,
                        acima_limite=sum(n>limite for n in words) if limite is not None else None,
                        reaproveitadas=sum(r['reaproveitada_'+m] for r in qs)))
            # Comparação comum: exatamente as mesmas questões com nota nos três braços.
            ids={r['uid_original'] for r in rows if r['conjunto']==conjunto}
            for m in self.respondentes:
                common=[u for u in sorted(ids) if all(bykey[(conjunto,b,u)]['veredito_'+m] is not None for b in BRACOS)]
                for b in BRACOS:
                    vs=[bykey[(conjunto,b,u)]['veredito_'+m] for u in common]
                    pares.append(dict(conjunto=conjunto,braco=b,modelo=m,n_comum=len(common),
                        acuracia=100*vs.count('correta')/len(vs) if vs else None))
        for name,data in [('resumo_exploratorio.csv',resumo),('comparacao_mesmas_questoes.csv',pares)]:
            with (self.saida/name).open('w',encoding='utf-8-sig',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)


def avaliar(saida=SAIDA,*,manifesto=Q.MANIFESTO,referencia=REFERENCIA,workers=8,judge_workers=2,clientes=None,progress=print):
    if min(workers,judge_workers)<1:raise ValueError('Workers devem ser positivos')
    data,originais,rows=carregar(manifesto)
    proof,responses,batches=referencia_100(referencia,data,originais)
    saida=Path(saida);referencia=Path(referencia)
    protected=[referencia]+[Path(s['path']) if Path(s['path']).is_absolute() else Q.C.ROOT/s['path'] for c in data['condicoes'] for s in c['fontes']]
    for p in protected:
        p=p.parent if p.is_file() else p
        if saida.resolve()==p.resolve() or p.resolve() in saida.resolve().parents:raise ValueError('Use outra saída fora das fontes/referência')
    cfg=dict(schema='qa-exploratoria-limites-v1',questoes_sha256=Q.C.sha(rows),manifesto_sha256=Q.C.sha(data),
        respondentes=Q.RESPONDENTES,juiz=Q.JUIZ,lote_juiz=8,bracos=BRACOS,
        prompts_sha256={b:Q.C.sha(prompt_resposta(b)) for b in BRACOS},juiz_sha256=Q.C.sha(prompt_juiz()),
        referencia_100=proof,inicial_max_tokens=8000,max_tokens_cap=16000,
        codigo_sha256=Q.C.sha(Path(__file__).read_text(encoding='utf-8')),
        motor_sha256=Q.C.sha(Path(Q.__file__).read_text(encoding='utf-8')),
        tabela_sha256=Q.C.sha(Path(Q.motor.__file__).read_text(encoding='utf-8')),
        bloqueios_sha256=Q.C.sha(Path(Q.bloqueios.__file__).read_text(encoding='utf-8')),
        base_sha256=Q.C.sha(Path(Q.base.__file__).read_text(encoding='utf-8')))
    with output_lock(saida):
        old=read_json(saida/'config.json')
        if old is not None and old!=cfg:raise ValueError('Configuração mudou; use outra saída')
        if old is None and (saida/'avaliacao').exists():raise ValueError('Avaliação sem protocolo; use outra saída')
        target=saida/'questoes.jsonl'
        if target.exists() and Q.linhas(target)!=rows:raise ValueError('Questões salvas alteradas')
        atomic_json(saida/'config.json',cfg);atomic_json(saida/'amostras.json',data)
        if not target.exists():Q.C.GeracaoSemConteudo.jsonl(target,rows)
        directory=saida/'avaliacao'
        with output_lock(directory):
            pp=directory/'protocolo_experimento.json'
            if pp.exists() and read_json(pp)!=cfg:raise ValueError('Protocolo mudou')
            atomic_json(pp,cfg)
            for m in Q.RESPONDENTES:
                for name in ('respostas','juiz'):(directory/name/m).mkdir(parents=True,exist_ok=True)
            (directory/'falhas').mkdir(parents=True,exist_ok=True)
            semear(saida,responses,batches,proof)
            marker=directory/'avaliacao_concluida.json';marker.unlink(missing_ok=True)
            (directory/'falha_execucao.json').unlink(missing_ok=True)
            e=AvaliacaoExploratoria(saida,respondentes=Q.RESPONDENTES,juiz=Q.JUIZ,grupos=[tuple(Q.RESPONDENTES)],
                workers=max(2,workers),judge_workers=judge_workers,lote_juiz=8,clientes=clientes,progress=progress)
            try:
                failures=e.run();summary=read_json(directory/'acuracia.json')
                if Q.C.sha(Q.linhas(target))!=cfg['questoes_sha256']:raise RuntimeError('Questões mudaram durante a execução')
                complete=all(summary['geral'][m]['processadas']==len(rows) and all(e._arq_resposta(m,q['uid']).exists() for q in rows) for m in Q.RESPONDENTES)
                if complete:
                    atomic_json(marker,dict(em=Q.C.agora(),questoes=len(rows),questoes_por_braco=len(originais),
                        respostas_reaproveitadas=proof['respostas'],questoes_sha256=cfg['questoes_sha256'],
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
    p.add_argument('--manifesto',type=Path,default=Q.MANIFESTO)
    p.add_argument('--referencia-100',type=Path,default=REFERENCIA)
    p.add_argument('--workers',type=int,default=8)
    p.add_argument('--judge-workers',type=int,default=2)
    p.add_argument('--plano',action='store_true')
    a=p.parse_args(argv);data,original,rows=carregar(a.manifesto)
    proof,_,_=referencia_100(a.referencia_100,data,original)
    print('Amostras: '+', '.join(f"{c['rotulo']} ({c['n']})" for c in data['condicoes']),flush=True)
    print('Braços: 50 palavras, 100 palavras, concisa sem limite numérico. Respondentes medium e juiz fixo.',flush=True)
    print(f"Casos de resposta: {len(rows)*2}; reaproveitados: {proof['respostas']}; novos: {len(rows)*2-proof['respostas']}.",flush=True)
    print(f'Saída: {a.saida}',flush=True)
    if a.plano:print('Plano sem API e sem criação de saída.');return 0
    return avaliar(a.saida,manifesto=a.manifesto,referencia=a.referencia_100,workers=a.workers,judge_workers=a.judge_workers)


if __name__=='__main__':raise SystemExit(main())
