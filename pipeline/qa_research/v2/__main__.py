"""CLI portátil: python -m pipeline.qa_research.v2 --plan."""
import argparse
import json
import shlex
import shutil
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.domain_corpora.manifest import load_manifest
from pipeline.domain_corpora.io_utils import file_hash
from . import VERSION
from .common import ROOT, Calls, digest, require, topic, load_examples
from . import context, questions

DEFAULT_CONFIG=ROOT/'pipeline/qa_research/v2/piloto_02_02.json'


def load_config(path):
    config=json.loads(Path(path).read_text(encoding='utf-8-sig'))
    for k in ('max_calls','workers','max_facets','document_rounds','document_patience','queries_per_facet',
              'retrieval_candidates','max_per_document','sources_per_facet','unit_batch_blocks',
              'max_units_per_batch','qa_rounds','max_targets','targets_per_round','min_new_questions',
              'qa_patience','min_questions','dedup_batch'):
        require(type(config.get(k)) is int and config[k]>0,'Parâmetro inteiro positivo esperado: '+k)
    for k in ('refine_attempts','examples_per_call'):
        require(type(config.get(k)) is int and config[k]>=0,'Parâmetro não negativo esperado: '+k)
    for k in ('unit_coverage','demand_coverage'):
        require(isinstance(config.get(k),(int,float)) and 0<config[k]<=1,'Cobertura inválida: '+k)
    roles=('plan','doc_research','doc_write','doc_audit','coverage','units','unit_audit',
           'qa_plan','qa_author','qa_solver','qa_audit','qa_refine','dedup')
    require(set(config['models'])==set(roles),'Configure todos os papéis explicitamente')
    for spec in config['models'].values():
        require(isinstance(spec,str) and ':' in spec and spec.rsplit(':',1)[1] in ('none','low','medium','high'),'Modelo: use deployment:effort')
    return config


def check_document(data,selected):
    require(isinstance(data,dict) and set(data)=={'titulo','capitulos'} and data['titulo']==selected['titulo'],
            'Documento limpo com título correspondente ao subtópico esperado')
    require(isinstance(data['capitulos'],list) and bool(data['capitulos']),'Documento sem capítulos')
    for c in data['capitulos']:
        require(set(c)=={'titulo','grupo','blocos'} and isinstance(c['blocos'],list) and bool(c['blocos']),'Capítulo inválido')
        for b in c['blocos']:
            require(set(b)=={'subtitulo','texto'} and all(isinstance(v,str) and v.strip() for v in b.values()),'Bloco inválido')


def summary_markdown(output,selected,summary):
    d=summary.get('contexto',{});q=summary.get('questoes',{})
    lines=['# Piloto do protocolo de cobertura', '', '**Subtópico:** '+selected['subtopico'],
        '', '**Frase do especialista:** '+selected['frase_especialista'], '', '**Estado:** '+summary['status'],
        '', 'Documento: '+d.get('motivo_parada','não executado'),
        '', 'QA: '+q.get('motivo_parada','não executada'),
        '', f"Questões aprovadas pelo modelo: {q.get('aprovadas',0)}.",
        '', f"Cobertura de unidades: {q.get('cobertura_unidades',0):.1%}; de demandas/classes: {q.get('cobertura_demandas',0):.1%}.",
        '', 'Aprovação automática não representa validação pelo especialista.',
        'As coberturas são relativas ao inventário admitido, sem garantia de exaustividade do domínio.',
        '', '| Classe | Aprovadas |','|---|---:|']
    lines += [f'| {t} | {n} |' for t,n in q.get('por_tipo',{}).items()]
    if summary.get('erro'): lines += ['', 'Erro/interrupção: '+summary['erro']]
    (Path(output)/'RELATORIO.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


def execute(selected,manifest,output,config,stage='all',document=None,example_paths=(),clients=None):
    output=Path(output).resolve()
    require(output!=ROOT and output not in ROOT.parents,'A saída não pode ser a raiz do projeto nem um diretório ancestral')
    examples=load_examples(example_paths,selected['id'])
    # Conteúdo dos arquivos referenciados (não só o JSON manifesto) é verificado antes de qualquer chamada.
    corpus_identity=None
    if stage!='qa' or manifest:
        require(manifest is not None,'Informe --manifest para gerar contexto')
        m,_=load_manifest(manifest)
        corpus_identity=digest(m)
    if manifest: require(Path(manifest).resolve().parent not in (output,*output.parents),'Saída não pode ficar dentro do corpus')
    if document: check_document(read_json(document),selected)
    implementation=digest({p.name:p.read_text(encoding='utf-8') for p in sorted(Path(__file__).parent.glob('*.py'))} | {
        'document_runner':file_hash(ROOT/'pipeline/qa_research/document/runner.py'),
        'document_prompts':file_hash(ROOT/'pipeline/qa_research/document/prompts.py'),
        'document_contracts':file_hash(ROOT/'pipeline/qa_research/document/contracts.py'),
        'document_export':file_hash(ROOT/'pipeline/qa_research/document/export.py'),
        'corpus_index':file_hash(ROOT/'pipeline/qa_research/corpus.py'),
        'manifest_loader':file_hash(ROOT/'pipeline/domain_corpora/manifest.py'),
        'tipos':file_hash(ROOT/'pipeline/qa_research/tipos.py'),
        'backend':file_hash(ROOT/'azure_openai_backend.py'),
        'client':file_hash(ROOT/'pipeline/inventario/llm.py')})
    identity=dict(version=VERSION,entrada=selected,config={k:v for k,v in config.items() if k!='max_calls'},
        corpus=corpus_identity,documento=file_hash(document) if document else None,
        exemplos=digest(examples),implementation=implementation)
    with output_lock(output):
        previous=read_json(output/'identidade.json')
        require(previous is None or previous==identity,'Entradas, modelos, exemplos ou código mudaram; use outra --output')
        atomic_json(output/'identidade.json',identity)
        calls=Calls(output,config,clients)
        summary=dict(status='em_andamento',entrada=selected)
        try:
            if stage in ('all','context') and not document:
                doc,doc_report=context.generate(selected,manifest,output/'contexto',config,calls)
                summary['contexto']=doc_report
            else:
                path=Path(document) if document else output/'contexto'/'documento.json'
                doc=read_json(path);check_document(doc,selected)
                doc_report=read_json(path.parent/'cobertura.json') or {}
                summary['contexto']=doc_report
            if stage in ('all','qa'):
                require(doc_report.get('qa_elegivel',True),'Revisão global ainda tem conflitos; QA bloqueada')
                check_document(doc,selected)
                summary['questoes']=questions.generate(doc,output/'questoes',config,calls,examples)
            reports=[summary[k] for k in ('contexto','questoes') if k in summary and summary[k]]
            summary['status']='concluido' if reports and all(r['status']=='concluido' for r in reports) else 'parcial'
        except KeyboardInterrupt:
            summary.update(status='interrompido',erro='Interrompido pelo operador; checkpoints preservados')
        except Exception as exc:
            summary.update(status='interrompido',erro=f'{type(exc).__name__}: {str(exc)[:1000]}')
        finally:
            summary['tentativas_reservadas']=calls.budget.used
            atomic_json(output/'resumo.json',summary);summary_markdown(output,selected,summary);calls.close()
        return summary


def collect(source,destination):
    source,destination=Path(source).resolve(),Path(destination).resolve()
    require(source!=destination and source not in destination.parents and destination not in source.parents,
            'Origem e destino devem ser separados')
    require(not destination.exists(),'Coleta é imutável: escolha destino novo')
    with output_lock(source):
        require((source/'resumo.json').is_file(),'Saída sem resumo')
        destination.mkdir(parents=True)
        # Só artefatos de auditoria/resultados. Pacotes de fontes e caches não voltam ao Git.
        for path in source.rglob('*'):
            rel=path.relative_to(source)
            if any(p in ('.local','pacote') for p in rel.parts) or path.name=='.run.lock': continue
            if 'chamadas' in rel.parts or 'documental' in rel.parts: continue
            if path.is_file() and not path.is_symlink() and path.suffix in ('.json','.jsonl','.md','.csv'):
                target=destination/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
        atomic_json(destination/'manifest_resultados.json',{'schema':'coverage-results-v2',
            'files':{p.relative_to(destination).as_posix():file_hash(p) for p in destination.rglob('*') if p.is_file()}})


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config',type=Path,default=DEFAULT_CONFIG)
    p.add_argument('--item',default='02_02')
    p.add_argument('--manifest',type=Path)
    p.add_argument('--output',type=Path,default=Path('pipeline/qa_research/saida_cobertura_v2/02_02'))
    p.add_argument('--stage',choices=('all','context','qa'),default='all')
    p.add_argument('--document',type=Path)
    p.add_argument('--examples',type=Path,action='append',help='Leitura de arquivo existente; nunca baixa ou modifica datasets QA')
    p.add_argument('--max-calls',type=int)
    p.add_argument('--solver-model',help='deployment:effort explícito; sem fallback automático')
    p.add_argument('--plan',action='store_true')
    p.add_argument('--collect',type=Path,help='Coleta --output para destino novo, sem executar geração')
    a=p.parse_args(argv)
    if a.collect: collect(a.output,a.collect);print('Coleta:',a.collect);return 0
    config=load_config(a.config)
    if a.max_calls is not None: require(a.max_calls>0,'Orçamento deve ser positivo');config['max_calls']=a.max_calls
    if a.solver_model: config['models']['qa_solver']=a.solver_model
    require(':' in config['models']['qa_solver'],'Resolvedor deve declarar esforço')
    selected=topic(a.item)
    if a.output==Path('pipeline/qa_research/saida_cobertura_v2/02_02'):
        a.output=a.output.parent/a.item
    examples=a.examples if a.examples is not None else [ROOT/'pipeline/qa_research/geracao_tipos/exemplos.json']
    if a.plan:
        print(json.dumps(dict(entrada=selected,config=config,manifest=str(a.manifest),output=str(a.output),
            stage=a.stage,document=str(a.document),exemplos_somente_leitura=[str(x) for x in examples]),ensure_ascii=False,indent=2));return 0
    result=execute(selected,a.manifest,a.output,config,a.stage,a.document,examples)
    print('O código acabou de rodar no terminal 🙂')
    print('Estado real:',result['status'],'| consulte',a.output/'RELATORIO.md')
    destination=Path('pipeline/qa_research/relatorios')/('piloto_cobertura_v2_'+a.item)
    if destination.exists():
        from datetime import datetime,timezone
        destination=destination.with_name(destination.name+'_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    print('Coleta no servidor:')
    print('python -m pipeline.qa_research.v2 --output '+shlex.quote(str(a.output))+' --collect '+shlex.quote(str(destination)))
    print('git add -- '+shlex.quote(str(destination)))
    print('git commit -m '+shlex.quote('Resultados do piloto de cobertura v2 - '+a.item))
    print('git push origin codex/qa-evidencias-verificadas')
    print('Coleta local: git pull --ff-only origin codex/qa-evidencias-verificadas')
    return 0 if result['status']=='concluido' else 2


if __name__=='__main__': raise SystemExit(main())
