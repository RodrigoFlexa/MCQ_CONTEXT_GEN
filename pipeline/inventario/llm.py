"""Cliente JSON Azure (padrão) ou OpenAI explícito, com cache, limites e retentativas.

Azure usa AzureSettings e a CA corporativa existentes. O modo público exige
escolha explícita; não há fallback entre provedores. Credenciais nunca entram no cache.
"""
import json
import os
import random
import sqlite3
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from .textutil import sha


class BudgetExceeded(RuntimeError):
    pass


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


class LLMClient:
    def __init__(self, model, effort, cache_path, log_path, max_calls=50000, timeout=600, api_key=None,
                 provider='azure', client=None, settings=None):
        if provider not in ('azure', 'openai'):
            raise ValueError('Provider inválido')
        identity = {'provider': provider}
        if provider == 'azure':
            from azure_openai_backend import AzureSettings, AzureOpenAIBackend
            settings = settings or (AzureSettings.load() if client is None else None)
            if settings:
                settings.require()
                identity.update(endpoint_sha=sha(settings.azure_endpoint, 40), api_version=settings.azure_api_version)
            if client is None:
                from openai import AzureOpenAI
                kwargs = dict(api_key=settings.azure_api_key, api_version=settings.azure_api_version,
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
        self.identity = identity
        self.model, self.effort, self.max_calls = model, effort or '', max_calls
        self.lock = threading.Lock()
        Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(cache_path), check_same_thread=False)
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('CREATE TABLE IF NOT EXISTS cache (k TEXT PRIMARY KEY, v TEXT)')
        self.db.commit()
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.calls = 0
        self.usage = {'calls': 0, 'cached': 0, 'prompt_tokens': 0, 'completion_tokens': 0, 'errors': 0}

    def close(self):
        self.db.close()
        if hasattr(self.client, 'close'):
            self.client.close()

    def _get(self, key):
        with self.lock:
            row = self.db.execute('SELECT v FROM cache WHERE k=?', (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def _put(self, key, value):
        with self.lock:
            self.db.execute('INSERT OR REPLACE INTO cache VALUES (?,?)', (key, json.dumps(value, ensure_ascii=False)))
            self.db.commit()

    def _log(self, row):
        with self.lock:
            with self.log_path.open('a', encoding='utf-8') as f:
                f.write(json.dumps(row, ensure_ascii=False) + '\n')

    def json(self, system, user, tag='', max_tokens=16000, validate=None):
        """Retorna um dict. `validate(dict)` pode levantar ValueError para pedir nova tentativa."""
        key = sha(json.dumps([self.identity, self.model, self.effort, max_tokens, system, user], sort_keys=True), 40)
        cached = self._get(key)
        if cached is not None:
            try:
                if validate:
                    validate(cached)
            except ValueError:
                with self.lock:
                    self.db.execute('DELETE FROM cache WHERE k=?', (key,))
                    self.db.commit()
            else:
                with self.lock:
                    self.usage['cached'] += 1
                return cached
        last = None
        for attempt in range(6):
            with self.lock:
                if self.calls >= self.max_calls:
                    raise BudgetExceeded(f'Limite de {self.max_calls} chamadas atingido')
                self.calls += 1
            started = time.time()
            try:
                kwargs = dict(model=self.model, max_completion_tokens=max_tokens,
                              response_format={'type': 'json_object'},
                              messages=[{'role': 'system', 'content': system}, {'role': 'user', 'content': user}])
                if self.effort:
                    kwargs['reasoning_effort'] = self.effort
                resp = self.client.chat.completions.create(**kwargs)
                content = resp.choices[0].message.content or ''
                u = resp.usage
                with self.lock:
                    self.usage['calls'] += 1
                    self.usage['prompt_tokens'] += getattr(u, 'prompt_tokens', 0) or 0
                    self.usage['completion_tokens'] += getattr(u, 'completion_tokens', 0) or 0
                if resp.choices[0].finish_reason != 'stop':
                    raise ValueError('Resposta incompleta: ' + str(resp.choices[0].finish_reason))
                data = json.loads(content)
                if not isinstance(data, dict):
                    raise ValueError('Resposta JSON não é objeto')
                if validate:
                    validate(data)
                self._log({'tag': tag, 'at': datetime.now(timezone.utc).isoformat(), 'ok': True,
                           'seconds': round(time.time() - started, 2),
                           'prompt_tokens': getattr(u, 'prompt_tokens', None),
                           'completion_tokens': getattr(u, 'completion_tokens', None),
                           'finish': resp.choices[0].finish_reason})
                self._put(key, data)
                return data
            except Exception as exc:  # noqa: BLE001 - classificamos abaixo
                last = exc
                name = type(exc).__name__
                with self.lock:
                    self.usage['errors'] += 1
                self._log({'tag': tag, 'at': datetime.now(timezone.utc).isoformat(), 'ok': False,
                           'error': name, 'attempt': attempt})
                from azure_openai_backend import _is_retryable, _retry_after_seconds
                if not isinstance(exc, ValueError) and not _is_retryable(exc):
                    raise
                if attempt < 5:
                    wait = min(60, max(_retry_after_seconds(exc), 2 ** attempt + random.random()))
                    time.sleep(wait)
        raise RuntimeError(f'Falha após 6 tentativas ({tag}): {type(last).__name__}: {last}')
