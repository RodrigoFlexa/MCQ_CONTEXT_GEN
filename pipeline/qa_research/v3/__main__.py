"""CLI do fluxo por seções e lotes: python -m pipeline.qa_research.v3."""
import argparse
import asyncio
import json
import shlex
import shutil
from pathlib import Path

from pipeline.domain_corpora.io_utils import file_hash
from pipeline.domain_corpora.manifest import load_manifest
from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from . import VERSION, contracts as C, context, questions, prompts as P
from .runtime import ROOT, Calls, digest, topic, load_examples, stamp

DEFAULT=Path(__file__).with_name('piloto.json')


def configuration(path=DEFAULT, overrides=None):
    config=json.loads(Path(path).read_text(encoding='utf-8-sig'));config.update(overrides or {})
    for k in ('workers','max_calls','request_timeout','heartbeat','output_tokens','retry_tokens','max_input_chars',
              'sections','sources_per_section','max_per_document','retrieval_candidates','section_words',
              'batch_size','max_batches','min_questions','patience'):
        C.require(type(config.get(k)) is int and config[k]>0,'Configuração inteira positiva esperada: '+k)
    C.require(config['batch_size']<=8,'batch_size deve ser no máximo 8')
    C.require(config['retry_tokens']>=config['output_tokens'],'retry_tokens deve ser >= output_tokens')
    C.require(set(config.get('models',{}))==set(P.PROMPTS),'Configure os sete papéis de modelos')
    for value in config['models'].values():
        C.require(isinstance(value,str) and ':' in value and value.rsplit(':',1)[1] in ('low','medium','high'),'Modelo deve ser deployment:low|medium|high')
    return config


def markdown(output, summary):
    d=summary.get('contexto',{});q=summary.get('questoes',{})
    lines=['# Piloto de contexto e questões — fluxo v3','',
        '**Subtópico:** '+summary['entrada']['subtopico'],'',
        '**Estado:** '+summary['status'],'',
        '**Frase do especialista:** '+summary['entrada']['frase_especialista'],'',
        f"Seções liberadas: {d.get('secoes_liberadas',0)} de {d.get('secoes_planejadas',0)}.",
        f"Questões admitidas pelo modelo: {q.get('admitidas',0)}.",
        f"Tentativas externas cumulativas: {summary.get('tentativas',0)}.",
        '', 'Motivo de parada das questões: '+q.get('motivo_parada','não concluídas nesta execução')+'.',
        '', 'Aprovação automática; validação pelo especialista pendente.',
        'Pontos ausentes do documento e perguntas não cobertas permanecem nos relatórios auxiliares.']
    if summary.get('erro'):lines+=['','Interrupção: '+summary['erro']]
    lines+=['','| Classe | Admitidas |','|---|---:|']
    lines += [f'| {k} | {v} |' for k,v in q.get('por_classe',{}).items()]
    (Path(output)/'RELATORIO.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


async def execute(entrada, manifest, output, config, stage='all', example_paths=(), transport=None, check=False):
    output=Path(output).resolve()
    C.require(output!=ROOT and output not in ROOT.parents,'A saída não pode ser raiz ou ancestral do projeto')
    manifest=Path(manifest).resolve()
    C.require(manifest.parent not in (output,*output.parents),'Saída não pode ficar dentro do corpus')
    examples=load_examples(example_paths,entrada['id'])
    print('[preparação] verificando manifesto e arquivos do corpus',flush=True)
    m,_=await asyncio.to_thread(load_manifest,manifest);corpus_identity=digest(m)
    with output_lock(output):
        identity=dict(schema=VERSION,entrada=entrada)
        previous=read_json(output/'identidade.json')
        C.require(previous is None or previous==identity,'Subtópico/versão mudou; use uma saída nova')
        atomic_json(output/'identidade.json',identity)
        summary=dict(status='em_andamento',entrada=entrada,inicio=stamp(),config=config,corpus=corpus_identity)
        calls=None
        try:
            calls=Calls(output,config,transport=transport)
            if check:
                for role in ('write','review','solve'):
                    await calls.call(role,'disponibilidade',{'tarefa':'Responda ok=true'},
                        lambda d:C.require(d.get('ok') is True,'Esperado ok=true'),system=P.CHECK,tokens=8000)
                return dict(status='verificado',tentativas=calls.budget.used)
            if stage in ('all','context'):
                sections,report=await context.generate(entrada,manifest,config,calls,output/'contexto',corpus_identity)
            else:
                report=read_json(output/'contexto'/'cobertura.json')
                C.require(report and report.get('entrada')==digest(entrada) and report.get('corpus_manifest')==corpus_identity,'Contexto ausente ou incompatível com entrada/corpus; execute --stage context')
                doc=read_json(output/'contexto'/'documento.json')
                trace=read_json(output/'contexto'/'versoes'/report['versao']/'rastreabilidade.json')
                C.require(doc and trace,'Documento/rastreabilidade ausente')
                sections=trace['secoes']
                clean=dict(titulo=entrada['titulo'],secoes=[dict(titulo=s['titulo'],texto=s['texto']) for s in sections])
                C.require(digest(doc)==report['documento_sha256']==digest(clean),'Contexto alterado após revisão; gere uma nova versão')
            summary['contexto']=report
            if stage in ('all','qa'):
                C.require(report['qa_elegivel'],'Nenhuma seção foi liberada para gerar questões')
                summary['questoes']=await questions.generate(entrada,sections,report,examples,config,calls,output/'questoes')
            reports=[summary[k] for k in ('contexto','questoes') if k in summary]
            summary['status']='concluido' if all(r['status']=='concluido' for r in reports) else 'parcial'
        except (asyncio.CancelledError,KeyboardInterrupt):
            summary.update(status='interrompido',erro='Interrompido pelo operador; resultados concluídos preservados')
        except Exception as exc:
            summary.update(status='interrompido',erro=f'{type(exc).__name__}: {str(exc)[:900]}')
        finally:
            if not check:
                checkpoint=read_json(output/'questoes'/'cobertura.json')
                if ('questoes' not in summary and 'contexto' in summary and stage in ('all','qa') and checkpoint
                        and checkpoint.get('documento_sha256')==summary['contexto']['documento_sha256']):
                    summary['questoes']=dict(checkpoint,status='interrompido',motivo_parada='pendencia_execucao')
                summary.update(fim=stamp(),tentativas=calls.budget.used if calls else 0)
                atomic_json(output/'resumo.json',summary);markdown(output,summary)
            if calls:await calls.close()
        return summary


def collect(output, destination):
    output,destination=Path(output).resolve(),Path(destination).resolve()
    C.require(output!=destination and output not in destination.parents and destination not in output.parents,'Coleta precisa de origem e destino separados')
    C.require(not destination.exists(),'Coleta imutável: escolha destino novo')
    with output_lock(output):
        C.require((output/'resumo.json').is_file(),'Saída sem resumo; aguarde a execução terminar')
        candidates=[output/n for n in ('identidade.json','resumo.json','RELATORIO.md','orcamento.json','chamadas_llm.jsonl')]
        for part in ('contexto','questoes'):
            candidates.extend(p for p in (output/part).glob('*') if p.is_file())
            report=read_json(output/part/'cobertura.json') or {}
            if report.get('versao'):
                version=output/part/'versoes'/report['versao']
                candidates.extend(p for p in version.glob('*.json') if p.is_file())
        destination.mkdir(parents=True)
        for path in candidates:
            if path.is_symlink() or path.suffix not in ('.json','.jsonl','.md','.csv'):continue
            target=destination/path.relative_to(output);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
        atomic_json(destination/'manifest_resultados.json',dict(schema='sections-batches-results-v3',
            files={p.relative_to(destination).as_posix():file_hash(p) for p in destination.rglob('*') if p.is_file()}))


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,default=DEFAULT)
    parser.add_argument('--item',default='02_02')
    parser.add_argument('--manifest',type=Path)
    parser.add_argument('--output',type=Path,default=Path('pipeline/qa_research/saida_fluxo_v3/02_02_piloto_01'))
    parser.add_argument('--stage',choices=('all','context','qa'),default='all')
    parser.add_argument('--examples',type=Path,action='append',help='Leitura explícita de exemplos existentes')
    parser.add_argument('--plan',action='store_true',help='Mostra configuração, sem chamadas nem escrita')
    parser.add_argument('--check',action='store_true',help='Verifica corpus/credenciais e os modelos com três chamadas curtas')
    parser.add_argument('--collect',type=Path)
    parser.add_argument('--solver-model',help='deployment:effort explícito')
    for name in ('max-calls','workers','request-timeout','min-questions','max-batches','batch-size'):
        parser.add_argument('--'+name,type=int)
    args=parser.parse_args(argv)
    if args.collect:
        collect(args.output,args.collect);print('Coleta:',args.collect);return 0
    config=configuration(args.config,{k:getattr(args,k) for k in ('max_calls','workers','request_timeout','min_questions','max_batches','batch_size') if getattr(args,k) is not None})
    if args.solver_model:
        config['models']['solve']=args.solver_model
        C.require(':' in args.solver_model and args.solver_model.rsplit(':',1)[1] in ('low','medium','high'),'Resolvedor: deployment:effort')
    entrada=topic(args.item)
    if args.output==Path('pipeline/qa_research/saida_fluxo_v3/02_02_piloto_01'):
        args.output=args.output.parent/(args.item+'_piloto_01')
    examples=args.examples if args.examples is not None else [ROOT/'pipeline/qa_research/geracao_tipos/exemplos.json']
    if args.plan:
        print(json.dumps(dict(entrada=entrada,config=config,manifest=str(args.manifest),output=str(args.output),
            exemplos_somente_leitura=[str(p) for p in examples]),ensure_ascii=False,indent=2));return 0
    C.require(args.manifest is not None,'Informe --manifest do corpus já instalado')
    result=asyncio.run(execute(entrada,args.manifest,args.output,config,args.stage,examples,check=args.check))
    if args.check:
        print('Verificação:',result['status'])
        if result.get('erro'):print(result['erro'])
        return 0 if result['status']=='verificado' else 2
    print('O código acabou de rodar no terminal 🙂')
    print('Estado real:',result['status'],'|',args.output/'RELATORIO.md')
    if result.get('erro'):print(result['erro'])
    destination=Path('pipeline/qa_research/relatorios')/('piloto_fluxo_v3_'+args.item+'_'+stamp().replace(':','').replace('-','').split('.')[0].replace('+0000','Z'))
    print('Comandos de coleta e envio:')
    print('"${DOCUMENT_PYTHON:-python3}" -m pipeline.qa_research.v3 --output '+shlex.quote(str(args.output))+' --collect '+shlex.quote(str(destination)))
    print('git add -- '+shlex.quote(str(destination)))
    print('git commit -m '+shlex.quote('Resultados do piloto fluxo v3 - '+args.item))
    print('git push origin codex/qa-evidencias-verificadas')
    return 0 if result['status']=='concluido' else 2


if __name__=='__main__':raise SystemExit(main())
