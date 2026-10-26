"""Congela apenas contagens e escopos do programa; não exporta nenhuma questão de referência."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from pipeline.fase_3.topicos import TOPICOS
from .core import METAS, ROOT


def preparar(origem,saida=METAS):
    source=Path(origem)/'aprovadas.jsonl'
    raw=source.read_bytes().replace(b'\r\n',b'\n')  # fingerprint portátil entre Git/Windows e Linux
    rows=[json.loads(x) for x in raw.decode('utf-8-sig').splitlines() if x.strip()]
    if not rows or len({r['uid'] for r in rows})!=len(rows) or any(r.get('aprovada') is not True for r in rows):
        raise ValueError('A origem deve conter aprovadas não vazias com IDs únicos')
    counts=Counter(r['item'] for r in rows)
    items=[]
    for ai,(area,subtopics) in enumerate(TOPICOS.items(),1):
        for si,(subtitle,phrase) in enumerate(subtopics.items(),1):
            key=f'{ai:02}_{si:02}'
            if key in counts:
                items.append({'id':key,'topico':area,'subtopico':subtitle,'frase_especialista':phrase,'meta':counts[key]})
    if {r['id'] for r in items}!=set(counts):
        raise ValueError('Há tópicos sem frase no programa')
    data={'schema':'metas-sem-conteudo-v1','run_referencia':Path(origem).name,
          'aprovadas_referencia_sha256':hashlib.sha256(raw).hexdigest(),
          'programa_sha256':hashlib.sha256((ROOT/'pipeline/fase_3/topicos.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
          'total':len(rows),'itens':items}
    Path(saida).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return data


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--origem',type=Path,default=ROOT/'pipeline/qa_research/relatorios/geracao_final_20261024T204734Z')
    p.add_argument('--saida',type=Path,default=METAS)
    a=p.parse_args()
    d=preparar(a.origem,a.saida)
    print(f'{d["total"]} questões em {len(d["itens"])} metas; nenhum enunciado de referência exportado.')
