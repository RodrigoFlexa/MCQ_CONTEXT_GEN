"""Planeja, gera, verifica e, quando necessário, refina um único lote retomável."""
import threading
import time
from pathlib import Path

from pipeline.inventario.llm import LLMClient, load_dotenv
from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json, sha
from ..document.common import ROOT, canonical
from ..runtime import PersistentBudget
from . import VERSION, contracts as C, inputs, prompts, references, resume


def implementation():
    files = sorted(Path(__file__).parent.glob("*.py")) + list(prompts.FILES.values())
    files += [ROOT / p for p in ("pipeline/inventario/llm.py", "pipeline/inventario/textutil.py",
              "pipeline/inventario/locking.py", "pipeline/qa_research/runtime.py", "azure_openai_backend.py",
              "pipeline/qa_research/document/common.py", "pipeline/qa_research/document/program.py")]
    return sha("\n".join(p.relative_to(ROOT).as_posix() + "\n" + p.read_text(encoding="utf-8")
                         for p in files), 64)


class Runner:
    def __init__(self, config, *, clients=None, progress=print):
        self.config, self.output = config, config.output
        self.clients = dict(clients or {})
        self.owned, self.progress = [], progress
        self.log_lock = threading.Lock()
        self.budget = None

    def client(self, role):
        if role not in self.clients:
            load_dotenv(ROOT)
            model, effort = self.config.models[role].rsplit(":", 1)
            client = LLMClient(model, effort,
                self.output / ".local" / (role + ".sqlite3"), self.output / "chamadas_llm.jsonl",
                provider="azure", budget=self.budget, max_calls=self.config.data["max_calls"],
                max_attempts=self.config.data["max_attempts"], timeout=self.config.data["timeout"],
                max_tokens_cap=32000, log_lock=self.log_lock,
                response_dir=self.output / ".local" / "respostas_brutas" / role)
            self.owned.append(client)
            backend = read_json(self.output / "backend.json", {})
            if backend and any(identity != client.identity for identity in backend.values()):
                raise ValueError("Backend Azure mudou; utilize outra pasta de saída")
            backend[role] = client.identity
            atomic_json(self.output / "backend.json", backend)
            self.clients[role] = client
        return self.clients[role]

    def call(self, stage, value, validate, *, round_=0, decode=None):
        role = "verificacao" if stage == "resolucao_cega" else stage
        system, user = prompts.system(stage), canonical(value)
        key = inputs.digest([stage, round_, self.config.models[role], system, user,
                             self.config.data["tokens"][role]])
        path = self.output / "chamadas" / (key + ".json")

        def strict(response):
            try:
                validate(decode(response) if decode else response)
            except (KeyError, TypeError, IndexError, AttributeError) as exc:
                raise ValueError("Estrutura inválida: " + str(exc)) from exc

        cached = read_json(path)
        if cached is not None:
            if cached.get("key") != key or inputs.digest(cached.get("response")) != cached.get("response_sha256"):
                raise ValueError("Checkpoint alterado: " + path.name)
            strict(cached["response"])
            self.progress(f"{stage}: checkpoint reutilizado", flush=True)
            return decode(cached["response"]) if decode else cached["response"]
        self.progress(f"{stage}: {self.config.models[role]} (rodada {round_ + 1})", flush=True)
        response = self.client(role).json(system, user, tag="qa9_" + stage,
            item=self.config.item, max_tokens=self.config.data["tokens"][role], validate=strict)
        strict(response)
        atomic_json(path, {"key": key, "stage": stage, "round": round_,
                           "response": response, "response_sha256": inputs.digest(response)})
        return decode(response) if decode else response

    def run(self):
        selected = inputs.topic(self.config)
        source = inputs.document(self.config, selected)
        identity = {"schema": VERSION, "topic": selected, "contexto_sha256": source["contexto_sha256"],
                    "implementation": implementation(), "models": self.config.models,
                    "tokens": self.config.data["tokens"]}
        with output_lock(self.output):
            previous = read_json(self.output / "identidade.json")
            if previous is not None and not resume.compatible(previous, identity):
                raise ValueError("Tópico, contexto, prompts, código ou modelos mudaram; use outra saída")
            if previous is None and any((self.output / name).exists() for name in ("chamadas", "qa.json", "resumo.json")):
                raise ValueError("Saída contém resultados sem identidade; use outra pasta")
            if previous is not None:
                finished = resume.completed(self.output, identity, self.config.data["max_refinements"])
                if finished is not None:
                    self.progress(f"{self.config.item}: resultado já finalizado ({finished['status']}); preservado.", flush=True)
                    return finished
                resume.checkpoints(self.output)
                if previous != identity:
                    atomic_json(self.output / "migracoes" / (previous["implementation"][:16] + ".json"),
                        {"anterior": previous, "atual": identity,
                         "motivo": "Reparo de referências da auditoria; etapas com a mesma chave são revalidadas e reutilizadas"})
                    self.progress("Retomada compatível: planejamento, geração e resolução com a mesma chave serão reutilizados.", flush=True)
            atomic_json(self.output / "identidade.json", identity)
            atomic_json(self.output / "entrada.json", {"topic": selected, "documento": source})
            self.budget = PersistentBudget(self.output / "orcamento.json", self.config.data["max_calls"])
            started = time.monotonic()
            summary = {"schema": VERSION, "status": "em_execucao", "item": self.config.item,
                       "models": self.config.models, "validacao_humana": "pendente",
                       "contexto_sha256": source["contexto_sha256"], "questoes_publicadas": 0,
                       "ids_pendentes": [], "refinamentos": 0, "motivo": ""}
            atomic_json(self.output / "resumo.json", summary)
            try:
                self.pipeline(selected, source, summary)
            except BaseException as exc:
                summary.update(status="interrompido", motivo=str(exc), erro=type(exc).__name__)
                summary.update(tipo_falha=getattr(exc, "kind", type(exc).__name__),
                               etapa_falha=getattr(exc, "tag", ""))
                raise
            finally:
                summary["tentativas_reservadas"] = self.budget.used
                summary["segundos_sessao"] = round(time.monotonic() - started, 2)
                try:
                    atomic_json(self.output / "resumo.json", summary)
                finally:
                    # Inclui clientes criados antes de uma falha em outro papel.
                    try:
                        for client in self.owned:
                            client.close()
                    finally:
                        self.owned.clear()
            return summary

    def pipeline(self, selected, source, summary):
        base = inputs.payload(selected, source)
        context = source["contexto_tecnico"]
        plan = self.call("planejamento", {**base, "escopo_orientador": selected["escopo_orientador"]},
                         lambda d: C.plan(d, context))
        atomic_json(self.output / "planejamento.json", plan)
        if plan["status"] != "ok":
            summary.update(status="planejamento_insuficiente", motivo=plan["motivo"])
            return
        batch = self.call("geracao", {**base, "plano": plan}, C.questions)
        atomic_json(self.output / "geracao.json", batch)
        if batch["status"] != "ok":
            summary.update(status="geracao_insuficiente", motivo=batch["motivo"])
            return
        for round_ in range(self.config.data["max_refinements"] + 1):
            atomic_json(self.output / "candidatas.json", batch)
            # Nenhum gabarito, alvo ou resposta esperada chega ao resolvedor.
            blind_questions = [{k: q[k] for k in ("id", "pergunta")} for q in batch["questoes"]]
            resolution = self.call("resolucao_cega", {**base, "questoes": blind_questions}, C.blind, round_=round_)
            catalog = references.catalog(context, batch["questoes"])
            atomic_json(self.output / "referencias" / f"rodada_{round_:02}.json", catalog)
            audit_base = {**base, "contexto_tecnico": catalog["contexto"]}
            audit = self.call("verificacao", {**audit_base, "plano": plan, "lote": batch,
                               "trechos_dos_enunciados": catalog["enunciados"],
                               "resolucao_sem_gabarito": resolution},
                              lambda d: C.review(d, context, batch["questoes"]), round_=round_,
                              decode=lambda d: references.decode_review(d, catalog))
            atomic_json(self.output / "revisoes" / f"rodada_{round_:02}.json",
                        {"resolucao_sem_gabarito": resolution, "auditoria": audit})
            bad = C.rejected(audit, resolution)
            summary.update(refinamentos=round_, ids_pendentes=bad)
            if not bad:
                from .export import publish
                publish(self.output, batch)
                summary.update(status="aprovado_modelo", questoes_publicadas=9, motivo="",
                               qa_sha256=inputs.digest(batch))
                self.progress("Lote aprovado pela verificação automática: 9 questões (3/3/3).", flush=True)
                return
            summary.update(status="pendente_revisao", motivo="Itens reprovados na verificação automática")
            if round_ == self.config.data["max_refinements"]:
                return
            repair = self.call("refinamento", {**base, "plano": plan, "lote": batch,
                               "ids_para_corrigir": bad, "resolucao_sem_gabarito": resolution,
                               "auditoria": audit}, lambda d: C.questions(d, bad), round_=round_)
            atomic_json(self.output / "refinamentos" / f"rodada_{round_:02}.json", repair)
            if repair["status"] != "ok":
                summary["motivo"] = repair["motivo"]
                return
            corrected = {q["id"]: q for q in repair["questoes"]}
            batch = {"status": "ok", "motivo": "", "questoes": [corrected.get(q["id"], q) for q in batch["questoes"]]}
            C.questions(batch)
            # A próxima rodada verifica o lote completo, inclusive pistas entre itens.


def run(config, **kwargs):
    return Runner(config, **kwargs).run()
