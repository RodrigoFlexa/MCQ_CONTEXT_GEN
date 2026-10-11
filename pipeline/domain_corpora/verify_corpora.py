"""Confere integridade e proveniência sem carregar embeddings ou usar Azure."""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from pipeline.domain_corpora.manifest import load_manifest
from pipeline.domain_corpora.io_utils import atomic_json


def verify(path,allow_sample=False):
    manifest,collections=load_manifest(path,allow_sample)
    result={}
    for collection in collections:
        name=collection['id']
        if collection['format']=='petroles_txt':
            result[name]={'files':len(collection['files']),'bytes':sum(f['bytes'] for f in collection['files']),
                          'document_boundary':'unknown','page_boundary':'unknown','integrity':'verified'}
            continue
        documents=set();pages=0;words=0;languages=Counter();jurisdictions=Counter()
        with collection['resolved_path'].open(encoding='utf-8') as stream:
            for line in stream:
                row=json.loads(line)
                required=('collection','document_id','title','url','language','jurisdiction','page','text','raw_sha256')
                if any(k not in row for k in required):raise ValueError('Metadados incompletos em '+name)
                if row['collection']!=name or not isinstance(row['text'],str) or not row['text'].strip():
                    raise ValueError('Conteúdo/proveniência inválidos em '+name)
                if row['page'] is not None and (type(row['page']) is not int or row['page']<1):
                    raise ValueError('Página inválida em '+name)
                documents.add(row['document_id']);pages+=1;words+=len(row['text'].split())
                languages[row['language']]+=1;jurisdictions[row['jurisdiction']]+=1
        if len(documents)!=collection['documents']:raise ValueError('Contagem de documentos não confere em '+name)
        result[name]={'documents':len(documents),'text_units':pages,'words':words,'languages':dict(languages),
                      'jurisdictions':dict(jurisdictions),'integrity':'verified'}
    return {'sample':manifest['sample'],'partial':manifest.get('partial',False),
            'download_errors':manifest.get('download_errors',0),'collections':result,'verified':True,'azure_calls':0}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=ROOT/'dataset/domain_corpora/manifest.json')
    parser.add_argument('--allow-sample',action='store_true')
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    try:result=verify(args.manifest,args.allow_sample)
    except (ValueError,FileNotFoundError) as error:parser.exit(1,str(error)+'\n')
    if args.report:atomic_json(args.report,result)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
