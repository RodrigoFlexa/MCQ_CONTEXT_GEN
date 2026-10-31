"""Inspeciona a busca no corpus instalado sem Azure nem credenciais."""
import argparse
import json
from pathlib import Path
from pipeline.qa_research.corpus import CorpusIndex
from .language import bilingual_search, validate_pairs


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--query',required=True)
    p.add_argument('--query-en',help='Consulta inglesa equivalente a --query em PT; executa e combina ambas, sem Azure')
    p.add_argument('--limit',type=int,default=5)
    p.add_argument('--index',type=Path,default=Path('pipeline/qa_research/.local/professional_index'))
    a=p.parse_args(argv)
    index=CorpusIndex(a.index,manifest=a.manifest);info=index.build()
    if a.query_en:
        pairs=[{'pt':a.query,'en':a.query_en}];validate_pairs({'pares':pairs},1)
        rows,traces=bilingual_search(index,pairs,a.limit)
        print(json.dumps({'indice':info,'consultas':traces,'resultados':rows[:a.limit]},ensure_ascii=False,indent=2))
    else:
        print(json.dumps({'indice':info,'resultados':index.search(a.query,limit=a.limit),
            'nota':'Consulta literal de um idioma; informe --query-en para testar recuperação PT/EN.'},ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
