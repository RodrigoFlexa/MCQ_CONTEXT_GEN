"""Geração sem recuperação documental; transações por lote e metas congeladas."""
from __future__ import annotations

import copy
import hashlib
import json
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json, squash, tokens
from pipeline.qa_research.tipos import TIPOS, problemas_tipo

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
METAS = HERE / 'metas_geracao_final_20261024.json'
MODELOS = dict.fromkeys(('geracao', 'auditoria', 'refinador', 'dedup'), 'gpt-5-4-petrobras:high')
CAMPOS = {'tipo', 'cenario', 'composicao', 'pergunta', 'resposta'}
MOTIVOS = {'nenhum', 'caso_especifico', 'resposta_vaga', 'lista_generica', 'reformula_enunciado',
           'varias_respostas', 'prudencia_generica', 'trivial', 'sim_nao_disfarcado',
           'tecnicamente_errada', 'sem_confianca', 'fora_do_escopo'}


def sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def agora():
    return datetime.now(timezone.utc).isoformat()


def carregar_metas(path=METAS):
    data = read_json(path)
    if not data or data.get('schema') != 'metas-sem-conteudo-v1':
        raise ValueError('Manifesto de metas inválido')
    items = data.get('itens', [])
    ids = [r['id'] for r in items]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError('Metas vazias ou IDs repetidos')
    for r in items:
        if set(r) != {'id', 'topico', 'subtopico', 'frase_especialista', 'meta'}:
            raise ValueError('As metas devem conter somente rótulos, frase e quantidade')
        if type(r['meta']) is not int or r['meta'] < 1 or any(
                not isinstance(r[k], str) or not r[k].strip() for k in ('id','topico','subtopico','frase_especialista')):
            raise ValueError('Meta e escopo devem estar preenchidos')
    if sum(r['meta'] for r in items) != data.get('total'):
        raise ValueError('Total do manifesto não confere')
    return data


def validar_questao(q):
    if not isinstance(q, dict) or set(q) != CAMPOS:
        raise ValueError('Questão deve ter exatamente tipo, cenario, composicao, pergunta e resposta')
    if q['tipo'] not in TIPOS or type(q['cenario']) is not bool or q['composicao'] not in ('simples','composta'):
        raise ValueError('Tipo, cenário ou composição inválidos')
    if any(not isinstance(q[k],str) or not q[k].strip() for k in ('pergunta','resposta')):
        raise ValueError('Pergunta e resposta devem ser textos preenchidos')


def validar_geracao(d, quantidade):
    if not isinstance(d,dict) or set(d) != {'status','motivo','questoes'}:
        raise ValueError('Use status, motivo e questoes')
    if d['status'] not in ('ok','parcial','sem_questoes') or not isinstance(d['motivo'],str) or not isinstance(d['questoes'],list):
        raise ValueError('Status ou campos inválidos')
    n = len(d['questoes'])
    if n > quantidade or (d['status']=='ok' and n != quantidade) or (d['status']=='parcial' and not 0<n<quantidade) or (d['status']=='sem_questoes' and n):
        raise ValueError('Quantidade incompatível com o status solicitado')
    if d['status']!='ok' and not d['motivo'].strip():
        raise ValueError('Explique a geração incompleta')
    for q in d['questoes']:
        validar_questao(q)


def validar_auditoria(d, ids):
    av = d.get('avaliacoes') if isinstance(d,dict) else None
    if not isinstance(av,list) or any(not isinstance(a,dict) for a in av) or [a.get('id') for a in av] != ids:
        raise ValueError('Uma avaliação por id, na mesma ordem')
    for a in av:
        if set(a) != {'id','aprovada','tipo_sugerido','motivo','justificativa'} or type(a['aprovada']) is not bool or a['tipo_sugerido'] not in TIPOS or a['motivo'] not in MOTIVOS or not isinstance(a['justificativa'],str) or not a['justificativa'].strip():
            raise ValueError('Campos da auditoria inválidos')
        if a['aprovada'] != (a['motivo']=='nenhum'):
            raise ValueError('Aprovação exige motivo nenhum; reprovação exige defeito')


def validar_refino(d):
    if not isinstance(d,dict) or set(d) != {'status','motivo','questao'} or d['status'] not in ('ok','descartar') or not isinstance(d['motivo'],str):
        raise ValueError('Use status, motivo e questao')
    if d['status']=='descartar':
        if d['questao'] is not None or not d['motivo'].strip():
            raise ValueError('Descarte exige questao null e motivo')
    else:
        validar_questao(d['questao'])


def validar_dedup(d, ids):
    if not isinstance(d,dict) or set(d) != {'grupos'} or not isinstance(d['grupos'],list):
        raise ValueError('Use grupos como lista')
    seen=set()
    for g in d['grupos']:
        if not isinstance(g,dict) or set(g) != {'manter','remover','motivo'} or not isinstance(g['remover'],list) or not g['remover'] or not isinstance(g['motivo'],str) or not g['motivo'].strip():
            raise ValueError('Grupo de deduplicação inválido')
        members=[g['manter'],*g['remover']]
        if any(not isinstance(i,str) or i not in ids or i in seen for i in members) or len(set(members))!=len(members):
            raise ValueError('Use somente IDs recebidos, sem repetir membros ou grupos')
        seen.update(members)


def duplicata(q, aprovadas, limiar=.6):
    a=set(tokens(q['pergunta']))
    for other in aprovadas:
        b=set(tokens(other['pergunta']))
        if squash(q['pergunta']) == squash(other['pergunta']) or len(a&b)/max(1,len(a|b)) >= limiar:
            return other['uid']
    return None


class GeracaoSemConteudo:
    def __init__(self, saida, *, metas=METAS, itens=None, lote=5, memoria=20, refinos=2,
                 workers=5, max_lotes=100, max_sem_progresso=10, max_chamadas=30000,
                 modelos=None, clientes=None, progress=print):
        self.saida = Path(saida)
        self.manifesto=carregar_metas(metas)
        stored=read_json(self.saida/'config.json') or {}
        ids=list(itens or stored.get('itens') or [r['id'] for r in self.manifesto['itens']])
        if len(ids)!=len(set(ids)) or set(ids)-{r['id'] for r in self.manifesto['itens']}:
            raise ValueError('Lista de tópicos inválida')
        self.itens=[next(r for r in self.manifesto['itens'] if r['id']==i) for i in ids]
        for k,v in dict(lote=lote,memoria=memoria,workers=workers,max_lotes=max_lotes,
                        max_sem_progresso=max_sem_progresso,max_chamadas=max_chamadas).items():
            if type(v) is not int or v<1:
                raise ValueError(k+' deve ser inteiro positivo')
        if type(refinos) is not int or not 0<=refinos<=2:
            raise ValueError('refinos deve estar entre 0 e 2')
        self.lote,self.memoria,self.refinos,self.workers=lote,memoria,refinos,workers
        self.max_lotes,self.max_sem_progresso,self.max_chamadas=max_lotes,max_sem_progresso,max_chamadas
        self.modelos={**MODELOS,**(modelos or {})}
        self.clientes=dict(clientes or {})
        self.progress=progress
        self.lock=threading.Lock()
        self.budget=None
        self.prompts={role:(HERE/'prompts'/f'{role}.md').read_text(encoding='utf-8') for role in MODELOS}

    def config(self):
        cfg={'schema':'geracao-sem-conteudo-v1','itens':[r['id'] for r in self.itens],
             'escopos_e_metas':self.itens,'manifesto_sha256':sha(self.manifesto),'modelos':self.modelos,
             'lote':self.lote,'memoria':self.memoria,'refinos':self.refinos,'jaccard':.6,
             'prompts_sha256':{k:sha(v) for k,v in self.prompts.items()},
             'regras_sha256':sha([(ROOT/f).read_text(encoding='utf-8') for f in (
                 'pipeline/qa_research/tipos.py','pipeline/qa_research/dificuldade.py',
                 'pipeline/inventario/textutil.py')]), 'motor_sha256':sha(Path(__file__).read_text(encoding='utf-8')),
             'conteudo_externo':False,'exemplos_herdados':False}
        old=read_json(self.saida/'config.json')
        if old and {k:v for k,v in old.items() if k!='criado_em'} != cfg:
            raise ValueError('Configuração mudou: use outra --saida para outro experimento')
        if not old:
            atomic_json(self.saida/'config.json',{**cfg,'criado_em':agora()})
        atomic_json(self.saida/'metas.json',self.manifesto)
        atomic_json(self.saida/'limites_execucao.json',{'max_lotes_por_topico':self.max_lotes,
                    'max_sem_progresso':self.max_sem_progresso,'max_chamadas_cumulativas':self.max_chamadas})

    def cliente(self, role):
        with self.lock:
            if role not in self.clientes:
                from pipeline.qa_research.runtime import PersistentBudget
                from pipeline.inventario.llm import LLMClient, load_dotenv
                load_dotenv(ROOT)
                if self.budget is None:
                    self.budget=PersistentBudget(self.saida/'orcamento.json',self.max_chamadas)
                model,effort=self.modelos[role].rsplit(':',1)
                self.clientes[role]=LLMClient(model,effort,self.saida/'.local'/f'{role}.sqlite3',
                    self.saida/'chamadas'/f'{role}.jsonl',provider='azure',budget=self.budget,
                    max_attempts=3,max_calls=self.max_chamadas,max_tokens_cap=32000,timeout=600,
                    response_dir=self.saida/'.local'/'respostas'/role)
            return self.clientes[role]

    def chamar(self, role, payload, item, validate):
        return self.cliente(role).json(self.prompts[role],json.dumps(payload,ensure_ascii=False,sort_keys=True),
                    tag='sem_conteudo_'+role,max_tokens=16000,item=item,validate=validate)

    @staticmethod
    def escopo(item):
        return {k:item[k] for k in ('topico','subtopico','frase_especialista')}

    def recentes(self,state,excluir=None):
        return [{k:q[k] for k in ('pergunta','resposta')} for q in state['recentes']
                if not excluir or not q['uid'].startswith(excluir)]

    def lembrar(self,state,q):
        state['recentes']=(state['recentes']+[{k:q[k] for k in ('uid','pergunta','resposta')}])[-self.memoria:]

    def auditar(self,qs,item):
        if not qs:
            return []
        ids=[q['uid'] for q in qs]
        payload={'escopo':self.escopo(item),'questoes':[{'id':q['uid'],**{k:q[k] for k in CAMPOS}} for q in qs]}
        return self.chamar('auditoria',payload,item['id'],lambda d:validar_auditoria(d,ids))['avaliacoes']

    def aceitar(self,q,a,state):
        q['auditoria']=a
        q['tipo_declarado']=q['tipo']
        q['tipo']=a['tipo_sugerido']
        problems=problemas_tipo(q['tipo'],q['cenario'],q['pergunta'],q['resposta'])
        match=duplicata(q,state['aprovadas'])
        q['problemas_codigo']=problems
        q['duplicata_de']=match
        q['aprovada']=a['aprovada'] and not problems and match is None
        state['questoes'].append(q)
        if q['aprovada']:
            state['aprovadas'].append(q)
        return q['aprovada']

    def lote_novo(self,item,state):
        state=copy.deepcopy(state)  # checkpoint só depois do lote inteiro; cache permite replay após falha
        n=min(self.lote,item['meta']-len(state['aprovadas']))
        rodada=state['lotes']+1
        payload={'escopo':self.escopo(item),'lote':rodada,'quantidade':n,'recentes':self.recentes(state)}
        result=self.chamar('geracao',payload,item['id'],lambda d:validar_geracao(d,n))
        qs=[]
        for i,q in enumerate(result['questoes'],1):
            q={**q,'uid':f"{item['id']}:sc:{rodada:04}:{i}",'item':item['id'],
               'origem':'sem_conteudo','rodada':rodada,'blocos':[]}
            self.lembrar(state,q)
            qs.append(q)
        reviews=self.auditar(qs,item)
        for q,a in zip(qs,reviews):
            if self.aceitar(q,a,state) or q['duplicata_de']:
                continue
            original=q
            for attempt in range(1,self.refinos+1):
                payload={'escopo':self.escopo(item),'original':{k:q[k] for k in CAMPOS},
                         'critica':{'auditoria':q['auditoria'],'problemas_codigo':q['problemas_codigo']},
                         'tentativa':attempt,'recentes':self.recentes(state,original['uid'])}
                r=self.chamar('refinador',payload,item['id'],validar_refino)
                if r['status']=='descartar':
                    state['eventos'].append({'etapa':'refino','uid':q['uid'],'motivo':r['motivo']})
                    break
                previous=q
                q={**r['questao'],'uid':original['uid']+f':ref{attempt}','item':item['id'],
                   'origem':'refinada','rodada':rodada,'blocos':[],'original_uid':original['uid']}
                self.lembrar(state,q)
                # Reescrita apenas cosmética não recupera uma questão reprovada.
                if squash(q['pergunta'])==squash(previous['pergunta']) and squash(q['resposta'])==squash(previous['resposta']):
                    q.update(aprovada=False,motivo_codigo='refino_identico')
                    state['questoes'].append(q)
                    break
                a=self.auditar([q],item)[0]
                if self.aceitar(q,a,state) or q['duplicata_de']:
                    break
        state['lotes']=rodada
        state['eventos'].append({'etapa':'geracao','lote':rodada,'status':result['status'],'motivo':result['motivo']})
        return state

    def deduplicar(self,item,state):
        qs=state['aprovadas']
        if len(qs)<2:
            return state
        ids=[q['uid'] for q in qs]
        payload={'escopo':self.escopo(item),'questoes':[{'id':q['uid'],'pergunta':q['pergunta'],'resposta':q['resposta']} for q in qs]}
        d=self.chamar('dedup',payload,item['id'],lambda d:validar_dedup(d,ids))
        removidos={i for g in d['grupos'] for i in g['remover']}
        for q in state['questoes']:
            if q['uid'] in removidos:
                q['aprovada']=False
                q['redundante']=True
        state['aprovadas']=[q for q in qs if q['uid'] not in removidos]
        state['eventos'].append({'etapa':'dedup','lote':state['lotes'],**d})
        return state

    def topico(self,item):
        directory=self.saida/'topicos'/item['id']
        path=directory/'estado.json'
        state=read_json(path) or {'lotes':0,'sem_progresso':0,'questoes':[],'aprovadas':[],
                                 'recentes':[],'eventos':[],'concluido':False}
        if state['concluido']:
            self.publicar(item,state)
            return True
        while True:
            before=len(state['aprovadas'])
            try:
                if before >= item['meta']:
                    state=self.deduplicar(item,copy.deepcopy(state))
                    state['concluido']=len(state['aprovadas'])==item['meta']
                    atomic_json(path,state)
                    if state['concluido']:
                        self.publicar(item,state)
                        self.progress(f"[{item['id']}] concluído: {item['meta']}/{item['meta']}",flush=True)
                        return True
                if state['lotes']>=self.max_lotes or state['sem_progresso']>=self.max_sem_progresso:
                    state['erro']='Meta incompleta: limite cumulativo de lotes ou de lotes sem progresso atingido'
                    atomic_json(path,state)
                    self.publicar(item,state)
                    return False
                state=self.lote_novo(item,state)
                state.pop('erro',None)
                state['sem_progresso']=state['sem_progresso']+1 if len(state['aprovadas'])<=before else 0
                atomic_json(path,state)
                self.progress(f"[{item['id']}] lote {state['lotes']}: {len(state['aprovadas'])}/{item['meta']} aprovadas",flush=True)
            except Exception as exc:
                state['erro']=f'{type(exc).__name__}: {str(exc)[:1500]}'
                atomic_json(path,state)
                self.publicar(item,state)
                self.progress(f"[{item['id']}] interrompido; progresso salvo: {state['erro']}",flush=True)
                return False

    @staticmethod
    def jsonl(path,rows):
        path.parent.mkdir(parents=True,exist_ok=True)
        tmp=path.with_suffix('.jsonl.tmp')
        tmp.write_text(''.join(json.dumps(q,ensure_ascii=False)+'\n' for q in rows),encoding='utf-8')
        tmp.replace(path)

    def publicar(self,item,state):
        directory=self.saida/'topicos'/item['id']
        self.jsonl(directory/'questoes.jsonl',state['questoes'])
        self.jsonl(directory/'aprovadas.jsonl',state['aprovadas'])
        if state['concluido']:
            atomic_json(directory/'finalizado.json',{'aprovadas':len(state['aprovadas']),'meta':item['meta'],'em':agora()})

    def relatorio(self):
        allqs,approved,summaries=[],[],[]
        for item in self.itens:
            s=read_json(self.saida/'topicos'/item['id']/'estado.json') or {}
            allqs+=s.get('questoes',[])
            approved+=s.get('aprovadas',[])
            summaries.append({'id':item['id'],'subtopico':item['subtopico'],'meta':item['meta'],
                'aprovadas':len(s.get('aprovadas',[])),'lotes':s.get('lotes',0),
                'concluido':s.get('concluido',False),'erro':s.get('erro')})
        self.jsonl(self.saida/'questoes.jsonl',allqs)
        self.jsonl(self.saida/'aprovadas.jsonl',approved)
        summary={'meta_total':sum(i['meta'] for i in self.itens),'aprovadas':len(approved),
                 'tentativas_de_questao':len(allqs),'origens_aprovadas':dict(Counter(q['origem'] for q in approved)),
                 'tipos_aprovadas':dict(Counter(q['tipo'] for q in approved)), 'topicos':summaries}
        atomic_json(self.saida/'resultado.json',summary)
        lines=['# Geração sem conteúdo externo','',
            f"Aprovadas automaticamente: **{len(approved)}/{summary['meta_total']}**. Fonte das metas: `{self.manifesto['run_referencia']}`.",
            '', 'Entradas: tópico, subtópico, frase do especialista e memória das questões desta run. '
            'Sem documentos, recuperação, exemplos ou bancos herdados. A auditoria usa conhecimento paramétrico; '
            'aprovação não significa validação documental nem humana. Deduplicação por sentido dentro de cada tópico; '
            'redundância entre tópicos deve ser medida na análise final. Tipos e composições não têm cotas.', '',
            '| ID | Subtópico | Meta | Aprovadas | Lotes | Situação |','|---|---|---:|---:|---:|---|']
        for s in summaries:
            status='concluído' if s['concluido'] else (s['erro'] or 'pendente')
            lines.append(f"| {s['id']} | {s['subtopico']} | {s['meta']} | {s['aprovadas']} | {s['lotes']} | {status.replace('|','/')} |")
        (self.saida/'RELATORIO.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
        return summary

    def run(self):
        with output_lock(self.saida):
            self.config()
            marker=self.saida/'geracao_concluida.json'
            marker.unlink(missing_ok=True)
            try:
                with ThreadPoolExecutor(max_workers=self.workers) as pool:
                    ok=list(pool.map(self.topico,self.itens))
                result=self.relatorio()
                if all(ok):
                    atomic_json(marker,{'em':agora(),'aprovadas':result['aprovadas']})
                return 0 if all(ok) else 2
            finally:
                for c in self.clientes.values():
                    if hasattr(c,'close'):
                        c.close()
