"""Contrato portátil e verificação dos arquivos antes de gastar chamadas Azure."""
import json
from pathlib import Path

from .io_utils import file_hash

REQUIRED={'petroles','anp','hse','bsee','regis'}


def load_manifest(path,allow_sample=False,verify=True):
    path=Path(path).resolve();manifest=json.loads(path.read_text(encoding='utf-8'))
    if manifest.get('schema')!='petroquest-domain-corpora-v1':raise ValueError('Versão do manifesto de corpora desconhecida')
    if manifest.get('ready') is not True:raise ValueError('Instalação incompleta. Consulte install_report.json e repita o instalador')
    if manifest.get('sample') and not allow_sample:raise ValueError('Corpus de teste/amostra. Instale sem limite para produção ou explicite --allow-sample-corpus')
    collections=manifest.get('collections',[])
    ids=[c['id'] for c in collections]
    if len(ids)!=len(set(ids)) or set(ids)!=REQUIRED:raise ValueError('São necessárias Petrolês + ANP + HSE + BSEE + REGIS, sem duplicatas')
    result=[]
    for collection in collections:
        item=dict(collection)
        if not isinstance(item.get('documents'),int) or item['documents']<1:raise ValueError('Coleção vazia: '+item['id'])
        if item['format']=='petroles_txt':
            item['files']=[{**f,'resolved_path':(path.parent/f['path']).resolve()} for f in item['files']]
            files=[(f['resolved_path'],f['sha256']) for f in item['files']]
        elif item['format']=='pages_jsonl':
            item['resolved_path']=(path.parent/item['path']).resolve();files=[(item['resolved_path'],item['sha256'])]
        else:raise ValueError('Formato desconhecido: '+item['format'])
        for filename,digest in files:
            if not filename.is_file():raise FileNotFoundError(str(filename))
            if verify and file_hash(filename)!=digest:raise ValueError('Corpus modificado ou corrompido: '+str(filename))
        result.append(item)
    return manifest,result


def iter_units(collections):
    """JSONL preserva fronteiras de documento e página; TXT mantém linhas reais."""
    for collection in collections:
        if collection['format']=='pages_jsonl':
            with collection['resolved_path'].open(encoding='utf-8') as stream:
                for line in stream:
                    row=json.loads(line)
                    if row.get('collection')!=collection['id']:raise ValueError('Proveniência não confere com o manifesto')
                    yield row
        else:
            # Petrolês original não tem fronteiras confiáveis de documento/página.
            # Não inventa essas fronteiras; sinaliza o limite ao auditor.
            for file in collection['files']:
                path=file['resolved_path'];docid='petroles-'+file['sha256'][:24]
                with path.open(encoding='utf-8',errors='replace') as stream:
                    for index,line in enumerate(stream):
                        yield {'collection':'petroles','document_id':docid,'title':path.name,
                            'arquivo':path.name,'language':'pt','jurisdiction':'not_specified','page':None,
                            'source_boundary':'original_concatenated_txt; document boundaries unknown',
                            'source_sha256':file['sha256'],'line':index,'text':line.strip()}
