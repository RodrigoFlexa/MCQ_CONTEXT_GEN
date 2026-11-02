"""CLI do fluxo contínuo por capítulos, sem teto de questões."""
import argparse
import asyncio
import json
from pathlib import Path
from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json,read_json
from pipeline.qa_research.v3.runtime import ROOT,digest,load_examples
from .__main__ import collect
from .documents import prepare,close_pilot,load,PENDING,LATEST,OLD
from .contextos import packages
from .evaluation import historical,rows,evaluate
from .generate import jsonl
from .adaptive import generate
from .similarity import Similarity
from . import contracts as C

HERE=Path(__file__).parent
DEFAULT=ROOT/'pipeline/qa_research/saida_piloto_qa/continuo_v2'


def config():
    c=load(HERE/'config.json')
    c.pop('questions_per_item');c.pop('max_batches')
    c.update(schema='qa-continuo-1',context_chars=24000,memory_limit=30,neighbors=5)
    return c


def base_bank():
    from pipeline.qa_research.benchmark_gap import SOURCE
    return [dict(q,id='H_'+digest(q['uid'])[:24]) for q in rows(SOURCE)]


def groups_at(output):
    protocol=load(output/'protocolo.json')
    groups={'historico':rows(output/'historico.jsonl')}
    for group in protocol['arms']:
        groups[group]=[q for item in protocol['items'] for path in [output/'geracao'/group/item/'aprovadas.jsonl'] if path.exists() for q in rows(path)]
    return protocol,groups


def tables(output,*,embeddings=False,assessment=False,mini=None):
    from .metrics import calculate
    from .report import write
    with output_lock(output):
        protocol,groups=groups_at(output);seed=protocol['config']['seed']
        if assessment:
            n=sum(len(qs) for qs in groups.values())
            print(f'[avaliação] {n} questões | {6*n} respostas com/sem contexto, além de julgamentos e auditorias',flush=True)
            result=evaluate([q for qs in groups.values() for q in qs],output/'avaliacao_comparavel',seed=seed,mini=mini)
            measured=read_json(output/'metricas/metricas.json') or {}
            if measured.get('protocolo',{}).get('dados_sha256')!=digest(groups):calculate(groups,output/'metricas',seed,embeddings)
        else:
            calculate(groups,output/'metricas',seed,embeddings);result=None
        path=write(output,groups)
        print(path.read_text(encoding='utf-8'),flush=True)
        print('Tabelas formatadas:',output/'TABELAS.html',flush=True)
        return result


async def run(output,c,arms,examples=(),transport=None,similarity=None):
    output=Path(output)
    with output_lock(output):
        prepared=prepare(output/'contextos',c['items']);baseline=base_bank()
        forms={}
        for item in c['items']:
            if examples:forms[item]=load_examples(examples,item)[:6]
            else:
                eligible=sorted((q for q in baseline if q['item'] not in c['items']),key=lambda q:digest([c['seed'],q['uid']]))
                forms[item]=[dict(tipo=q['tipo'],pergunta=q['pergunta'],resposta=q['resposta'],origem='banco_proprio',id=q['uid'])
                    for kind in C.TYPES for q in [next(q for q in eligible if q['tipo']==kind)]]
        protocol=dict(schema='qa-continuo-1',items=c['items'],arms=arms,
            config={k:v for k,v in c.items() if k not in ('max_calls','heartbeat','workers')},
            documentos=digest(prepared),banco=digest(baseline),exemplos=digest(forms))
        previous=read_json(output/'protocolo.json')
        C.require(previous is None or previous==protocol,'Protocolo mudou; use outra saída')
        atomic_json(output/'protocolo.json',protocol)
        jsonl(output/'historico.jsonl',historical(c['items'],20,c['seed']))
        own=similarity is None;similarity=similarity or Similarity(output)
        reports=read_json(output/'resumo_geracao.json') or {}
        try:
            # Validação semântica antes de qualquer API paga; não baixa pesos.
            similarity.vectors([q['pergunta'] for q in baseline])
            for group,folder in [('novo_antigo','antigo'),('novo_refinado','refinado')]:
                if group not in arms:continue
                bank=list(baseline);reports.setdefault(group,{})
                for item in c['items']:
                    destination=output/'geracao'/group/item
                    report=await generate(load(output/'contextos'/folder/item/'documento.json'),item,group,c,destination,
                        bank,similarity,forms[item],PENDING[item],transport=transport)
                    reports[group][item]=report;atomic_json(output/'resumo_geracao.json',reports)
                    # A suspensão bloqueia os próximos documentos: retomada mantém o banco inicial.
                    if report['status']!='concluido':return reports
                    bank+=rows(destination/'aprovadas.jsonl')
        finally:
            if own:similarity.close()
        return reports


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage',choices=['prepare','generate','metrics','evaluate','all'],default='generate')
    p.add_argument('--output',type=Path,default=DEFAULT)
    p.add_argument('--items',nargs='+');p.add_argument('--arms',choices=['both','refinado','antigo'],default='both')
    p.add_argument('--max-calls',type=int,default=150);p.add_argument('--memory-limit',type=int,default=30)
    p.add_argument('--patience',type=int,default=3);p.add_argument('--plan',action='store_true')
    p.add_argument('--examples',type=Path,action='append',default=[])
    p.add_argument('--collect',type=Path);p.add_argument('--embeddings',action='store_true');p.add_argument('--mini-deployment')
    args=p.parse_args(argv);c=config();c.update(max_calls=args.max_calls,memory_limit=args.memory_limit,patience=args.patience)
    if args.items:c['items']=args.items
    C.require(len(c['items'])==len(set(c['items'])) and c['items'],'IDs válidos e únicos')
    C.require(all(type(c[k]) is int and c[k]>0 for k in ('max_calls','memory_limit','patience')),'Limites positivos obrigatórios')
    arms=['novo_antigo','novo_refinado'] if args.arms=='both' else ['novo_'+args.arms]
    output=args.output.resolve()
    for protected in (ROOT,HERE,LATEST,OLD):
        C.require(output!=protected and output not in protected.parents and (protected==ROOT or protected not in output.parents),'Saída deve ser separada de código/fontes')
    if args.collect:collect(output,args.collect);return 0
    if args.plan:
        details={}
        for item in c['items']:
            refined,_=close_pilot(item);details[item]={}
            for group,doc in [('novo_antigo',load(OLD/item/'documento.json')),('novo_refinado',refined)]:
                if group in arms:details[item][group]=[{k:v for k,v in pack.items() if k!='blocos'} for pack in packages(doc,c['context_chars'])]
        print(json.dumps(dict(config=c,arms=arms,contextos=details,teto_questoes=None,
            chamadas_max_por_documento_grupo=c['max_calls'],api=False),ensure_ascii=False,indent=2));return 0
    if args.stage=='prepare':prepare(output/'contextos',c['items']);return 0
    if args.stage in ('generate','all'):
        reports=asyncio.run(run(output,c,arms,args.examples))
        complete=all(reports.get(g,{}).get(i,{}).get('status')=='concluido' for g in arms for i in c['items'])
        tables(output,embeddings=True)
        assessed=None
        if complete and args.stage=='all':assessed=tables(output,assessment=True,mini=args.mini_deployment)
        print('O código acabou de rodar no terminal 🙂')
        print('Estado:', 'contextos sem ganho' if complete else 'parcial; consultar resumo e retomar', '|',output)
        if assessed is not None:print('Avaliação:',assessed['status'])
        target='pipeline/qa_research/relatorios/qa_continuo_v2'
        print(f'"${{DOCUMENT_PYTHON:-python3}}" -m pipeline.qa_research.piloto_qa.fluxo --output "{output}" --collect {target}')
        print('git add -- '+target);print('git commit -m "Resultados QA continuo v2"');print('git push origin codex/qa-evidencias-verificadas')
        return 0 if complete and (assessed is None or assessed['status']=='concluido') else 2
    if args.stage=='metrics':
        tables(output,embeddings=args.embeddings)
        return 0
    # Avaliação com N variável exige saída nova; não mistura uma avaliação anterior.
    result=tables(output,assessment=True,mini=args.mini_deployment)
    print('O código acabou de rodar no terminal 🙂');print('Avaliação:',result['status'])
    return 0 if result['status']=='concluido' else 2


if __name__=='__main__':raise SystemExit(main())
