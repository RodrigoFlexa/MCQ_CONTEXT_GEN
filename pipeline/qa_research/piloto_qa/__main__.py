"""Preparar, gerar e comparar três grupos sem alterar os bancos existentes."""
import argparse
import asyncio
import json
import shutil
from pathlib import Path
from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.v3.runtime import ROOT, load_examples, digest
from . import VERSION
from . import contracts as C
from .documents import prepare, load, PENDING, LATEST
from .generate import generate, jsonl
from .evaluation import historical, rows, evaluate

HERE=Path(__file__).parent
GROUPS=('historico','novo_antigo','novo_refinado')


def config(path=HERE/'config.json'):
    c=load(path)
    for k in ('questions_per_item','batch_size','max_batches','patience','workers','max_calls','request_timeout','heartbeat','max_input_chars','output_tokens','retry_tokens'):
        C.require(type(c.get(k)) is int and c[k]>0,'Inteiro positivo obrigatório: '+k)
    C.require(c['batch_size']<=4,'Lotes de até quatro questões')
    C.require(c['retry_tokens']>=c['output_tokens'],'retry_tokens insuficiente')
    C.require(set(c['models'])=={'plan','author','solve','judge','refine'},'Cinco papéis obrigatórios')
    return c


def samples(output):
    output=Path(output);groups={'historico':rows(output/'historico.jsonl')}
    identity=load(output/'protocolo.json')
    for group in GROUPS[1:]:
        groups[group]=[q for item in identity['items'] for q in rows(output/'geracao'/group/item/'aprovadas.jsonl')]
    return groups


async def run(output, c, example_paths=(), transport=None):
    output=Path(output)
    with output_lock(output):
        prepared=prepare(output/'contextos',c['items'])
        history=historical(c['items'],c['questions_per_item'],c['seed'])
        form={item:load_examples(example_paths,item) for item in c['items']}
        # Exemplos próprios de outros subtópicos, nunca as perguntas da amostra de comparação.
        if not example_paths:
            from pipeline.qa_research.benchmark_gap import SOURCE
            allq=rows(SOURCE)
            for item in form:
                eligible=sorted((q for q in allq if q['item'] not in c['items']),key=lambda q:digest([c['seed'],q['uid']]))
                form[item]=[dict(tipo=q['tipo'],pergunta=q['pergunta'],resposta=q['resposta'],origem=str(SOURCE),id=q['uid'])
                    for kind in C.TYPES for q in [next(q for q in eligible if q['tipo']==kind)]]
        protocol=dict(schema=VERSION,items=c['items'],config={k:v for k,v in c.items() if k not in ('workers','max_calls','heartbeat')},
            documentos=digest(prepared),historico=digest(history),exemplos=digest(form))
        saved=read_json(output/'protocolo.json')
        C.require(saved is None or saved==protocol,'Protocolo/entradas mudaram; use nova saída')
        atomic_json(output/'protocolo.json',protocol);jsonl(output/'historico.jsonl',history)
        reports={}
        for group,folder in [('novo_antigo','antigo'),('novo_refinado','refinado')]:
            reports[group]={}
            for item in c['items']:
                report=await generate(load(output/'contextos'/folder/item/'documento.json'),item,group,c,
                    output/'geracao'/group/item,examples=form[item],pending=PENDING[item],transport=transport)
                reports[group][item]=report
                atomic_json(output/'resumo_geracao.json',reports)
        return reports


def collect(source,destination):
    source,destination=Path(source).resolve(),Path(destination).resolve()
    C.require(not destination.exists() and source!=destination and source not in destination.parents and destination not in source.parents,'Coleta exige destino novo e separado')
    with output_lock(source):
        for path in source.rglob('*'):
            relative=path.relative_to(source)
            if not path.is_file() or path.is_symlink() or any(p.startswith('.') for p in relative.parts):continue
            if path.suffix not in ('.json','.jsonl','.md','.csv','.npz','.html'):continue
            target=destination/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
        from pipeline.domain_corpora.io_utils import file_hash
        atomic_json(destination/'manifest_resultados.json',dict(schema=VERSION,files={p.relative_to(destination).as_posix():file_hash(p) for p in destination.rglob('*') if p.is_file()}))


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage',choices=['prepare','generate','metrics','evaluate'],default='generate')
    p.add_argument('--config',type=Path,default=HERE/'config.json')
    p.add_argument('--output',type=Path,default=ROOT/'pipeline/qa_research/saida_piloto_qa/piloto_60_v1')
    p.add_argument('--items',nargs='+');p.add_argument('--per-item',type=int);p.add_argument('--examples',type=Path,action='append',default=[])
    p.add_argument('--plan',action='store_true');p.add_argument('--embeddings',action='store_true')
    p.add_argument('--collect',type=Path);p.add_argument('--mini-deployment')
    args=p.parse_args(argv);c=config(args.config)
    if args.items:c['items']=args.items
    if args.per_item is not None:
        C.require(args.per_item>0,'Quantidade positiva');c['questions_per_item']=args.per_item
    output=args.output.resolve()
    C.require(output!=ROOT and output not in ROOT.parents,'Saída não pode ser a raiz/ancestral')
    for source in (LATEST,HERE,ROOT/'pipeline/qa_research/relatorios/dez_areas_final_v2'):
        C.require(source!=output and source not in output.parents and output not in source.parents,'Saída deve ser separada das fontes/código')
    if args.collect:collect(output,args.collect);return 0
    if args.plan:
        C.require(len(c['items'])==len(set(c['items'])),'IDs duplicados')
        for item in c['items']:
            from .documents import close_pilot
            close_pilot(item)
        n=len(c['items'])*c['questions_per_item']
        print(json.dumps(dict(config=c,grupos={g:n for g in GROUPS},casos_resposta_max=3*n*2*3,
            auditorias_sustentacao_max=3*n,api=False,nota='Meta, não garantia de admissão. Avaliação é comando separado.'),ensure_ascii=False,indent=2));return 0
    if args.stage=='prepare':
        prepare(output/'contextos',c['items']);print('Contextos ajustados:',output/'contextos');return 0
    if args.stage=='generate':
        reports=asyncio.run(run(output,c,args.examples));complete=all(r['status']=='concluido' for g in reports.values() for r in g.values())
        print('O código acabou de rodar no terminal 🙂');print('Geração:', 'concluída' if complete else 'parcial', '|', output)
        print('Coletar os resultados:')
        target='pipeline/qa_research/relatorios/piloto_qa_60_v1'
        print(f'"${{DOCUMENT_PYTHON:-python3}}" -m pipeline.qa_research.piloto_qa --output "{output}" --collect {target}')
        print('git add -- '+target);print('git commit -m "Resultados do piloto de QA comparavel"');print('git push origin codex/qa-evidencias-verificadas')
        return 0 if complete else 2
    groups=samples(output)
    seed=load(output/'protocolo.json')['config']['seed']
    if args.stage=='metrics':
        from .metrics import calculate
        result=calculate(groups,output/'metricas',seed,args.embeddings)
        print('Métricas:',output/'metricas/metricas.json');return 0
    result=evaluate([q for qs in groups.values() for q in qs],output/'avaliacao_comparavel',seed=seed,mini=args.mini_deployment)
    print('O código acabou de rodar no terminal 🙂');print('Avaliação:',result['status'])
    return 0 if result['status']=='concluido' else 2


if __name__=='__main__':raise SystemExit(main())
