"""Cliente JSON Azure (padrão) ou OpenAI explícito: cache, retentativas, reparo e diagnóstico.

Política de erros (cada pedido é independente; a etapa decide se continua):
- filtro de conteúdo da Azure (no prompt ou na resposta) -> ContentFiltered, sem repetir;
- resposta inválida (JSON ou validação) -> nova tentativa com o erro devolvido ao modelo;
- resposta truncada (finish_reason=length) -> nova tentativa com mais tokens;
- 408/409/429/5xx, timeout e conexão -> espera (Retry-After) e repete;
- 401/403/404 -> erro fatal de configuração (interrompe a execução);
- esgotadas as tentativas -> CallFailed com o último motivo, nunca só "RuntimeError".
Cada tentativa é registrada com a mensagem do erro em chamadas_llm.jsonl.
Credenciais nunca entram no cache nem no log.
"""
import json
import os
import random
import sqlite3
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from .textutil import atomic_json, sha


class LLMError(RuntimeError):
    kind = 'erro'

    def __init__(self, message, kind=None, tag='', item=None):
        super().__init__(message)
        self.kind = kind or self.kind
        self.tag = tag
        self.item = item


class BudgetExceeded(LLMError):
    kind = 'orcamento'


class CallBudget:
    """Limite global de tentativas de API, compartilhado entre deployments e workers."""

    def __init__(self, limit):
        self.limit, self.used = limit, 0
        self.lock = threading.Lock()

    def reserve(self):
        with self.lock:
            if self.used >= self.limit:
                raise BudgetExceeded(f'Limite global de {self.limit} chamadas atingido')
            self.used += 1


class ContentFiltered(LLMError):
    """Bloqueio do filtro de conteúdo (Responsible AI). Item é pulado; a execução segue."""
    kind = 'filtro_conteudo'


class CallFailed(LLMError):
    """Esgotou as tentativas: validação, truncamento ou indisponibilidade persistente."""
    kind = 'falha_chamada'


FATAL_STATUS = (401, 403, 404)


def load_dotenv(root):
    path = Path(root) / '.env'
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _status(exc):
    return getattr(exc, 'status_code', None) or getattr(exc, 'status', None)


def _error_body_text(exc):
    parts = [str(exc)]
    for attr in ('body', 'response'):
        value = getattr(exc, attr, None)
        if value is None:
            continue
        if attr == 'response':
            value = getattr(value, 'text', None)
        try:
            parts.append(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False))
        except (TypeError, ValueError):
            parts.append(repr(value))
    code = getattr(exc, 'code', None)
    if code:
        parts.append(str(code))
    return ' '.join(p for p in parts if p)


def is_content_filter(exc):
    """Azure devolve 400 com code=content_filter / ResponsibleAIPolicyViolation para prompts bloqueados."""
    text = _error_body_text(exc).casefold()
    return any(t in text for t in ('content_filter', 'content filter', 'responsibleaipolicyviolation',
                                   'content management policy'))


def is_quota_exhausted(exc):
    """Saldo ou cota esgotados (429 permanente): esperar não resolve."""
    text = str(exc).casefold()
    return any(tok in text for tok in ('insufficient_quota', 'credit_balance_exhausted', 'billing_hard_limit'))


def is_transient(exc):
    if is_quota_exhausted(exc):
        return False
    if _status(exc) in (408, 409, 429, 500, 502, 503, 504):
        return True
    name = type(exc).__name__
    return any(tok in name for tok in ('RateLimit', 'Timeout', 'APIConnection', 'InternalServer',
                                       'ServiceUnavailable', 'ConnectError', 'ReadError', 'RemoteProtocol'))


def is_fatal(exc):
    if is_quota_exhausted(exc) or _status(exc) in FATAL_STATUS:
        return True
    return type(exc).__name__ in ('AuthenticationError', 'PermissionDeniedError', 'NotFoundError')


def retry_after(exc):
    headers = getattr(getattr(exc, 'response', None), 'headers', None) or {}
    for key, scale in (('retry-after-ms', 1000.0), ('Retry-After-Ms', 1000.0), ('retry-after', 1.0),
                       ('Retry-After', 1.0)):
        if key in headers:
            try:
                return float(headers[key]) / scale
            except (TypeError, ValueError):
                pass
    return 0.0


class LLMClient:
    def __init__(self, model, effort, cache_path, log_path, max_calls=50000, timeout=600, api_key=None,
                 provider='azure', client=None, settings=None, max_attempts=6, max_tokens_cap=32000,
                 sleep=None, budget=None, log_lock=None, api_version=None, response_dir=None):
        if provider not in ('azure', 'openai'):
            raise ValueError('Provider inválido')
        identity = {'provider': provider}
        if provider == 'azure':
            from azure_openai_backend import AzureSettings, AzureOpenAIBackend
            settings = settings or (AzureSettings.load() if client is None else None)
            # Alguns deployments (o3, o4-mini) exigem outra API version; o padrão vem da configuração Azure.
            version = api_version or (settings.azure_api_version if settings else None)
            if settings:
                settings.require()
                identity.update(endpoint_sha=sha(settings.azure_endpoint, 40), api_version=version)
            if client is None:
                from openai import AzureOpenAI
                kwargs = dict(api_key=settings.azure_api_key, api_version=version,
                              timeout=timeout, max_retries=0)
                kwargs['base_url' if settings.use_base_url else 'azure_endpoint'] = settings.azure_endpoint
                http = AzureOpenAIBackend._build_http_client(settings.ca_bundle, timeout)
                if http is not None:
                    kwargs['http_client'] = http
                client = AzureOpenAI(**kwargs)
        elif client is None:
            from openai import OpenAI
            key = api_key or os.environ.get('OPENAI_API_KEY')
            if not key:
                raise RuntimeError('OPENAI_API_KEY ausente')
            client = OpenAI(api_key=key, timeout=timeout, max_retries=0)
        self.client = client
        # Opcional: auditoria das saídas, inclusive JSON inválido, sem headers/credenciais.
        self.response_dir = Path(response_dir) if response_dir is not None else None
        self.provider, self.timeout = provider, timeout
        self._api_version = api_version
        self._auto_client = provider == 'azure' and settings is not None and self.client is not None \
            and type(client).__name__ == 'AzureOpenAI'
        self._key_seen = getattr(settings, 'azure_api_key', None)
        self.identity = identity
        self.model, self.effort, self.max_calls = model, effort or '', max_calls
        self.max_attempts, self.max_tokens_cap = max_attempts, max_tokens_cap
        self.sleep = sleep or time.sleep
        self.lock = threading.Lock()
        self.budget = budget
        self.log_lock = log_lock or self.lock
        Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(cache_path), check_same_thread=False, timeout=30)
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('CREATE TABLE IF NOT EXISTS cache (k TEXT PRIMARY KEY, v TEXT)')
        self.db.commit()
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.calls = 0
        self.usage = {'calls': 0, 'cached': 0, 'prompt_tokens': 0, 'completion_tokens': 0, 'errors': 0,
                      'filtro_conteudo': 0, 'reparos': 0}
        self._stage_usage = {}

    @property
    def usage_by_stage(self):
        with self.lock:
            return {tag: dict(counts) for tag, counts in self._stage_usage.items()}

    def _add_usage(self, tag, **counts):
        with self.lock:
            stage = self._stage_usage.setdefault(tag, {**dict.fromkeys(self.usage, 0), 'attempts': 0})
            for key, value in counts.items():
                stage[key] += value
                if key in self.usage:
                    self.usage[key] += value

    # ------------------------------------------------------------------ util
    def close(self):
        self.db.close()
        if hasattr(self.client, 'close'):
            self.client.close()

    def _refresh_credentials(self, failed_key):
        """Relê o .env (token JWT do gateway expira) e recria o cliente. True se a chave mudou."""
        if not self._auto_client:
            return False
        with self.lock:
            if self._key_seen != failed_key:
                return True  # outra thread já renovou
            from azure_openai_backend import AzureSettings, AzureOpenAIBackend
            from openai import AzureOpenAI
            new = AzureSettings.load(override=True)
            if not new.azure_api_key or new.azure_api_key == failed_key:
                return False
            kwargs = dict(api_key=new.azure_api_key, api_version=self._api_version or new.azure_api_version,
                          timeout=self.timeout, max_retries=0)
            kwargs['base_url' if new.use_base_url else 'azure_endpoint'] = new.azure_endpoint
            http = AzureOpenAIBackend._build_http_client(new.ca_bundle, self.timeout)
            if http is not None:
                kwargs['http_client'] = http
            self.client = AzureOpenAI(**kwargs)
            self._key_seen = new.azure_api_key
            return True

    def _get(self, key):
        with self.lock:
            row = self.db.execute('SELECT v FROM cache WHERE k=?', (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def _put(self, key, value):
        with self.lock:
            self.db.execute('INSERT OR REPLACE INTO cache VALUES (?,?)', (key, json.dumps(value, ensure_ascii=False)))
            self.db.commit()

    def _drop(self, key):
        with self.lock:
            self.db.execute('DELETE FROM cache WHERE k=?', (key,))
            self.db.commit()

    def _log(self, row):
        row = {'at': datetime.now(timezone.utc).isoformat(), 'model': self.model,
               'effort': self.effort or 'none', 'provider': self.identity['provider'], **row}
        with self.log_lock:
            with self.log_path.open('a', encoding='utf-8') as f:
                f.write(json.dumps(row, ensure_ascii=False) + '\n')

    def _reserve(self, tag=''):
        with self.lock:
            if self.calls >= self.max_calls:
                raise BudgetExceeded(f'Limite de {self.max_calls} chamadas atingido')
            if self.budget is not None:
                self.budget.reserve()
            self.calls += 1
        self._add_usage(tag, attempts=1)

    # ------------------------------------------------------------------ API
    def json(self, system, user, tag='', max_tokens=16000, validate=None, item=None):
        """Retorna um dict validado. `validate(dict)` levanta ValueError com mensagem útil ao modelo."""
        key = sha(json.dumps([self.identity, self.model, self.effort, max_tokens, system, user], sort_keys=True), 40)
        cached = self._get(key)
        if cached is not None:
            try:
                if validate:
                    validate(cached)
            except ValueError:
                self._drop(key)
            else:
                self._add_usage(tag, cached=1)
                return cached
        tokens = max_tokens
        repair = None          # (conteúdo anterior, erro) para a tentativa de reparo
        last_kind, last_msg = None, None
        refreshed = False
        for attempt in range(self.max_attempts):
            self._reserve(tag)
            started = time.time()
            messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]
            if repair:
                previous, error = repair
                messages += [{'role': 'assistant', 'content': previous[:20000]},
                             {'role': 'user', 'content': 'Sua resposta anterior não passou na validação automática: '
                              f'{error}\nCorrija somente o necessário e devolva o JSON COMPLETO no formato pedido.'}]
            kwargs = dict(model=self.model, max_completion_tokens=tokens, response_format={'type': 'json_object'},
                          messages=messages)
            if self.effort:
                kwargs['reasoning_effort'] = self.effort
            base_log = {'tag': tag, 'item': item, 'attempt': attempt, 'max_tokens': tokens, 'reparo': bool(repair)}
            client = self.client
            used_key = self._key_seen
            try:
                resp = client.chat.completions.create(**kwargs)
            except Exception as exc:  # noqa: BLE001 - classificado abaixo
                msg = _error_body_text(exc)[:800]
                self._add_usage(tag, errors=1)
                if is_content_filter(exc):
                    self._add_usage(tag, filtro_conteudo=1)
                    self._log({**base_log, 'ok': False, 'kind': 'filtro_conteudo', 'error': type(exc).__name__,
                               'message': msg})
                    raise ContentFiltered(f'Filtro de conteúdo ({tag}): {msg[:300]}', tag=tag, item=item) from exc
                if _status(exc) == 401 and not refreshed:
                    refreshed = True
                    if self._refresh_credentials(used_key):
                        self._log({**base_log, 'ok': False, 'kind': 'credencial_renovada',
                                   'error': type(exc).__name__, 'message': msg})
                        continue
                if is_fatal(exc):
                    self._log({**base_log, 'ok': False, 'kind': 'fatal', 'error': type(exc).__name__, 'message': msg})
                    if _status(exc) == 401:
                        raise LLMError('401: a chave/JWT da Azure expirou ou é inválida. Atualize '
                                       'AZURE_OPENAI_API_KEY no .env (e no ambiente, se definida) e rode de novo; '
                                       'o cache retoma de onde parou.', kind='fatal', tag=tag, item=item) from exc
                    raise
                kind = 'transitorio' if is_transient(exc) else 'requisicao'
                self._log({**base_log, 'ok': False, 'kind': kind, 'error': type(exc).__name__, 'message': msg,
                           'seconds': round(time.time() - started, 2)})
                last_kind, last_msg = kind, f'{type(exc).__name__}: {msg[:300]}'
                if kind == 'requisicao' and attempt >= 1:
                    break  # 400 não relacionado a filtro (ex.: contexto longo): repetir não resolve
                if attempt < self.max_attempts - 1:
                    self.sleep(min(90.0, max(retry_after(exc), 2 ** attempt + random.random())))
                continue
            choice = resp.choices[0]
            finish = getattr(choice, 'finish_reason', None)
            content = getattr(choice.message, 'content', None) or ''
            u = getattr(resp, 'usage', None)
            pt = getattr(u, 'prompt_tokens', 0) or 0
            ct = getattr(u, 'completion_tokens', 0) or 0
            self._add_usage(tag, calls=1, prompt_tokens=pt, completion_tokens=ct)
            meta = {**base_log, 'finish': finish, 'prompt_tokens': pt, 'completion_tokens': ct,
                    'seconds': round(time.time() - started, 2)}
            if self.response_dir is not None and finish != 'content_filter':
                stamp = datetime.now(timezone.utc).isoformat()
                response_id = sha(json.dumps([stamp, self.model, meta, content], sort_keys=True), 32)
                atomic_json(self.response_dir / (response_id + '.json'),
                            {'at': stamp, 'model': self.model, 'effort': self.effort,
                             'provider': self.provider, **meta, 'content': content})
                meta['response_file'] = str(self.response_dir / (response_id + '.json'))
            if finish == 'content_filter':
                self._add_usage(tag, filtro_conteudo=1)
                self._log({**meta, 'ok': False, 'kind': 'filtro_conteudo', 'message': 'resposta bloqueada'})
                raise ContentFiltered(f'Filtro de conteúdo na resposta ({tag})', tag=tag, item=item)
            if finish == 'length':
                self._log({**meta, 'ok': False, 'kind': 'truncada', 'message': f'max_tokens={tokens}'})
                last_kind, last_msg = 'truncada', f'resposta truncada com max_tokens={tokens}'
                if tokens >= self.max_tokens_cap:
                    break
                tokens = min(self.max_tokens_cap, int(tokens * 1.6))
                continue
            try:
                data = json.loads(content)
                if not isinstance(data, dict):
                    raise ValueError('a resposta deve ser um objeto JSON')
                if validate:
                    validate(data)
            except ValueError as exc:  # inclui JSONDecodeError
                msg = str(exc)[:600]
                self._log({**meta, 'ok': False, 'kind': 'validacao', 'message': msg})
                self._add_usage(tag, reparos=1)
                last_kind, last_msg = 'validacao', msg
                repair = (content, msg)
                continue
            self._log({**meta, 'ok': True})
            self._put(key, data)
            return data
        raise CallFailed(f'{tag}: falhou após tentativas ({last_kind}): {last_msg}', kind=last_kind or 'falha_chamada',
                         tag=tag, item=item)
