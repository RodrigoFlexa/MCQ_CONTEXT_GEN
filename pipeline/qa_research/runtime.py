"""Orçamento persistente e cliente já utilizado no projeto, sem lógica legada de QA."""
import threading
from pathlib import Path

from pipeline.inventario.llm import BudgetExceeded, LLMClient, load_dotenv
from pipeline.inventario.textutil import atomic_json, read_json


class PersistentBudget:
    """Reserva antes da chamada; interrupções/reparos não reiniciam a contagem."""
    def __init__(self, path, limit):
        self.path, self.limit = Path(path), limit
        self.used = (read_json(self.path) or {}).get("tentativas_reservadas", 0)
        if type(self.limit) is not int or self.limit < 1:
            raise ValueError("Limite de chamadas deve ser inteiro positivo")
        if type(self.used) is not int or self.used < 0:
            raise ValueError("Contagem persistida de chamadas inválida")
        self.lock = threading.Lock()

    def reserve(self):
        with self.lock:
            if self.used >= self.limit:
                raise BudgetExceeded(f"Orçamento cumulativo atingido: {self.used}/{self.limit}")
            self.used += 1
            atomic_json(self.path, {"tentativas_reservadas": self.used, "limite": self.limit})


def make_clients(config, budget):
    load_dotenv(Path(__file__).resolve().parents[2])
    output = Path(config.output)
    clients = {}
    try:
        for role, spec in config.models.items():
            deployment, effort = spec.rsplit(":", 1)
            clients[role] = LLMClient(
                deployment, effort, output / ".local" / (role + ".sqlite3"),
                output / "chamadas_llm.jsonl", provider=config.provider,
                budget=budget, max_calls=config.max_calls, max_attempts=config.max_attempts,
                timeout=config.timeout, log_lock=threading.Lock(),
                response_dir=output / ".local" / "respostas_brutas" / role)
    except Exception:
        for client in clients.values():
            client.close()
        raise
    # Um único lock é compartilhado para não intercalar linhas no log.
    log_lock = threading.Lock()
    for client in clients.values():
        client.log_lock = log_lock
    return clients
