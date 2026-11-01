"""Todos os QAs próprios: gap open/closed-book e sustentação dos gabaritos."""
import argparse
import csv
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.qa_medium import core as Q
from pipeline.qa_research.piloto_janela.core import DOCS, blocos, janela

HERE=Path(__file__).resolve().parent/'benchmark_gap_prompts'
SOURCE=Q.C.ROOT/'pipeline/qa_research/relatorios/geracao_final_20261024T204734Z/aprovadas.jsonl'
OUT=Q.C.ROOT/'pipeline/qa_research/relatorios/benchmark_gap_full_v1'
MODELS={'gpt-4-1-nano':'gpt-4-1-nano-petrobras','gpt-4-1-mini':'gpt-4-1-mini-petrobras','gpt-4-1':'gpt-4-1-petrobras'}
ARMS=('closed_book','open_book')


def prompt(name):return (HERE/(name+'.md')).read_text(encoding='utf-8').strip()


def carregar(source=SOURCE,docs=DOCS):
    original=Q.linhas(source)
    if not original or len({q['uid'] for q in original})!=len(original):raise ValueError('Banco vazio ou UIDs repetidos')
    cache={i:blocos(i,Path(docs)) for i in {q['item'] for q in original}}
    enriched=[];rows=[]
    for q in original:
        doc,bs=cache[q['item']]
        if q.get('foco') is not None:
            selected=[b for _,b in janela(bs,q['foco'])]
        elif q.get('blocos'):
            ids=q['blocos']
            if len(set(ids))!=len(ids) or any(type(i) is not int or i<0 or i>=len(bs) for i in ids):raise ValueError('Índice de bloco inválido')
            selected=[bs[i] for i in ids]
        else:raise ValueError('Questão sem vínculo de contexto: '+q['uid'])
        text='\n\n'.join(f"{b['titulo_capitulo']} / {b['subtitulo']}\n{b['texto']}" for b in selected)
        enriched.append({**q,'contexto_tecnico':text,'blocos_contexto':[
            dict(id=f'B{k}',texto=b['texto'],indice_documento=b['indice']) for k,b in enumerate(selected,1)]})
        for arm in ARMS:
            rows.append({**q,'uid_original':q['uid'],'uid':arm+':'+q['uid'],'condicao':arm,
                'contexto_tecnico':text if arm=='open_book' else None})
    return enriched,rows


def validar_faithfulness(d,blocks):
    if not isinstance(d,dict) or set(d)!={'cobertura_completa','afirmacoes','observacoes'}:raise ValueError('Esquema de sustentação inválido')
    if type(d['cobertura_completa']) is not bool or not isinstance(d['observacoes'],str):raise ValueError('Cobertura/observações inválidas')
    if not isinstance(d['afirmacoes'],list) or not d['afirmacoes']:raise ValueError('Decomponha o gabarito em afirmações')
    for a in d['afirmacoes']:
        if not isinstance(a,dict) or set(a)!={'afirmacao','veredito','evidencias','justificativa'}:raise ValueError('Afirmação inválida')
        if any(not isinstance(a[k],str) or not a[k].strip() for k in ('afirmacao','justificativa')):raise ValueError('Texto obrigatório')
        if a['veredito'] not in ('sustentada','contradita','insuficiente'):raise ValueError('Veredito inválido')
        if not isinstance(a['evidencias'],list):raise ValueError('Evidências devem ser lista')
        if a['veredito'] in ('sustentada','contradita') and not a['evidencias']:raise ValueError('Exige evidência literal')
        for e in a['evidencias']:
            if not isinstance(e,dict) or set(e)!={'bloco','trecho'} or e['bloco'] not in blocks:raise ValueError('Bloco inexistente')
            if not isinstance(e['trecho'],str) or not e['trecho'].strip() or e['trecho'] not in blocks[e['bloco']]:raise ValueError('Trecho não literal no bloco')


def resumo_faithfulness(d):
    counts={v:sum(a['veredito']==v for a in d['afirmacoes']) for v in ('sustentada','contradita','insuficiente')}
    status=('inconclusivo' if not d['cobertura_completa'] else
        'contradicao' if counts['contradita'] else 'suporte_insuficiente' if counts['insuficiente'] else 'totalmente_sustentado')
    return dict(status=status,afirmacoes=len(d['afirmacoes']),**counts,
        fracao_sustentada=counts['sustentada']/len(d['afirmacoes']))


class AvaliacaoGap(Q.AvaliacaoQA):
    def _markdown(self,res):
        super()._markdown(res)
        p=self.saida/'ACURACIA.md'
        p.write_text(p.read_text(encoding='utf-8').replace('Respondentes com esforço medium e limite solicitado de 100 palavras.',
            'GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.'),encoding='utf-8')

    def checar_modelos(self):
        for m,alias in self.respondentes.items():
            self.progress(f'[DISPONIBILIDADE] {m}: {alias}',flush=True)
            self.cliente('resp_'+m,alias).json(prompt('respondente'),
                json.dumps(dict(pergunta='Qual a função de um separador trifásico?',contexto=None),ensure_ascii=False),
                tag='teste_'+m,max_tokens=8000,validate=Q.base.validar_resposta)

    def responder_um(self,m,q):
        name='resposta_'+m+'_'+Q._nome_arq(q['uid'])
        try:
            data=self.cliente('resp_'+m,self.respondentes[m]).json(prompt('respondente'),
                json.dumps(dict(pergunta=q['pergunta'],contexto=q['contexto_tecnico']),ensure_ascii=False),
                tag='resposta_'+m,max_tokens=8000,item=q['item'],validate=Q.base.validar_resposta)
            record=dict(uid=q['uid'],modelo=m,resposta=data['resposta'],status_avaliacao='respondida',
                palavras=len(data['resposta'].split()),acima_limite_solicitado=len(data['resposta'].split())>100)
        except Exception as exc:
            if not Q._filtrado(exc):self._falha(name,exc);return False
            record=dict(uid=q['uid'],modelo=m,resposta=None,status_avaliacao='bloqueio_respondente',erro='ContentFiltered')
        atomic_json(self._arq_resposta(m,q['uid']),record);self._ok(name)
        with self.lock:self.respondidas[m].add(q['uid'])
        return True

    def julgar_lote(self,m,rows):
        # Separação ANTES de qualquer chamada: variantes da mesma questão não são comparadas juntas.
        ok=True
        for arm in ARMS:
            group=[q for q in rows if q['condicao']==arm]
            if group:ok=super().julgar_lote(m,group) and ok
        return ok


def salvar_csv(path,rows):
    if not rows:return
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def exportar_gap(directory,models):
    rows=Q.linhas(directory/'avaliacao/avaliacoes.jsonl');byid={q['uid']:q for q in rows}
    original=sorted({q['uid_original'] for q in Q.linhas(directory/'questoes.jsonl')})
    # A exportação histórica não copia uid_original: recuperar pelo prefixo preservado.
    byoriginal={(q['condicao'],q['uid'].split(':',1)[1]):q for q in rows}
    summary=[];pairs=[]
    for m in models:
        common=[u for u in original if all(byoriginal[a,u]['veredito_'+m] is not None for a in ARMS)]
        def correct(a):return sum(byoriginal[a,u]['veredito_'+m]=='correta' for u in common)
        wins=sum(byoriginal['closed_book',u]['veredito_'+m]!='correta' and byoriginal['open_book',u]['veredito_'+m]=='correta' for u in common)
        losses=sum(byoriginal['closed_book',u]['veredito_'+m]=='correta' and byoriginal['open_book',u]['veredito_'+m]!='correta' for u in common)
        summary.append(dict(modelo=m,total=len(original),pares_com_nota=len(common),sem_par=len(original)-len(common),
            acuracia_closed=100*correct('closed_book')/len(common) if common else None,
            acuracia_open=100*correct('open_book')/len(common) if common else None,
            gap_pp=100*(wins-losses)/len(common) if common else None,ganhos=wins,perdas=losses))
        for u in original:
            pair=dict(uid=u,modelo=m,pergunta=byoriginal['closed_book',u]['pergunta'])
            for a in ARMS:
                q=byoriginal[a,u]
                pair['resposta_'+a]=q['resposta_'+m];pair['veredito_'+a]=q['veredito_'+m]
                pair['status_'+a]=q['status_avaliacao_'+m]
            pairs.append(pair)
    salvar_csv(directory/'gap_pareado.csv',summary);salvar_csv(directory/'pares.csv',pairs)


def faithfulness(e,original):
    directory=e.rodada/'faithfulness';directory.mkdir(exist_ok=True)
    def one(q):
        path=directory/(Q._nome_arq(q['uid'])+'.json')
        if path.exists():return True
        name='faithfulness_'+Q._nome_arq(q['uid'])
        try:
            blocks={b['id']:b['texto'] for b in q['blocos_contexto']}
            d=e.cliente('faithfulness',Q.JUIZ).json(prompt('faithfulness'),json.dumps(dict(
                pergunta=q['pergunta'],gabarito=q['resposta'],blocos=q['blocos_contexto']),ensure_ascii=False),
                tag='faithfulness',max_tokens=12000,item=q['item'],validate=lambda d:validar_faithfulness(d,blocks))
            record=dict(uid=q['uid'],avaliacao=d,**resumo_faithfulness(d))
        except Exception as exc:
            if not Q._filtrado(exc):e._falha(name,exc);return False
            record=dict(uid=q['uid'],status='bloqueio_provedor',erro='ContentFiltered')
        atomic_json(path,record);e._ok(name)
        return True
    with ThreadPoolExecutor(max_workers=e.workers) as pool:
        for n,f in enumerate(as_completed([pool.submit(one,q) for q in original]),1):
            f.result()
            if n%10==0:e.progress(f'[SUSTENTAÇÃO] {n}/{len(original)} processadas nesta passagem',flush=True)
    records=[read_json(directory/(Q._nome_arq(q['uid'])+'.json')) for q in original]
    records=[r for r in records if r]
    Q.C.GeracaoSemConteudo.jsonl(e.rodada/'faithfulness.jsonl',records)
    evaluated=[r for r in records if r['status']!='bloqueio_provedor']
    complete=[r for r in evaluated if r['status']!='inconclusivo']
    atomic_json(e.rodada/'faithfulness_resumo.json',dict(total=len(original),processadas=len(records),
        por_status=dict(Counter(r['status'] for r in records)),
        afirmacoes_em_gabaritos_com_decisao={k:sum(r[k] for r in complete) for k in ('afirmacoes','sustentada','contradita','insuficiente')},
        bloqueadas=len(records)-len(evaluated),inconclusivas=len(evaluated)-len(complete),com_decisao=len(complete),
        totalmente_sustentadas=sum(r['status']=='totalmente_sustentado' for r in complete),
        taxa_totalmente_sustentadas=sum(r['status']=='totalmente_sustentado' for r in complete)/len(complete) if complete else None,
        pendentes=len(original)-len(records),metodo='Auditoria automática adicional, não validação humana independente.'))
    # Amostra determinística por resultado; não é amostra uniforme, conservar estratos para análise.
    candidates=[]
    for status in sorted({r['status'] for r in evaluated}):
        selected=sorted((r for r in evaluated if r['status']==status),key=lambda r:Q.C.sha(r['uid']))[:25]
        for r in selected:
            q=next(q for q in original if q['uid']==r['uid'])
            candidates.append(dict(uid=r['uid'],estrato=status,pergunta=q['pergunta'],gabarito=q['resposta'],
                contexto=q['contexto_tecnico'],auditoria=json.dumps(r['avaliacao'],ensure_ascii=False),parecer_humano='',observacao_humana=''))
    salvar_csv(e.rodada/'amostra_revisao_humana.csv',candidates)
    return len(records)==len(original)


def executar(saida=OUT,source=SOURCE,docs=DOCS,workers=8,judge_workers=2,mini=MODELS['gpt-4-1-mini'],clientes=None,progress=print):
    if workers<1 or judge_workers<1:raise ValueError('Workers positivos obrigatórios')
    original,rows=carregar(source,docs);saida=Path(saida)
    for protected in (Path(source).parent,Path(docs)):
        if saida.resolve()==protected.resolve() or protected.resolve() in saida.resolve().parents:raise ValueError('Saída deve ficar fora das fontes')
    if prompt('juiz')!=Q.prompt('juiz'):raise ValueError('Juiz congelado diverge do motor; não misturar protocolos')
    models={**MODELS,'gpt-4-1-mini':mini}
    if not mini.strip() or ':' in mini:raise ValueError('Informe deployment do GPT-4.1 Mini, sem effort')
    cfg=dict(schema='benchmark-gap-full-v1',n=len(original),dados_sha256=Q.C.sha(original),questoes_sha256=Q.C.sha(rows),
        modelos=models,juiz=Q.JUIZ,limite_palavras=100,lote_juiz=8,fonte=str(Path(source).resolve().relative_to(Q.C.ROOT)) if Q.C.ROOT in Path(source).resolve().parents else 'fixture',
        tokens_iniciais_resposta_juiz=8000,tokens_iniciais_faithfulness=12000,max_tokens_cap=16000,
        prompts={n:Q.C.sha(prompt(n)) for n in ('respondente','juiz','faithfulness')},
        codigo=Q.C.sha(Path(__file__).read_text(encoding='utf-8')),
        dependencias={n:Q.C.sha(Path(m.__file__).read_text(encoding='utf-8')) for n,m in [('core',Q),('motor',Q.motor),('base',Q.base),('bloqueios',Q.bloqueios)]})
    with output_lock(saida):
        old=read_json(saida/'config.json')
        if old is not None and old!=cfg:raise ValueError('Protocolo ou dados mudaram; use outra saída')
        if old is None and (saida/'avaliacao').exists():raise ValueError('Pasta sem protocolo, use outra saída')
        if (saida/'questoes.jsonl').exists() and Q.linhas(saida/'questoes.jsonl')!=rows:raise ValueError('Questões salvas alteradas')
        atomic_json(saida/'config.json',cfg)
        Q.C.GeracaoSemConteudo.jsonl(saida/'questoes.jsonl',rows)
        Q.C.GeracaoSemConteudo.jsonl(saida/'contextos.jsonl',original)
        directory=saida/'avaliacao'
        with output_lock(directory):
            atomic_json(directory/'protocolo_experimento.json',cfg)
            for m in models:
                for sub in ('respostas','juiz'):(directory/sub/m).mkdir(parents=True,exist_ok=True)
            (directory/'falhas').mkdir(exist_ok=True)
            marker=saida/'rodada_concluida.json';marker.unlink(missing_ok=True)
            (saida/'falha_execucao.json').unlink(missing_ok=True)
            e=AvaliacaoGap(saida,respondentes=models,juiz=Q.JUIZ,grupos=[tuple(models)],workers=workers,
                judge_workers=judge_workers,lote_juiz=8,clientes=clientes,progress=progress)
            try:
                e.run()
                exportar_gap(saida,models)
                qa_done=all(len(e.vereditos[m])==len(rows) for m in models)
                faithful_done=faithfulness(e,original)
                if qa_done and faithful_done:
                    atomic_json(marker,dict(status='concluida',questoes=len(original),casos_resposta=len(rows)*len(models),
                        dados_sha256=cfg['dados_sha256'],observacao='Bloqueios são resultados terminais sem nota; consultar cobertura.'))
                return 0 if qa_done and faithful_done else 2
            except Exception as exc:
                atomic_json(saida/'falha_execucao.json',dict(erro=type(exc).__name__,mensagem=str(exc)[:1500]))
                progress(f'[INCOMPLETA] {type(exc).__name__}: {exc}',flush=True);return 2
            finally:
                for c in e.clientes.values():
                    if hasattr(c,'close'):c.close()


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--saida',type=Path,default=OUT)
    p.add_argument('--workers',type=int,default=8);p.add_argument('--judge-workers',type=int,default=2)
    p.add_argument('--mini-deployment',default=MODELS['gpt-4-1-mini'])
    p.add_argument('--plano',action='store_true')
    a=p.parse_args(argv);original,rows=carregar()
    print(f'TODAS as {len(original)} QAs do Default: {len(rows)*3} casos de resposta, mais julgamentos e {len(original)} auditorias de sustentação.',flush=True)
    print(f'Mini: {a.mini_deployment}. Saída: {a.saida}',flush=True)
    if a.plano:print('Sem API e sem criar saída.');return 0
    return executar(a.saida,workers=a.workers,judge_workers=a.judge_workers,mini=a.mini_deployment)


if __name__=='__main__':raise SystemExit(main())
