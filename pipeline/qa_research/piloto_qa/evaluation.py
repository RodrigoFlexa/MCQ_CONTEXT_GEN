"""Adapta o benchmark já utilizado; mantém respondentes juiz e limite de 100 palavras."""
import random
from collections import Counter
from pathlib import Path
from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research import benchmark_gap as B
from pipeline.qa_research.v3.runtime import digest
from .generate import jsonl


def rows(path):
    import json
    return [json.loads(s) for s in Path(path).read_text(encoding='utf-8-sig').splitlines() if s.strip()]


def historical(items, n, seed):
    original,_=B.carregar()
    selected=[]
    for item in items:
        pool=sorted([q for q in original if q['item']==item],key=lambda q:digest([seed,q['uid']]))
        if len(pool)<n:raise ValueError('Banco histórico insuficiente: '+item)
        counts=Counter()
        while sum(counts.values())<n:
            pool.sort(key=lambda q:counts[q['tipo']])
            q=pool.pop(0);counts[q['tipo']]+=1
            selected.append(dict(q,uid='historico:'+q['uid'],uid_historico=q['uid'],grupo='historico'))
    return selected


def paired_summary(pairs, metadata, seed, draws=2000):
    groups=sorted({q['grupo'] for q in metadata.values()});models=sorted({p['modelo'] for p in pairs});output=[]
    for group in groups:
        for model in models:
            selected=[p for p in pairs if p['modelo']==model and metadata[p['uid']]['grupo']==group]
            valid=[p for p in selected if all(p['veredito_'+a] in ('correta','parcial','incorreta') for a in B.ARMS)]
            delta=[int(p['veredito_open_book']=='correta')-int(p['veredito_closed_book']=='correta') for p in valid]
            rng=random.Random(seed);bootstrap=sorted(100*sum(rng.choices(delta,k=len(delta)))/len(delta) for _ in range(draws)) if delta else []
            output.append(dict(grupo=group,modelo=model,total=len(selected),pares_validos=len(valid),sem_par=len(selected)-len(valid),
                acuracia_sem_contexto=100*sum(p['veredito_closed_book']=='correta' for p in valid)/len(valid) if valid else None,
                acuracia_com_contexto=100*sum(p['veredito_open_book']=='correta' for p in valid)/len(valid) if valid else None,
                gap_pp=100*sum(delta)/len(delta) if delta else None,
                ic95_gap=[bootstrap[int(.025*(draws-1))],bootstrap[int(.975*(draws-1))]] if bootstrap else None))
    return output


def evaluate(questions, destination, *, seed=20261102, workers=6, judge_workers=2, mini=None, clients=None):
    destination=Path(destination);models={**B.MODELS}
    if mini:models['gpt-4-1-mini']=mini
    ids=[q['uid'] for q in questions]
    if not ids or len(ids)!=len(set(ids)):raise ValueError('Questões vazias ou UIDs repetidos')
    original=[dict(q) for q in questions];paired=[]
    for q in original:
        for arm in B.ARMS:
            paired.append(dict(q,uid=arm+':'+q['uid'],uid_original=q['uid'],condicao=arm,
                contexto_tecnico=q['contexto_tecnico'] if arm=='open_book' else None))
    cfg=dict(schema='piloto-qa-avaliacao-1',dados_sha256=digest(original),models=models,juiz=B.Q.JUIZ,
        prompt_sha256={n:digest(B.prompt(n)) for n in ('respondente','juiz','faithfulness')},limite_palavras=100,
        codigo={name:digest(Path(path).read_text(encoding='utf-8')) for name,path in
                [('adaptador',__file__),('benchmark',B.__file__),('avaliador',B.Q.__file__)]},seed=seed)
    with output_lock(destination):
        saved=read_json(destination/'config.json')
        if saved is not None and saved!=cfg:raise ValueError('Avaliação mudou; escolher nova saída')
        atomic_json(destination/'config.json',cfg);jsonl(destination/'questoes.jsonl',paired);jsonl(destination/'contextos.jsonl',original)
        directory=destination/'avaliacao'
        with output_lock(directory):
            for model in models:
                for sub in ('respostas','juiz'):(directory/sub/model).mkdir(parents=True,exist_ok=True)
            (directory/'falhas').mkdir(exist_ok=True)
            e=B.AvaliacaoGap(destination,respondentes=models,juiz=B.Q.JUIZ,grupos=[tuple(models)],workers=workers,
                judge_workers=judge_workers,lote_juiz=8,clientes=clients)
            e.run();B.exportar_gap(destination,models)
            faithful=B.faithfulness(e,original)
        import csv
        with (destination/'pares.csv').open(encoding='utf-8-sig',newline='') as f:pairs=list(csv.DictReader(f,escapechar='\\'))
        metadata={q['uid']:q for q in original}
        gaps=paired_summary(pairs,metadata,seed)
        from .metrics import matched
        bygroup={g:[q for q in original if q['grupo']==g] for g in sorted({q['grupo'] for q in original})}
        balanced=matched(bygroup,seed);balanced_ids={q['uid'] for qs in balanced.values() for q in qs}
        balanced_gaps=paired_summary([p for p in pairs if p['uid'] in balanced_ids],metadata,seed)
        audits=B.Q.linhas(destination/'faithfulness.jsonl');byuid={q['uid']:q for q in audits};support={}
        for group in sorted({q['grupo'] for q in original}):
            qs=[q for q in original if q['grupo']==group];cases=[byuid[q['uid']] for q in qs if q['uid'] in byuid]
            decided=[a for a in cases if a['status'] in ('totalmente_sustentado','suporte_insuficiente','contradicao')]
            support[group]=dict(total=len(qs),processadas=len(cases),com_decisao=len(decided),
                por_status=dict(Counter(a['status'] for a in cases)),
                taxa_sustentacao=100*sum(a['status']=='totalmente_sustentado' for a in decided)/len(decided) if decided else None)
        complete=faithful and all(len(e.vereditos[m])==len(paired) for m in models)
        supported_ids={u for u,a in byuid.items() if a['status']=='totalmente_sustentado'}
        result=dict(status='concluido' if complete else 'parcial',gap_por_grupo=gaps,
            gap_mesmo_n_item_classe=balanced_gaps,uids_amostra_comparavel=sorted(balanced_ids),
            gap_sensibilidade_sustentados=paired_summary([p for p in pairs if p['uid'] in supported_ids],metadata,seed),sustentacao_por_grupo=support,
            protocolo='Mesmo protocolo histórico de 100 palavras e juízes congelados; auditoria independente da admissão',
            ressalva='Auditoria automática, não humana. Comparações entre grupos têm perguntas diferentes; só open/closed por questão é pareado.')
        atomic_json(destination/'comparacao.json',result)
        md=['# Gap e sustentação no piloto','',
            '| Grupo | Modelo | Pares válidos | Sem contexto | Com contexto | Gap p p | IC 95 do gap |',
            '|---|---|---:|---:|---:|---:|---|']
        def fmt(v):return '—' if v is None else f'{v:.2f}'
        for r in gaps:
            ci='—' if r['ic95_gap'] is None else ' a '.join(fmt(x) for x in r['ic95_gap'])
            md.append('| '+' | '.join([r['grupo'],r['modelo'],str(r['pares_validos']),fmt(r['acuracia_sem_contexto']),
                fmt(r['acuracia_com_contexto']),fmt(r['gap_pp']),ci])+' |')
        md+=['','| Grupo | Auditorias com decisão | Total | Gabaritos sustentados em percentual |','|---|---:|---:|---:|']
        for group,s in support.items():md.append(f"| {group} | {s['com_decisao']} | {s['total']} | {fmt(s['taxa_sustentacao'])} |")
        md+=['',result['ressalva'],'A comparação por mesmo tamanho/documento/classe e a sensibilidade restrita a gabaritos sustentados estão em comparacao.json.',
             'Bloqueios e falhas não recebem zero artificial. O conjunto final permanece sujeito à revisão humana.']
        (destination/'RESULTADOS.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
        return result
