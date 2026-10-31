"""Inspeciona a busca no corpus instalado sem Azure nem credenciais."""
import argparse
import json
from pathlib import Path
from pipeline.qa_research.corpus import CorpusIndex


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--query',required=True)
    p.add_argument('--limit',type=int,default=5)
    p.add_argument('--index',type=Path,default=Path('pipeline/qa_research/.local/professional_index'))
    a=p.parse_args(argv)
    index=CorpusIndex(a.index,manifest=a.manifest);info=index.build()
    print(json.dumps({'indice':info,'resultados':index.search(a.query,limit=a.limit)},ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
