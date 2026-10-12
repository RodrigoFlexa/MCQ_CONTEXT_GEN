"""Embeddings Azure exclusivos, cache persistente e cobertura integral do texto."""
import hashlib
import json
import random
import sqlite3
import time
from pathlib import Path

import numpy as np

from .storage import atomic_json, append_jsonl, utc_now, CallLimitReached


class AzureEmbeddingBackend:
    def __init__(self,cfg,store=None,client=None,settings=None):
        self.cfg,self.store=cfg,store
        if client is None:
            from azure_openai_backend import AzureSettings, AzureOpenAIBackend
            from openai import AzureOpenAI
            self.settings=settings or AzureSettings.load();self.settings.require()
            kwargs={'api_key':self.settings.azure_api_key,'api_version':self.settings.azure_api_version,
                    'max_retries':0,'timeout':300}
            http=AzureOpenAIBackend._build_http_client(self.settings.ca_bundle,300)
            if http is not None:kwargs['http_client']=http
            kwargs['base_url' if self.settings.use_base_url else 'azure_endpoint']=self.settings.azure_endpoint
            client=AzureOpenAI(**kwargs)
        else:self.settings=settings
        self.client=client

    def create(self,inputs):
        if self.store:
            state=self.store.state
            if state['api_calls']>=self.cfg.max_calls:raise CallLimitReached('Limite de chamadas atingido antes de embeddings')
            state['api_calls']+=1;roles=state['calls_by_role'];roles['embeddings']=roles.get('embeddings',0)+1
            self.store.save_state()
        start=utc_now();timer=time.monotonic();error=None;usage=None;model=None;http_attempts=0
        try:
            from azure_openai_backend import _is_retryable, _retry_after_seconds
            for attempt in range(6):
                http_attempts+=1
                try:
                    result=self.client.embeddings.create(model=self.cfg.embedding_deployment,input=inputs,
                        encoding_format='float')
                    usage=getattr(result,'usage',None);model=getattr(result,'model',None)
                    return result
                except Exception as exc:
                    if not _is_retryable(exc) or attempt==5:raise
                    time.sleep(min(60,max(_retry_after_seconds(exc),(2**attempt)*(.5+random.random()))))
        except BaseException as exc:error=type(exc).__name__;raise
        finally:
            record={'role':'embeddings','deployment':self.cfg.embedding_deployment,'model':model,
                'dimensions':self.cfg.embedding_dimensions,'started_at':start,'finished_at':utc_now(),
                'elapsed_seconds':round(time.monotonic()-timer,3),'input_items':len(inputs),
                'input_tokens_counted':sum(len(i) for i in inputs),'http_attempts':http_attempts,'error_type':error,
                'prompt_tokens':getattr(usage,'prompt_tokens',None),'total_tokens':getattr(usage,'total_tokens',None)}
            append_jsonl(Path(self.cfg.output)/'chamadas_embeddings.jsonl',record)
            if self.store:
                total=self.store.state.setdefault('embedding_usage',{'calls':0,'prompt_tokens':0,'usage_missing':0})
                total['calls']+=1
                if usage is None:total['usage_missing']+=1
                else:total['prompt_tokens']+=getattr(usage,'prompt_tokens',0) or 0
                self.store.save_state()


class AzureFullTextEmbedder:
    def __init__(self,cfg,backend=None,tokenizer=None,store=None):
        self.cfg=cfg;self.dim=cfg.embedding_dimensions;self.window=cfg.embedding_max_tokens
        self.overlap=cfg.embedding_overlap_tokens
        if not 0<=self.overlap<self.window:raise ValueError('Sobreposição inválida para embeddings Azure')
        if tokenizer is None:
            from .prepare_tokenizer import ensure_tokenizer
            tokenizer=ensure_tokenizer()
        self.tokenizer=tokenizer;self.backend=backend or AzureEmbeddingBackend(cfg,store)
        api_version=getattr(getattr(self.backend,'settings',None),'azure_api_version',None)
        self.protocol={'provider':'azure','name':cfg.embedding_model,'deployment':cfg.embedding_deployment,
            'declared_model_version':'1','dimensions':self.dim,'max_tokens':self.window,'window':self.window,
            'overlap':self.overlap,'tokenizer':'cl100k_base','api_version':api_version,
            'aggregation':'mean_weighted_new_tokens_l2_v1'}
        endpoint=getattr(getattr(self.backend,'settings',None),'azure_endpoint',None)
        self.protocol['endpoint_signature']=hashlib.sha256(endpoint.encode()).hexdigest() if endpoint else None
        root=Path(cfg.output)/'dominio/embeddings';root.mkdir(parents=True,exist_ok=True)
        path=root/'protocolo_azure.json'
        if path.exists() and json.loads(path.read_text(encoding='utf-8'))!=self.protocol:
            raise ValueError('Protocolo de embeddings mudou; use outra saída')
        if (root/'cache.npz').exists() or (root/'protocolo.json').exists():
            raise ValueError('Esta pasta contém embeddings locais anteriores; use uma nova saída')
        self.cache=sqlite3.connect(root/'azure_cache.sqlite3')
        atomic_json(path,self.protocol)
        self.cache.execute('CREATE TABLE IF NOT EXISTS vectors (key TEXT PRIMARY KEY, vector BLOB NOT NULL)')
        self.cache.commit()

    def tokens(self,text):return self.tokenizer.encode(text,disallowed_special=())

    def windows(self,text):
        ids=self.tokens(text)
        if not ids:raise ValueError('Não é permitido enviar texto vazio ao modelo de embeddings')
        pieces=[];weights=[];step=self.window-self.overlap
        for start in range(0,len(ids),step):
            part=ids[start:start+self.window];pieces.append(part)
            weights.append(len(part) if start==0 else max(1,len(part)-self.overlap))
            if start+self.window>=len(ids):break
        return pieces,weights

    def _get(self,key):
        row=self.cache.execute('SELECT vector FROM vectors WHERE key=?',(key,)).fetchone()
        if row is None:return None
        vector=np.frombuffer(row[0],dtype=np.float32).copy()
        if vector.shape!=(self.dim,) or not np.isfinite(vector).all():raise ValueError('Cache Azure inválido')
        return vector

    def _put(self,key,vector):
        self.cache.execute('INSERT OR REPLACE INTO vectors VALUES (?,?)',(key,np.asarray(vector,dtype=np.float32).tobytes()))
        self.cache.commit()

    def _vectors(self,inputs):
        result=self.backend.create(inputs);data=getattr(result,'data',None)
        if not isinstance(data,list) or len(data)!=len(inputs):raise ValueError('Resposta de embeddings incompleta')
        rows={}
        for item in data:
            index=getattr(item,'index',None)
            if type(index) is not int or index in rows or not 0<=index<len(inputs):raise ValueError('Índices de embeddings inválidos')
            vector=np.asarray(getattr(item,'embedding',None),dtype=np.float32)
            if vector.shape!=(self.dim,) or not np.isfinite(vector).all() or np.linalg.norm(vector)==0:
                raise ValueError('Vetor de embeddings inválido ou dimensão diferente de 3072')
            rows[index]=vector/max(float(np.linalg.norm(vector)),1e-12)
        return [rows[i] for i in range(len(inputs))]

    def encode(self,textos,batch_size=None,usar_cache=True,progresso=False):
        texts=list(textos)
        if not texts:return np.zeros((0,self.dim),dtype=np.float32)
        outputs={};batch=[];locations=[];tokens=0
        size=min(batch_size or self.cfg.embedding_batch_size,self.cfg.embedding_batch_size)
        def flush():
            nonlocal tokens
            if not batch:return
            vectors=self._vectors(batch)
            for (key,weight),vector in zip(locations,vectors):
                state=outputs[key];state['sum']+=weight*vector;state['received']+=1
                if state['received']==state['expected']:
                    average=state['sum']/state['total_weight'];norm=float(np.linalg.norm(average))
                    if norm<1e-12:raise ValueError('Agregação de embeddings resultou em vetor nulo')
                    self._put(key,average/norm)
            batch.clear();locations.clear();tokens=0
        keys=[]
        for text in texts:
            key=hashlib.sha256(text.encode()).hexdigest();keys.append(key)
            if key in outputs or (usar_cache and self._get(key) is not None):continue
            pieces,weights=self.windows(text)
            outputs[key]={'sum':np.zeros(self.dim,dtype=np.float32),'received':0,'expected':len(pieces),'total_weight':sum(weights)}
            for piece,weight in zip(pieces,weights):
                if len(piece)>self.cfg.embedding_batch_tokens:raise ValueError('Janela excede o orçamento de tokens do lote')
                if batch and (len(batch)>=size or tokens+len(piece)>self.cfg.embedding_batch_tokens):flush()
                batch.append(piece);locations.append((key,weight));tokens+=len(piece)
        flush()
        return np.stack([self._get(key) for key in keys])

    def diagnostics(self,text):
        return {'tokens':len(self.tokens(text)),'windows':len(self.windows(text)[0]),
                'provider':'azure','deployment':self.cfg.embedding_deployment,'silently_truncated':False}

    def salvar_cache(self):self.cache.commit()

    def close(self):
        self.cache.close()
        client=getattr(self.backend,'client',None)
        if client is not None and hasattr(client,'close'):client.close()
