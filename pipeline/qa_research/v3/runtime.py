"""Cliente assíncrono: prazo total, duas tentativas, cache validado e progresso."""
import asyncio
import hashlib
import json
import ssl
import time
from datetime import datetime, timezone
from pathlib import Path

from pipeline.inventario.llm import is_content_filter, is_fatal, is_transient, retry_after
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.runtime import PersistentBudget
from . import contracts as C, prompts as P

ROOT=Path(__file__).resolve().parents[3]
LABELS=dict(plan='planejamento',write='redação',review='revisão',author='questões',
    solve='resolução',judge='revisão de questões',refine='refino')


def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()


def stamp(): return datetime.now(timezone.utc).isoformat()


class CallFailure(RuntimeError): pass
class Fatal(CallFailure): pass


def safe_error(exc):
    if isinstance(exc,ValueError): return str(exc)[:800]
    status=getattr(exc,'status_code',None)
    return f'{type(exc).__name__}'+(f' HTTP {status}' if status else '')


class Calls:
    def __init__(self, output, config, transport=None, progress=print):
        self.output,self.config=Path(output),config
        self.transport,self.progress=transport,progress
        self.budget=PersistentBudget(self.output/'orcamento.json',config['max_calls'])
        self.slots=asyncio.Semaphore(config['workers'])
        self.clients=[];self.client=None;self.settings=None;self.abort=False
        if transport is None:
            from azure_openai_backend import AzureSettings
            self.settings=AzureSettings.load();self.settings.require()
            self.backend=dict(endpoint=digest(self.settings.azure_endpoint),api_version=self.settings.azure_api_version)
        else:self.backend={'transport':'simulado'}

    def log(self, row):
        path=self.output/'chamadas_llm.jsonl';path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('a',encoding='utf-8') as stream:
            stream.write(json.dumps(dict(at=stamp(),**row),ensure_ascii=False)+'\n')

    def make_client(self):
        import httpx
        from openai import AsyncAzureOpenAI
        settings=self.settings
        context=ssl.create_default_context()
        if settings.ca_bundle:context.load_verify_locations(cafile=settings.ca_bundle)
        kwargs=dict(api_key=settings.azure_api_key,api_version=settings.azure_api_version,
            max_retries=0,timeout=self.config['request_timeout'],
            http_client=httpx.AsyncClient(verify=context,timeout=self.config['request_timeout']))
        kwargs['base_url' if settings.use_base_url else 'azure_endpoint']=settings.azure_endpoint
        self.client=AsyncAzureOpenAI(**kwargs);self.clients.append(self.client)

    async def request(self, role, messages, tokens):
        if self.transport is not None:return await self.transport(role,messages,tokens)
        if self.client is None:self.make_client()
        model,effort=self.config['models'][role].rsplit(':',1)
        return await self.client.chat.completions.create(model=model,reasoning_effort=effort,
            max_completion_tokens=tokens,response_format={'type':'json_object'},messages=messages)

    def refresh(self):
        if self.settings is None:return False
        from azure_openai_backend import AzureSettings
        changed=AzureSettings.load(override=True);changed.require()
        C.require(self.backend==dict(endpoint=digest(changed.azure_endpoint),api_version=changed.azure_api_version),
            'Endpoint/API version mudaram durante a execução; retome em outra saída')
        if changed.azure_api_key==self.settings.azure_api_key:return False
        self.settings=changed;self.make_client();return True

    async def call(self, role, tag, payload, validate, system=None, tokens=None):
        system=system or P.PROMPTS[role]
        initial=tokens or self.config['output_tokens']
        body=json.dumps(payload,ensure_ascii=False)
        C.require(len(body)+len(system)<=self.config['max_input_chars'],tag+': entrada excedeu max_input_chars; reduza o lote ou divida a revisão')
        key=digest([C.VERSION,self.backend,self.config['models'][role],system,payload])
        path=self.output/'.local'/'chamadas'/(key+'.json')
        step='seleção' if system==P.SELECT else LABELS.get(role,role)
        label=f'[{step}:{tag}]'

        def retry_message(reason, action='Repetindo uma vez'):
            self.progress(f'{label} {reason}. {action}.',flush=True)

        def checked(data):
            try:
                C.require(isinstance(data,dict),'Resposta deve ser objeto JSON');validate(data)
            except (KeyError,TypeError,IndexError) as exc:
                raise ValueError('Estrutura inválida: '+str(exc)) from exc

        saved=read_json(path)
        if saved is not None:
            try:checked(saved['response'])
            except ValueError:pass
            else:
                self.progress(f'{label} resultado anterior reutilizado',flush=True)
                return saved['response']
        state={'fase':'aguardando vaga','tentativa':0,'inicio_fase':time.monotonic()};started=time.monotonic()

        async def heartbeat():
            while True:
                await asyncio.sleep(self.config['heartbeat'])
                elapsed=time.monotonic()-state['inicio_fase']
                self.progress(f'{label} {state["fase"]} há {elapsed:.0f}s',flush=True)

        ticker=asyncio.create_task(heartbeat())
        try:
            async with self.slots:
                queued=round(time.monotonic()-started,2)
                messages=[dict(role='system',content=system),dict(role='user',content=body)]
                current=initial
                for attempt in range(1,3):
                    if self.abort:raise Fatal('Execução interrompida por falha fatal; checkpoints preservados')
                    self.budget.reserve(); state.update(fase='aguardando resposta',tentativa=attempt,inicio_fase=time.monotonic())
                    if self.config.get('verbose'):
                        self.progress(f'{label} tentativa {attempt}/2 | limite {current} tokens | fila {queued:.1f}s',flush=True)
                    elif attempt==1:
                        self.progress(f'{label} iniciando'+(f' após {queued:.0f}s na fila' if queued>=1 else ''),flush=True)
                    t0=time.monotonic();meta=dict(id=key,role=role,tag=tag,model=self.config['models'][role],
                        attempt=attempt,max_tokens=current,queue_seconds=queued)
                    try:
                        response=await asyncio.wait_for(self.request(role,messages,current),timeout=self.config['request_timeout'])
                    except asyncio.CancelledError:
                        self.log(dict(**meta,ok=False,kind='cancelada',seconds=round(time.monotonic()-t0,2)));raise
                    except Exception as exc:
                        elapsed=round(time.monotonic()-t0,2)
                        kind='prazo' if isinstance(exc,TimeoutError) else 'transitorio' if is_transient(exc) else 'requisicao'
                        self.log(dict(**meta,ok=False,kind=kind,error=safe_error(exc),seconds=elapsed))
                        if attempt<2 and getattr(exc,'status_code',None)==401 and self.refresh():
                            retry_message('Credencial renovada');continue
                        if is_fatal(exc) or (kind=='requisicao' and not is_content_filter(exc)):
                            self.abort=True;raise Fatal(f'{tag}: {safe_error(exc)}; verifique deployment, credenciais e configuração') from exc
                        if attempt==2 or is_content_filter(exc):raise CallFailure(f'{tag}: {safe_error(exc)}') from exc
                        retry_message('Prazo da requisição esgotado' if kind=='prazo' else 'Falha temporária do serviço: '+safe_error(exc))
                        state.update(fase='aguardando nova chamada',inicio_fase=time.monotonic())
                        await asyncio.sleep(min(30,max(1,retry_after(exc))));continue
                    seconds=round(time.monotonic()-t0,2)
                    choice=response.choices[0];finish=choice.finish_reason
                    content=choice.message.content or ''
                    usage=getattr(response,'usage',None)
                    meta.update(seconds=seconds,finish=finish,prompt_tokens=getattr(usage,'prompt_tokens',0) or 0,
                        completion_tokens=getattr(usage,'completion_tokens',0) or 0)
                    atomic_json(self.output/'.local'/'brutas'/f'{key}_{attempt}_{time.time_ns()}.json',dict(**meta,content=content))
                    if finish=='content_filter':
                        self.log(dict(**meta,ok=False,kind='filtro_conteudo'));raise CallFailure(tag+': filtro de conteúdo')
                    if finish=='length':
                        self.log(dict(**meta,ok=False,kind='truncada'))
                        if attempt==2:raise CallFailure(tag+': resposta truncada após duas tentativas')
                        retry_message('Resposta interrompida pelo limite de saída','Repetindo uma vez com mais espaço para a resposta')
                        current=max(current,self.config['retry_tokens']);continue
                    try:
                        data=json.loads(content);checked(data)
                    except ValueError as exc:
                        message=safe_error(exc)
                        self.log(dict(**meta,ok=False,kind='validacao',error=message))
                        if attempt==2:raise CallFailure(tag+': '+message) from exc
                        retry_message('Resposta fora do formato esperado: '+message[:250],'Solicitando uma correção de formato')
                        # Reparo compacto: não acrescente a resposta anterior inteira.
                        messages=[dict(role='system',content=system),dict(role='user',content=body),
                            dict(role='user',content='Corrija este erro de contrato e devolva o JSON completo: '+message)]
                        continue
                    self.log(dict(**meta,ok=True))
                    atomic_json(path,dict(role=role,tag=tag,request=payload,system=system,response=data))
                    self.progress(f'{label} concluído em {seconds:.1f}s',flush=True)
                    return data
        finally:
            ticker.cancel()
            await asyncio.gather(ticker,return_exceptions=True)

    async def close(self):
        for client in self.clients:await client.close()


def topic(item):
    from pipeline.fase_3.topicos import TOPICOS
    for ai,(area,subjects) in enumerate(TOPICOS.items(),1):
        for si,(subject,phrase) in enumerate(subjects.items(),1):
            if item==f'{ai:02}_{si:02}':return dict(id=item,topico=area,subtopico=subject,
                frase_especialista=phrase,titulo=f'{ai}.{si}. {subject if subject!="Geral" else area}')
    raise ValueError('Subtópico desconhecido: '+item)


def load_examples(paths, item):
    examples=[]
    for path in paths:
        path=Path(path)
        if not path.is_absolute():path=ROOT/path
        if path.suffix=='.jsonl':data=[json.loads(s) for s in path.read_text(encoding='utf-8-sig').splitlines() if s.strip()]
        else:
            data=json.loads(path.read_text(encoding='utf-8-sig'))
            if isinstance(data,dict):data=data.get('exemplos')
        C.require(isinstance(data,list),'Exemplos: array esperado em '+str(path))
        for r in data:
            if r.get('item')==item or r.get('status') in ('reprovada','rejeitada'):continue
            q,a=r.get('pergunta',r.get('question')),r.get('resposta',r.get('answer'))
            if C.text(q) and C.text(a):examples.append(dict(tipo=r.get('tipo'),pergunta=q,resposta=a,origem=str(path),id=r.get('id')))
    return examples
