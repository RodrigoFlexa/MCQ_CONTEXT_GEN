"""Contratos e chamadas persistentes do protocolo; sem acesso implícito a credenciais."""
import hashlib
import json
import re
import threading
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.inventario.llm import LLMClient, load_dotenv
from pipeline.qa_research.runtime import PersistentBudget

ROOT=Path(__file__).resolve().parents[3]
TYPES=('conceito','mecanismo','consequencia','diagnostico','decisao','procedimento')


def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()


def require(ok, message):
    if not ok: raise ValueError(message)


def text(value):
    return isinstance(value,str) and bool(value.strip())


def unique(rows):
    require(isinstance(rows,list) and all(isinstance(r,dict) and text(r.get('id')) and
        re.fullmatch(r'[A-Za-z0-9_-]{1,64}',r['id']) for r in rows),'Lista com IDs seguros esperada')
    require(len({r['id'] for r in rows})==len(rows),'IDs duplicados')


def ids(values, allowed, nonempty=True):
    require(isinstance(values,list) and (bool(values) or not nonempty) and all(isinstance(v,str) for v in values)
            and len(values)==len(set(values)) and set(values)<=set(allowed),'Referências inexistentes, vazias ou duplicadas')


def exact_rows(rows, expected):
    unique(rows); require({r['id'] for r in rows}==set(expected),'O parecer deve cobrir exatamente os IDs enviados')


def approved(review, criteria):
    return review.get('aprovada') is True and all(review.get(c) is True for c in criteria)


def topic(item):
    from pipeline.fase_3.topicos import TOPICOS
    for a,(area,subjects) in enumerate(TOPICOS.items(),1):
        for s,(subject,phrase) in enumerate(subjects.items(),1):
            if item==f'{a:02}_{s:02}':
                return dict(id=item,topico=area,subtopico=subject,frase_especialista=phrase,
                            titulo=f'{a}.{s}. {subject if subject!="Geral" else area}')
    raise ValueError('Subtópico desconhecido: '+item)


def response_shape(value,depth=0):
    """Diagnóstico de contrato sem reproduzir evidências ou texto gerado."""
    if isinstance(value,dict):
        return {k:response_shape(v,depth+1) for k,v in list(value.items())[:30]} if depth<5 else {'type':'object','fields':list(value)[:30]}
    if isinstance(value,list):
        return {'type':'array','count':len(value),'items':[response_shape(v,depth+1) for v in value[:12]] if depth<5 else []}
    return {'type':type(value).__name__,'characters':len(value) if isinstance(value,str) else None}


class Calls:
    def __init__(self, output, config, clients=None):
        self.output,self.config=Path(output),config
        self.clients=dict(clients or {}); self.owned=[]
        self.lock=threading.RLock()
        self.budget=PersistentBudget(self.output/'orcamento.json',config['max_calls'])

    def client(self, role):
        if role not in self.clients:
            load_dotenv(ROOT)
            model,effort=self.config['models'][role].rsplit(':',1)
            self.clients[role]=LLMClient(model,effort,self.output/'.local'/f'{role}.sqlite3',
                self.output/'chamadas_llm.jsonl',provider='azure',budget=self.budget,
                max_calls=self.config['max_calls'],max_attempts=3,timeout=300,
                max_tokens_cap=32000,response_dir=self.output/'.local'/'brutas'/role)
            self.owned.append(role)
        return self.clients[role]

    def call(self, role, system, payload, validate, tokens=10000):
        identity=digest([role,self.config['models'][role],system,payload])
        path=self.output/'chamadas'/(identity+'.json')
        prior=read_json(path)
        if prior:
            validate(prior['response']);return prior['response']
        print(f'[{role}] iniciando chamada',flush=True)
        with self.lock: client=self.client(role)
        diagnostic=self.output/'diagnosticos'/(role+'_'+identity+'.json')
        failures=(read_json(diagnostic) or {}).get('falhas',[])
        def checked(data):
            try:validate(data)
            except ValueError as exc:
                failures.append(dict(erro=str(exc),estrutura=response_shape(data)))
                atomic_json(diagnostic,dict(role=role,model=self.config['models'][role],
                    status='resposta_rejeitada',falhas=failures))
                raise
        response=client.json(system,json.dumps(payload,ensure_ascii=False),tag='v2_'+role,
                                        max_tokens=tokens,validate=checked)
        if failures:atomic_json(diagnostic,dict(role=role,model=self.config['models'][role],status='reparado',falhas=failures))
        atomic_json(path,dict(role=role,model=self.config['models'][role],system=system,request=payload,response=response))
        return response

    def close(self):
        for role in self.owned: self.clients[role].close()


def tokens(value): return set(re.findall(r'[^\W_]+',value.casefold()))


def jaccard(a,b):
    a,b=tokens(a),tokens(b)
    return len(a&b)/max(1,len(a|b))


def load_examples(paths,item):
    """Somente leitura. Exemplos não integram corpus nem suporte factual."""
    result=[]
    for filename in paths:
        path=Path(filename)
        if not path.is_absolute(): path=ROOT/path
        if path.suffix=='.jsonl': rows=[json.loads(s) for s in path.read_text(encoding='utf-8-sig').splitlines() if s.strip()]
        else:
            data=read_json(path)
            rows=data.get('exemplos',[]) if isinstance(data,dict) else data
        require(isinstance(rows,list),'Arquivo de exemplos inválido')
        for r in rows:
            if r.get('item')==item or r.get('status') in ('reprovada','rejeitada'): continue
            question=r.get('pergunta',r.get('question'));answer=r.get('resposta',r.get('answer'))
            if text(question) and text(answer):
                result.append(dict(tipo=r.get('tipo'),pergunta=question,resposta=answer,
                                   origem=str(path),origem_id=r.get('id',r.get('uid'))))
    return result
