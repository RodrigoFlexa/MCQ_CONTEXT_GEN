"""
azure_openai_backend.py — cliente único e portátil para Azure OpenAI (multi-deployment)
=========================================================================================

Copie este arquivo para qualquer projeto Python e use assim:

    USO RÁPIDO
    ----------
    from azure_openai_backend import AzureOpenAIBackend

    llm = AzureOpenAIBackend(deployment="gpt-5-petrobras")
    resposta = llm.complete("Explique o que é um grafo bipartido em 2 frases.")
    print(resposta)

    # Trocar de modelo é só trocar o parâmetro — as credenciais são as mesmas:
    llm_mini = AzureOpenAIBackend(deployment="gpt-4o-mini-petrobras")
    print(llm_mini.complete("Resuma isto em uma frase: Lorem ipsum dolor sit amet."))

    # JSON estruturado, tolerante a texto com ```json ... ``` ao redor:
    dado = llm.complete_json('Responda em JSON: {"soma": quanto é 2+2?}', default={})

    # Diagnóstico rápido (credenciais + 1 chamada real de teste):
    #   python azure_openai_backend.py gpt-5-petrobras


O QUE PRECISA EXISTIR NO AMBIENTE
-----------------------------------------------------------------------------
1) Pacotes Python:

       pip install openai          # sempre necessário
       pip install httpx           # só se você for usar AOAI_CA_BUNDLE (gateway
                                    # corporativo com certificado próprio)

2) Um arquivo `.env` na raiz do projeto (procurado a partir do diretório atual,
   subindo pastas — igual ao `git`). NUNCA versione esse arquivo: coloque
   `.env` no `.gitignore`. Duas formas de preencher, escolha UMA:

   ---------------------------------------------------------------------
   OPÇÃO A — Azure OpenAI direto (recurso próprio, sem gateway)
   ---------------------------------------------------------------------
       AZURE_OPENAI_ENDPOINT=https://SEU-RECURSO.openai.azure.com/
       AZURE_OPENAI_API_KEY=coloque-sua-chave-aqui
       AZURE_OPENAI_API_VERSION=2024-10-21

   ---------------------------------------------------------------------
   OPÇÃO B — gateway corporativo (ex.: Petrobras): credenciais num .ini
   e certificado próprio (.pem) para validar o TLS
   ---------------------------------------------------------------------
       AOAI_CONFIG_INI=config-v1.x.ini
       AOAI_CONFIG_SECTION=OPENAI
       AOAI_CA_BUNDLE=petrobras-ca-root.pem

       # o .ini (também NUNCA versionado) segue este formato:
       #
       #   [OPENAI]
       #   OPENAI_API_KEY = ...
       #   OPENAI_API_VERSION = 2024-10-21
       #   AZURE_OPENAI_BASE_URL = https://seu-gateway.empresa.com/openai/v1
       #
       # Um endpoint que já contém caminho (.../openai/v1) é detectado como
       # base_url automaticamente. Force com AOAI_USE_BASE_URL=true se a
       # heurística errar.

   Em ambos os casos, opcionalmente defina um deployment padrão (dá pra
   passar por código também, veja "USO RÁPIDO" acima):

       AOAI_DEFAULT_DEPLOYMENT=gpt-5-petrobras

   Rode `python azure_openai_backend.py --print-env-example > .env` para
   gerar esse template pronto para editar.

3) O `.pem` (só na OPÇÃO B, gateway corporativo): é o certificado da CA do
   gateway, necessário para o `httpx` validar o TLS. Peça ao time de
   infra/segurança. Coloque o arquivo na raiz do projeto (ao lado do `.env`)
   ou aponte um caminho absoluto em AOAI_CA_BUNDLE.

4) Nome do *deployment* (não é o nome do modelo!). Exemplos:

       "gpt-5-petrobras"          -> modelo de raciocínio (gpt-5 completo)
       "gpt-4o-mini-petrobras"    -> modelo de chat comum, mais barato/rápido

   Deployments de raciocínio (nome contém "gpt-5", "gpt5", "o1-", "o3-",
   "o4-") são detectados AUTOMATICAMENTE pelo nome e tratados de forma
   diferente: usam `max_completion_tokens` em vez de `max_tokens`, não
   aceitam `temperature` customizada, e reservam um piso de tokens
   (`reasoning_min_tokens`, default 4000) para "pensar" antes de responder —
   sem esse piso a API devolve resposta vazia com finish_reason="length".
   Se o nome do seu deployment não seguir essa convenção, force com
   `AzureOpenAIBackend(..., api_style="reasoning")` ou `api_style="chat"`.

5) Preço/custo por deployment não é algo que este arquivo conhece — isso é
   negociado internamente pela sua organização e não é uma informação
   pública. Se quiser rastrear custo, anote você mesmo os valores por 1K
   tokens de cada deployment (ex. num dicionário no seu projeto) e cruze com
   `llm.usage.prompt_tokens` / `llm.usage.completion_tokens` depois de usar.

Comportamentos que já vêm prontos, para você não ter que redescobrir:
  • cache em disco por hash do pedido (evita pagar duas vezes pelo mesmo
    prompt) — desligue com `cache_enabled=False`;
  • backoff exponencial com jitter em 429/5xx/timeout;
  • parâmetro não suportado pelo endpoint (ex. um gateway que rejeita
    `seed`) é detectado e removido automaticamente, com um retry;
  • resposta vazia nunca é tratada como resposta válida: levanta
    `LLMUnhealthy` já explicando a causa mais provável (na maioria das
    vezes, orçamento de tokens curto demais para um modelo de raciocínio).
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import time
from configparser import ConfigParser, ExtendedInterpolation
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

# ============================================================================
# .env — carregado sem dependências externas
# ============================================================================

_ENV_LINE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$")

#: valores que ainda estão como no template — um run não deve começar assim,
#: senão a primeira chamada falha com um erro de DNS/auth opaco em vez de
#: "você esqueceu de editar o .env"
PLACEHOLDERS = frozenset(
    {
        "https://your-resource.openai.azure.com/",
        "https://your-resource.openai.azure.com",
        "https://seu-recurso.openai.azure.com/",
        "https://seu-recurso.openai.azure.com",
        "your-resource",
        "seu-recurso",
        "changeme",
        "xxx",
        "<your-key>",
        "coloque-sua-chave-aqui",
        "sk-...",
    }
)


def _is_placeholder(value: Optional[str]) -> bool:
    if not value:
        return False
    v = value.strip()
    return (
        v in PLACEHOLDERS
        or "your-resource" in v
        or "seu-recurso" in v
        or v.lower() in {"changeme", "todo"}
    )


def _parse_dotenv(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = _ENV_LINE.match(raw)
        if not m:
            continue
        key, value = m.group(1), m.group(2)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        else:
            value = value.split(" #")[0].rstrip()
        out[key] = value
    return out


def _find_dotenv(start: Optional[Path] = None) -> Path:
    """Procura um `.env` a partir do diretório atual, subindo pastas."""
    here = (start or Path.cwd()).resolve()
    for d in (here, *here.parents):
        candidate = d / ".env"
        if candidate.exists():
            return candidate
    return here / ".env"


def _load_dotenv(path: Optional[Path] = None, override: bool = False) -> dict[str, str]:
    """Carrega `.env` em `os.environ`. Variáveis de ambiente reais vencem, a
    menos que `override=True`."""
    p = path or _find_dotenv()
    if not p.exists():
        return {}
    values = _parse_dotenv(p.read_text(encoding="utf-8"))
    for key, value in values.items():
        if override or key not in os.environ:
            os.environ[key] = value
    return values


# ============================================================================
# Credenciais (Settings)
# ============================================================================


@dataclass
class AzureSettings:
    """Tudo que vem do ambiente/.env — nunca de código versionado."""

    azure_endpoint: Optional[str] = None
    azure_api_key: Optional[str] = field(default=None, repr=False)
    azure_api_version: Optional[str] = None
    default_deployment: Optional[str] = None
    ca_bundle: Optional[str] = None
    use_base_url: bool = False
    dotenv_path: Optional[Path] = None
    dotenv_found: bool = False
    placeholders: tuple[str, ...] = ()
    ini_path: Optional[str] = None

    @classmethod
    def load(cls, dotenv_path: Optional[Path] = None, override: bool = False) -> "AzureSettings":
        p = dotenv_path or _find_dotenv()
        found = bool(_load_dotenv(p, override=override))
        env = os.environ.get

        ini_path, ini = _load_ini(env("AOAI_CONFIG_INI"), env("AOAI_CONFIG_SECTION"), p.parent)

        raw = {
            "azure_endpoint": env("AZURE_OPENAI_ENDPOINT") or ini.get("endpoint"),
            "azure_api_key": env("AZURE_OPENAI_API_KEY") or ini.get("api_key"),
            "azure_api_version": env("AZURE_OPENAI_API_VERSION") or ini.get("api_version"),
            "default_deployment": env("AOAI_DEFAULT_DEPLOYMENT") or None,
        }
        env_names = {
            "azure_endpoint": "AZURE_OPENAI_ENDPOINT",
            "azure_api_key": "AZURE_OPENAI_API_KEY",
            "azure_api_version": "AZURE_OPENAI_API_VERSION",
        }
        # um placeholder é pior que nada: trata como não-definido, mas avisa
        stale = tuple(
            env_names[k] for k, v in raw.items() if k in env_names and _is_placeholder(v)
        )
        for k in list(raw):
            if _is_placeholder(raw[k]):
                raw[k] = None

        ca_raw = env("AOAI_CA_BUNDLE") or ini.get("ca_bundle")
        ca = _resolve_ca_bundle(ca_raw, base=p.parent)
        if ca_raw and not ca:
            raise RuntimeError(
                f"AOAI_CA_BUNDLE aponta para {ca_raw!r}, que não foi encontrado "
                f"(procurei em {p.parent}, no diretório atual e ao lado deste "
                "arquivo). Use um caminho absoluto ou coloque o .pem ao lado do .env."
            )

        endpoint = raw["azure_endpoint"] or ""
        explicit = env("AOAI_USE_BASE_URL")
        use_base_url = (
            explicit.strip().lower() in ("1", "true", "yes", "on")
            if explicit
            else _looks_like_base_url(endpoint)
        )

        return cls(
            **raw,
            ca_bundle=ca,
            use_base_url=use_base_url,
            dotenv_path=p,
            dotenv_found=found,
            placeholders=stale,
            ini_path=ini_path,
        )

    @property
    def ready(self) -> bool:
        return bool(self.azure_endpoint and self.azure_api_key and self.azure_api_version)

    def missing(self) -> list[str]:
        return [
            name
            for name, value in (
                ("AZURE_OPENAI_ENDPOINT", self.azure_endpoint),
                ("AZURE_OPENAI_API_KEY", self.azure_api_key),
                ("AZURE_OPENAI_API_VERSION", self.azure_api_version),
            )
            if not value
        ]

    def explain_missing(self) -> str:
        parts = []
        stale = set(self.placeholders)
        blank = [n for n in self.missing() if n not in stale]
        if blank:
            parts.append("não definidas: " + ", ".join(blank))
        if stale:
            parts.append("ainda com valor de exemplo do template: " + ", ".join(sorted(stale)))
        return "; ".join(parts) or "credenciais incompletas"

    def require(self) -> None:
        if not self.ready:
            raise RuntimeError(
                f"Azure OpenAI não configurado — {self.explain_missing()}.\n"
                f"Edite {self.dotenv_path} (veja o exemplo no topo deste arquivo, "
                "ou rode `python azure_openai_backend.py --print-env-example`) "
                "ou exporte as variáveis de ambiente diretamente."
            )

    def redacted(self) -> dict:
        """Seguro para logar/serializar: segredos viram fingerprints."""

        def mask_key(v: Optional[str]) -> Optional[str]:
            return f"<definida:{hashlib.sha256(v.encode()).hexdigest()[:8]}>" if v else None

        def mask_host(url: Optional[str]) -> Optional[str]:
            m = re.match(r"^(https?://)([^/]+)(.*)$", url or "")
            if not m:
                return url
            host = m.group(2)
            head = host.split(".")[0]
            keep = head[:3] + "***" if len(head) > 3 else "***"
            rest = ".".join(host.split(".")[1:])
            return f"{m.group(1)}{keep}" + (f".{rest}" if rest else "") + m.group(3)

        return {
            "azure_endpoint": mask_host(self.azure_endpoint),
            "azure_api_key": mask_key(self.azure_api_key),
            "azure_api_version": self.azure_api_version,
            "default_deployment": self.default_deployment,
            "ca_bundle": self.ca_bundle,
            "use_base_url": self.use_base_url,
            "dotenv_path": str(self.dotenv_path) if self.dotenv_path else None,
            "dotenv_found": self.dotenv_found,
            "config_ini": self.ini_path,
            "placeholders": list(self.placeholders),
        }


#: chaves procuradas dentro de uma seção do .ini, em ordem de preferência
INI_KEYS = {
    "api_key": ("OPENAI_API_KEY", "AZURE_OPENAI_API_KEY", "API_KEY"),
    "api_version": ("OPENAI_API_VERSION", "AZURE_OPENAI_API_VERSION", "API_VERSION"),
    "endpoint": (
        "AZURE_OPENAI_BASE_URL",
        "AZURE_OPENAI_ENDPOINT",
        "OPENAI_BASE_URL",
        "BASE_URL",
        "ENDPOINT",
    ),
    "ca_bundle": ("CA_BUNDLE", "SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"),
}


def _load_ini(
    path: Optional[str], section: Optional[str], base: Path
) -> tuple[Optional[str], dict[str, str]]:
    """Lê credenciais de um `.ini` (ConfigParser), formato usado por gateways
    corporativos: seção padrão `[OPENAI]`, `ExtendedInterpolation` habilitada."""
    if not path:
        return None, {}
    p = Path(path).expanduser()
    if not p.is_absolute():
        for candidate_base in (base, Path.cwd()):
            if (candidate_base / p).exists():
                p = (candidate_base / p).resolve()
                break
    if not p.exists():
        raise RuntimeError(
            f"AOAI_CONFIG_INI aponta para {path!r}, que não existe "
            f"(resolvido como {p}). Use um caminho absoluto."
        )

    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read(p, encoding="UTF-8")

    candidates = [section] if section else ["OPENAI", "AZURE", "azure", "openai"]
    chosen = next((s for s in candidates if s and parser.has_section(s)), None)
    values = dict(parser[chosen]) if chosen else dict(parser.defaults())
    upper = {k.upper(): v for k, v in values.items()}

    out: dict[str, str] = {}
    for target, names in INI_KEYS.items():
        for name in names:
            if upper.get(name):
                out[target] = upper[name]
                break
    return str(p), out


def _resolve_ca_bundle(name: Optional[str], base: Path) -> Optional[str]:
    """Encontra o .pem sem depender do diretório de onde o script foi chamado."""
    if not name:
        return None
    p = Path(name).expanduser()
    if p.is_absolute():
        return str(p) if p.exists() else None
    for candidate_base in (base, Path.cwd(), Path(__file__).resolve().parent):
        candidate = (candidate_base / p).resolve()
        if candidate.exists():
            return str(candidate)
    return None


def _looks_like_base_url(endpoint: str) -> bool:
    """Uma URL com caminho é um base_url de gateway, não um recurso Azure puro."""
    m = re.match(r"^https?://[^/]+(/.*)?$", endpoint or "")
    if not m:
        return False
    path = (m.group(1) or "").strip("/")
    return bool(path)


# ============================================================================
# Detecção de modelos de raciocínio (gpt-5, o1/o3/o4-mini...)
# ============================================================================

#: fragmentos do NOME DO DEPLOYMENT que indicam um modelo de raciocínio —
#: por isso um sufixo tipo "-petrobras" não atrapalha a detecção
REASONING_MARKERS = ("gpt-5", "gpt5", "o1-", "o3-", "o4-", "-o1", "-o3", "-o4")

#: parâmetros que enviamos otimisticamente e removemos se o endpoint rejeitar
OPTIONAL_PARAMS = (
    "seed",
    "temperature",
    "frequency_penalty",
    "presence_penalty",
    "response_format",
    "max_tokens",
    "max_completion_tokens",
    "reasoning_effort",
)


def is_reasoning_deployment(name: str) -> bool:
    n = (name or "").lower()
    return any(m in n for m in REASONING_MARKERS)


class LLMError(RuntimeError):
    pass


class LLMUnhealthy(LLMError):
    """O backend respondeu, mas sem nada usável. Falha rápido, não finge."""


@dataclass
class Usage:
    """Contagem de tokens/chamadas — inspecione via `backend.usage`."""

    calls: int = 0
    cached_calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    empty_responses: int = 0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


# ============================================================================
# Backend principal
# ============================================================================


class AzureOpenAIBackend:
    """Cliente único para qualquer deployment Azure OpenAI da sua organização.

    Parameters
    ----------
    deployment:
        Nome do *deployment* (ex.: ``"gpt-5-petrobras"``). Se omitido, usa
        ``AOAI_DEFAULT_DEPLOYMENT`` do ``.env``.
    temperature, max_tokens, seed:
        Defaults por chamada (podem ser sobrescritos em ``.complete(...)``).
    api_style:
        ``"auto"`` (default, detecta pelo nome do deployment) | ``"chat"`` |
        ``"reasoning"``.
    reasoning_min_tokens:
        Piso de tokens reservado para modelos de raciocínio "pensarem" antes
        de responder. ``0`` omite o piso por completo.
    reasoning_effort:
        ``"minimal" | "low" | "medium" | "high" | ""`` — só se aplica a
        deployments de raciocínio.
    cache_enabled, cache_dir:
        Cache em disco por hash do pedido (evita pagar duas vezes pelo mesmo
        prompt). ``cache_dir`` é relativo ao diretório de trabalho atual.
    fail_on_empty:
        Levanta ``LLMUnhealthy`` na primeira resposta vazia (ou numa taxa
        sustentada de respostas vazias) em vez de deixar passar em silêncio.
    """

    def __init__(
        self,
        deployment: Optional[str] = None,
        *,
        temperature: float = 0.0,
        max_tokens: int = 512,
        seed: Optional[int] = 1234,
        request_timeout: float = 60.0,
        max_retries: int = 6,
        backoff_base: float = 2.0,
        backoff_max: float = 60.0,
        api_style: str = "auto",
        reasoning_min_tokens: int = 4000,
        reasoning_effort: str = "low",
        send_temperature: bool = True,
        cache_enabled: bool = True,
        cache_dir: str = ".cache/azure_openai_backend",
        fail_on_empty: bool = True,
        health_check_calls: int = 5,
        max_empty_rate: float = 0.2,
        settings: Optional[AzureSettings] = None,
    ) -> None:
        try:
            from openai import AzureOpenAI
        except ImportError as exc:  # pragma: no cover
            raise LLMError(
                "o pacote 'openai' (>=1.x) é necessário: pip install openai"
            ) from exc

        self.settings = settings or AzureSettings.load()
        self.settings.require()

        if deployment is None:
            deployment = self.settings.default_deployment
        if not deployment:
            raise LLMError(
                "nenhum deployment informado — passe "
                "AzureOpenAIBackend(deployment='gpt-5-petrobras') ou defina "
                "AOAI_DEFAULT_DEPLOYMENT no .env"
            )
        self.deployment = deployment

        self.temperature = temperature
        self.max_tokens = max_tokens
        self.seed = seed
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.backoff_max = backoff_max
        self.reasoning_min_tokens = reasoning_min_tokens
        self.reasoning_effort = reasoning_effort
        self.send_temperature = send_temperature
        self.fail_on_empty = fail_on_empty
        self.health_check_calls = health_check_calls
        self.max_empty_rate = max_empty_rate

        self.reasoning = (
            is_reasoning_deployment(deployment)
            if api_style == "auto"
            else api_style == "reasoning"
        )

        http_client = self._build_http_client(self.settings.ca_bundle, request_timeout)
        kwargs: dict[str, Any] = dict(
            api_key=self.settings.azure_api_key,
            api_version=self.settings.azure_api_version,
        )
        if http_client is not None:
            kwargs["http_client"] = http_client

        # Uma URL de gateway já contém o caminho de roteamento, então precisa
        # ir como base_url; um host de recurso puro é azure_endpoint.
        endpoint = self.settings.azure_endpoint or ""
        if self.settings.use_base_url:
            kwargs["base_url"] = endpoint
        else:
            kwargs["azure_endpoint"] = endpoint
        self._client = AzureOpenAI(**kwargs)

        #: parâmetros que este endpoint já rejeitou uma vez
        self._unsupported: set[str] = set()
        self.last_finish_reason: Optional[str] = None
        self.last_reasoning_tokens: int = 0
        self.last_raw: dict = {}
        self.usage = Usage()

        self.cache_enabled = cache_enabled
        self._cache_dir = Path(cache_dir)
        if cache_enabled:
            self._cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _build_http_client(ca_bundle: Optional[str], timeout: float):
        if not ca_bundle:
            return None
        try:
            import httpx
        except ImportError as exc:  # pragma: no cover
            raise LLMError("AOAI_CA_BUNDLE exige httpx: pip install httpx") from exc
        return httpx.Client(verify=ca_bundle, timeout=timeout)

    # ---------------------------------------------------------- API pública --

    def complete(
        self,
        prompt: str,
        *,
        system: Optional[str] = None,
        json_mode: bool = False,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """Retorna o texto da resposta do modelo (com cache em disco)."""
        temperature = self.temperature if temperature is None else temperature
        max_tokens = self.max_tokens if max_tokens is None else max_tokens

        key = self._cache_key(prompt, system, json_mode, max_tokens, temperature)
        cached = self._cache_read(key)
        if cached is not None:
            self.usage.calls += 1
            self.usage.cached_calls += 1
            self.usage.prompt_tokens += cached.get("prompt_tokens", 0)
            self.usage.completion_tokens += cached.get("completion_tokens", 0)
            return cached["text"]

        text, ptok, ctok = self._call(prompt, system, json_mode, max_tokens, temperature)
        empty = not (text or "").strip()
        self.usage.calls += 1
        self.usage.prompt_tokens += ptok
        self.usage.completion_tokens += ctok
        if empty:
            self.usage.empty_responses += 1
        self.last_raw = {
            "text": text,
            "prompt_tokens": ptok,
            "completion_tokens": ctok,
            "prompt_head": prompt[:300],
        }

        if empty:
            self._on_empty(ptok, ctok, max_tokens)
        else:
            self._cache_write(
                key, {"text": text, "prompt_tokens": ptok, "completion_tokens": ctok}
            )
        return text

    def complete_json(
        self,
        prompt: str,
        *,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        default: Any = None,
    ) -> Any:
        """``.complete(...)`` em modo JSON, tolerante a texto com ```json ... ```
        ao redor ou com prosa antes/depois do objeto."""
        raw = self.complete(prompt, system=system, json_mode=True, max_tokens=max_tokens)
        try:
            return parse_json_loose(raw)
        except ValueError:
            if default is not None:
                return default
            raise

    def doctor(self) -> None:
        """Diagnóstico rápido: mostra a configuração (segredos mascarados) e
        faz uma chamada de teste real."""
        print("Configuração (segredos mascarados):")
        for k, v in self.settings.redacted().items():
            print(f"  {k}: {v}")
        print(f"  deployment: {self.deployment} (reasoning={self.reasoning})")
        print("Fazendo uma chamada de teste...")
        tokens = max(self.max_tokens, self.reasoning_min_tokens) if self.reasoning else self.max_tokens
        resposta = self.complete("Responda apenas com a palavra: ok", max_tokens=tokens)
        print(f"  resposta: {resposta!r}")
        print("OK." if resposta.strip() else "FALHOU: resposta vazia.")

    # -------------------------------------------------------------- params --

    def _budget(self, max_tokens: int) -> int:
        """Teto de tokens a pedir. Modelos de raciocínio precisam de espaço
        para pensar antes."""
        if not self.reasoning:
            return max_tokens
        if self.reasoning_min_tokens <= 0:
            return 0  # omite o teto por completo
        return max(max_tokens, self.reasoning_min_tokens)

    def _build_kwargs(self, messages, json_mode, max_tokens, temperature) -> dict:
        kwargs: dict[str, Any] = {"model": self.deployment, "messages": messages}

        budget = self._budget(max_tokens)
        if budget > 0:
            key = "max_completion_tokens" if self.reasoning else "max_tokens"
            kwargs[key] = budget

        # Deployments de raciocínio só aceitam a temperatura padrão.
        if not self.reasoning and self.send_temperature:
            kwargs["temperature"] = temperature
        if self.seed is not None and not self.reasoning:
            kwargs["seed"] = self.seed
        if self.reasoning and self.reasoning_effort:
            kwargs["reasoning_effort"] = self.reasoning_effort
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        return {k: v for k, v in kwargs.items() if k not in self._unsupported}

    # ---------------------------------------------------------------- call --

    def _call(self, prompt, system, json_mode, max_tokens, temperature):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries):
            kwargs = self._build_kwargs(messages, json_mode, max_tokens, temperature)
            try:
                resp = self._client.chat.completions.create(**kwargs)
                choice = resp.choices[0]
                text = (choice.message.content or "").strip()
                usage = getattr(resp, "usage", None)
                self.last_finish_reason = getattr(choice, "finish_reason", None)
                details = getattr(usage, "completion_tokens_details", None)
                self.last_reasoning_tokens = getattr(details, "reasoning_tokens", 0) or 0
                return (
                    text,
                    getattr(usage, "prompt_tokens", 0) or 0,
                    getattr(usage, "completion_tokens", 0) or 0,
                )
            except Exception as exc:  # noqa: BLE001 - classificado abaixo
                last_exc = exc
                if self._maybe_drop_parameter(exc, kwargs):
                    continue  # tenta de novo sem o parâmetro rejeitado
                if not _is_retryable(exc) or attempt == self.max_retries - 1:
                    break
                delay = min(self.backoff_max, self.backoff_base**attempt) * (
                    0.5 + random.random()
                )
                time.sleep(max(delay, _retry_after_seconds(exc)))

        raise LLMError(
            f"chamada ao Azure falhou (deployment={self.deployment!r}, "
            f"reasoning={self.reasoning}): {last_exc}"
        ) from last_exc

    def _maybe_drop_parameter(self, exc: Exception, kwargs: dict) -> bool:
        """Aprende quais parâmetros opcionais este endpoint rejeita, e para
        de enviá-los."""
        status = getattr(exc, "status_code", None) or getattr(exc, "status", None)
        if status not in (400, 422):
            return False
        message = str(exc)
        for name in OPTIONAL_PARAMS:
            if name in self._unsupported or name not in kwargs:
                continue
            if re.search(rf"\b{re.escape(name)}\b", message):
                self._unsupported.add(name)
                return True
        return False

    def _on_empty(self, ptok: int, ctok: int, max_tokens: int) -> None:
        """Uma resposta vazia nunca é uma resposta válida — decide se aborta.

        Tratar isso silenciosamente como abstenção é o que transforma um
        backend quebrado numa tabela de resultados cheia e plausível, com
        tudo errado. Por isso a primeira resposta vazia já aborta o run (e
        também uma taxa sustentada de respostas vazias)."""
        if not self.fail_on_empty:
            return
        live = self.usage.calls - self.usage.cached_calls
        first = live <= 1
        sustained = (
            live >= self.health_check_calls
            and self.usage.empty_responses / live > self.max_empty_rate
        )
        if not (first or sustained):
            return

        finish = self.last_finish_reason
        reasoning_tok = self.last_reasoning_tokens
        if finish == "length" or (reasoning_tok and reasoning_tok >= ctok > 0):
            cause = (
                f"\n[CAUSA MAIS PROVÁVEL] finish_reason={finish!r}"
                + (f", reasoning_tokens={reasoning_tok}" if reasoning_tok else "")
                + f", orçamento pedido={max_tokens}.\n"
                "Comportamento clássico de modelo de *raciocínio* (o1/o3/o4-mini, "
                "família gpt-5): max_completion_tokens é um orçamento\n"
                "COMPARTILHADO entre os tokens de raciocínio internos e a resposta "
                "visível. Se ele acaba durante o raciocínio, a API\n"
                'devolve content="".\n'
                "Correção: aumente max_tokens na chamada (`.complete(..., "
                "max_tokens=3000)`), ou aumente reasoning_min_tokens no\n"
                "construtor, ou aponte para um deployment sem raciocínio "
                "(ex.: gpt-4o-mini)."
            )
        else:
            cause = (
                "\nCausas comuns:\n"
                "  • orçamento de tokens curto demais para um modelo de raciocínio\n"
                "    (finish_reason='length' → aumente max_tokens)\n"
                "  • nome de deployment errado\n"
                "  • filtro de conteúdo do Azure devolvendo content=None\n"
                "  • gateway/proxy corporativo engolindo o corpo da resposta"
            )

        raise LLMUnhealthy(
            "O backend devolveu uma resposta VAZIA "
            f"({self.usage.empty_responses}/{live} chamadas até agora), "
            f"deployment={self.deployment!r}, prompt_tokens={ptok}, "
            f"completion_tokens={ctok}, finish_reason={finish!r}."
            + cause
            + "\n\nPara tolerar respostas vazias mesmo assim (não recomendado): "
            "AzureOpenAIBackend(..., fail_on_empty=False)"
        )

    # -- cache -------------------------------------------------------------

    def _cache_key(self, prompt, system, json_mode, max_tokens, temperature) -> str:
        payload = "\x1f".join(
            [
                self.deployment,
                f"{temperature:.4f}",
                str(max_tokens),
                str(self.seed),
                str(bool(json_mode)),
                system or "",
                prompt,
            ]
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _cache_path(self, key: str) -> Path:
        return self._cache_dir / key[:2] / f"{key}.json"

    def _cache_read(self, key: str) -> Optional[dict]:
        if not self.cache_enabled:
            return None
        p = self._cache_path(key)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None

    def _cache_write(self, key: str, payload: dict) -> None:
        if not self.cache_enabled:
            return
        p = self._cache_path(key)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        tmp.replace(p)


def _is_retryable(exc: Exception) -> bool:
    status = getattr(exc, "status_code", None) or getattr(exc, "status", None)
    if status in (408, 409, 429, 500, 502, 503, 504):
        return True
    name = type(exc).__name__
    return any(
        tok in name
        for tok in ("RateLimit", "Timeout", "APIConnection", "InternalServer", "ServiceUnavailable")
    )


def _retry_after_seconds(exc: Exception) -> float:
    headers = getattr(getattr(exc, "response", None), "headers", None) or {}
    for key in ("retry-after-ms", "Retry-After-Ms"):
        if key in headers:
            try:
                return float(headers[key]) / 1000.0
            except (TypeError, ValueError):
                pass
    for key in ("retry-after", "Retry-After"):
        if key in headers:
            try:
                return float(headers[key])
            except (TypeError, ValueError):
                pass
    return 0.0


# ============================================================================
# JSON tolerante (para complete_json)
# ============================================================================

_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def parse_json_loose(text: str) -> Any:
    """Parseia JSON que pode vir cercado por ```json ... ```, com prefixo ou
    prosa depois."""
    cleaned = _FENCE.sub("", text).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    for opener, closer in (("{", "}"), ("[", "]")):
        start = cleaned.find(opener)
        end = cleaned.rfind(closer)
        if start != -1 and end > start:
            try:
                return json.loads(cleaned[start : end + 1])
            except json.JSONDecodeError:
                continue
    raise ValueError(f"não consegui parsear JSON da saída do modelo: {text[:300]!r}")


# ============================================================================
# Template de .env — imprima com --print-env-example
# ============================================================================

ENV_EXAMPLE = """\
# ---------------------------------------------------------------------------
# azure_openai_backend — configuração de runtime
#
#   cp .env.example .env      e preencha os valores abaixo.
#   .env é gitignored; .env.example (se você criar um) nunca contém segredo.
# ---------------------------------------------------------------------------

# ===========================================================================
# OPÇÃO A — Azure OpenAI direto
# ===========================================================================
AZURE_OPENAI_ENDPOINT=https://SEU-RECURSO.openai.azure.com/
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_API_VERSION=2024-10-21

# ===========================================================================
# OPÇÃO B — gateway corporativo (credenciais num .ini, CA própria)
#
# Comente o bloco A acima e descomente estas linhas. O .ini é lido com
# ConfigParser + ExtendedInterpolation; a seção padrão é [OPENAI].
# ===========================================================================
# AOAI_CONFIG_INI=config-v1.x.ini
# AOAI_CONFIG_SECTION=OPENAI
# AOAI_CA_BUNDLE=petrobras-ca-root.pem

# Um endpoint que já contém caminho (…/openai/v1) é detectado como base_url
# automaticamente. Force com esta variável se a heurística errar.
# AOAI_USE_BASE_URL=true

# ===========================================================================
# Deployment padrão (opcional — também dá pra passar por código)
# ===========================================================================
# AOAI_DEFAULT_DEPLOYMENT=gpt-5-petrobras
"""


if __name__ == "__main__":
    import sys

    if "--print-env-example" in sys.argv:
        print(ENV_EXAMPLE, end="")
    else:
        deployment = next((a for a in sys.argv[1:] if not a.startswith("-")), None)
        AzureOpenAIBackend(deployment=deployment).doctor()
