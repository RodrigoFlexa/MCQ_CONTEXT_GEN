"""Roteamento explícito por etapa; sem fallback silencioso para outro modelo."""
import threading
from pathlib import Path

from .llm import CallBudget, LLMClient

PROFILE = 'petrobras-nano-low'
NANO = 'gpt-5-4-nano-petrobras'
GPT = 'gpt-5-4-petrobras'
TAGS = ('assuntos', 'assuntos_retry', 'fatos', 'conceitos', 'redator', 'revisor', 'combinacoes')


def resolve(args, default_model):
    """Resolve os valores efetivos antes de criar serviços ou reaproveitar resultados."""
    if args.perfil_modelos == PROFILE:
        if args.llm_provider != 'azure':
            raise ValueError(f'{PROFILE} exige --llm-provider azure')
        if args.llm_model is not None:
            raise ValueError(f'{PROFILE} define os deployments; remova --llm-model')
        if args.effort not in (None, 'low'):
            raise ValueError(f'{PROFILE} exige effort low')
        args.effort = 'low'
        return {tag: {'model': NANO if tag in ('assuntos', 'assuntos_retry', 'fatos') else GPT,
                      'effort': 'low'} for tag in TAGS}
    args.effort = args.effort or 'medium'
    return {tag: {'model': default_model, 'effort': args.effort} for tag in TAGS}


class StageLLM:
    """Uma fachada para as etapas, dois clientes, um orçamento e um log sincronizado."""

    def __init__(self, routes, cache_path, log_path, max_calls, provider='azure', client_factory=LLMClient):
        self.routes = {tag: dict(spec) for tag, spec in routes.items()}
        self.budget = CallBudget(max_calls)
        self.clients = {}
        log_lock = threading.Lock()
        try:
            for spec in routes.values():
                key = (spec['model'], spec['effort'])
                if key not in self.clients:
                    self.clients[key] = client_factory(key[0], None if key[1] == 'none' else key[1],
                        Path(cache_path), Path(log_path), max_calls=max_calls, provider=provider,
                        budget=self.budget, log_lock=log_lock)
        except BaseException:
            self.close()
            raise

    def json(self, system, user, tag='', **kwargs):
        if tag not in self.routes:
            raise ValueError(f'Etapa sem modelo configurado: {tag!r}')
        spec = self.routes[tag]
        return self.clients[(spec['model'], spec['effort'])].json(system, user, tag=tag, **kwargs)

    @property
    def usage(self):
        result = {}
        for client in self.clients.values():
            for key, value in client.usage.items():
                result[key] = result.get(key, 0) + value
        return result

    @property
    def usage_by_stage(self):
        result = {}
        for (model, effort), client in self.clients.items():
            for tag, counts in client.usage_by_stage.items():
                row = result.setdefault(tag, dict.fromkeys(counts, 0))
                for key, value in counts.items():
                    row[key] += value
                row.update(model=model, effort=effort)
        return result

    def close(self):
        clients, self.clients = self.clients, {}
        error = None
        for client in clients.values():
            try:
                client.close()
            except Exception as exc:
                error = error or exc
        if error is not None:
            raise error
