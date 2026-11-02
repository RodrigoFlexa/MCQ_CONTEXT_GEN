"""Pacotes de texto original: capítulos e interfaces do mesmo grupo editorial."""
from collections import defaultdict
from .contracts import require
from .documents import flatten


def packages(document, max_chars=24000):
    flat=iter(flatten(document));chapters=[];groups=defaultdict(list)
    for i,c in enumerate(document['capitulos'],1):
        blocks=[next(flat) for _ in c['blocos']]
        chapters.append((i,c,blocks));groups[c.get('grupo',c['titulo'])].append((i,c,blocks))
    result=[]
    def add(name,kind,blocks):
        current=[];size=0
        for b in blocks:
            n=len(b['texto'])+len(b['capitulo'])+len(b['subtitulo'])+100
            require(n<=max_chars,'Bloco maior que context_chars: '+b['id'])
            if current and size+n>max_chars:
                result.append(dict(nome=name,tipo=kind,blocos=current));current=[];size=0
            current.append(b);size+=n
        if current:result.append(dict(nome=name,tipo=kind,blocos=current))
    for i,c,bs in chapters:add(c['titulo'],'capitulo',bs)
    for name,cs in groups.items():
        if len(cs)<2:continue
        bs=[b for _,_,blocks in cs for b in blocks]
        # Interfaces só são emitidas completas. Se grandes, usar pares adjacentes.
        if sum(len(b['texto'])+len(b['capitulo'])+len(b['subtitulo'])+100 for b in bs)<=max_chars:
            add(name,'interface',bs)
        else:
            for a,b in zip(cs,cs[1:]):
                joined=a[2]+b[2]
                if sum(len(x['texto'])+len(x['capitulo'])+len(x['subtitulo'])+100 for x in joined)<=max_chars:
                    add(a[1]['titulo']+' + '+b[1]['titulo'],'interface',joined)
    unique=[];seen=set()
    for p in result:
        signature=tuple(b['id'] for b in p['blocos'])
        if signature not in seen:
            seen.add(signature);unique.append(dict(p,id=f'C{len(unique)+1:03}'))
    require(unique,'Documento sem contextos')
    return unique
