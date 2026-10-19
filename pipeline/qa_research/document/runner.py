"""Pesquisa documental retomável sobre pacote local, sem índice/modelo no servidor."""
import concurrent.futures
import json
import re
import threading
import time
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.llm import BudgetExceeded, LLMClient, LLMError, is_fatal, load_dotenv
from pipeline.inventario.textutil import atomic_json, read_json, sha
from ..runtime import PersistentBudget
from . import VERSION, contracts as C, prompts as P
from .common import Packet, ROOT, canonical


def implementation():
    files = sorted(Path(__file__).parent.glob("*.py")) + [ROOT / p for p in (
        "pipeline/inventario/llm.py", "pipeline/inventario/textutil.py", "pipeline/inventario/locking.py",
        "pipeline/qa_research/runtime.py", "azure_openai_backend.py")]
    return sha("\n".join(p.relative_to(ROOT).as_posix() + "\n" + p.read_text(encoding="utf-8") for p in files), 64)


def new_state(facet):
    return {"id": facet["id"], "round": 0, "read_done": False, "seen": [], "next": [],
            "assessments": [], "findings": [], "quarantine": [], "requests": [], "gap_history": [],
            "versions": [], "active_blocks": [], "reviews": {}, "resolutions": [],
            "discoveries": [], "errors": [], "status": "pendente", "repairs": 0}


class Runner:
    def __init__(self, packet, output, overrides=None, client=None, progress=print, reuse=None):
        self.packet, self.output = packet, Path(output).resolve()
        self.settings = {**packet.profile["runtime"], **(overrides or {})}
        for k in ("workers", "max_calls", "max_attempts", "research_rounds", "batch_sources", "writer_sources", "max_blocks"):
            if type(self.settings[k]) is not int or self.settings[k] < 1:
                raise ValueError("Configuração inteira positiva esperada: " + k)
        self.client, self.progress = client, progress
        self.reuse = reuse
        self.lock = threading.Lock()
        self.api_slots = threading.BoundedSemaphore(self.settings["workers"])
        self.timings = {}
        self.states = {}
        self.stop = threading.Event()
        self.budget = None

    def save(self, state):
        atomic_json(self.output / "recortes" / (state["id"] + ".json"), state)

    def call(self, stage, item, payload, validate, tokens=6000):
        prompt = getattr(P, stage.upper())
        key = sha(canonical([VERSION, self.settings["model"], stage, payload]), 40)
        path = self.output / "chamadas" / (key + ".json")

        def strict(data):
            try:
                validate(data)
            except (KeyError, TypeError, IndexError) as exc:
                raise ValueError("Estrutura inválida: " + str(exc)) from exc

        cached = read_json(path)
        if cached:
            strict(cached["response"])
            return cached["response"]
        if self.stop.is_set():
            raise BudgetExceeded("Execução interrompida; checkpoints preservados")
        started = time.monotonic()
        try:
            # Redatores e auditores de recortes distintos compartilham o mesmo
            # teto global; pools internos não multiplicam a concorrência de API.
            with self.api_slots:
                if self.stop.is_set():
                    raise BudgetExceeded("Execução interrompida; checkpoints preservados")
                response = self.client.json(prompt, canonical(payload), tag="document_" + stage,
                                            item=item, max_tokens=tokens, validate=strict)
            atomic_json(path, {"stage": stage, "item": item, "system": prompt,
                               "request": payload, "response": response})
            return response
        except Exception as exc:
            if isinstance(exc, BudgetExceeded) or is_fatal(exc) or getattr(exc, "kind", None) == "fatal":
                self.stop.set()
            raise
        finally:
            seconds = time.monotonic() - started
            with self.lock:
                values = self.timings.setdefault(stage, {"requests": 0, "seconds": 0.})
                values["requests"] += 1
                values["seconds"] += seconds
                atomic_json(self.output / "progresso.json", {"etapa": stage, "item": item,
                    "tentativas_reservadas": self.budget.used if self.budget else None,
                    "tempos_sessao": self.timings})
            self.progress(f"{stage}: {item} ({seconds:.1f}s)")

    def gap(self, state, value, origin):
        if not isinstance(value, str) or not value.strip() or len(value) > 1800:
            return
        key = "G" + sha(" ".join(value.casefold().split()), 16)
        if not any(g["id"] == key for g in state["gap_history"]):
            state["gap_history"].append({"id": key, "texto": value, "origem": origin})

    def research(self, facet, state):
        unread = [sid for sid in facet["fontes"] if sid not in state["seen"]]
        preferred = [sid for sid in state["next"] if sid in unread]
        batch = list(dict.fromkeys(preferred + unread))[:self.settings["batch_sources"]]
        if not batch:
            state["read_done"] = True
            self.save(state)
            return
        catalog = [{"id": sid, "titulo": self.packet.sources[sid].get("title"),
                    "previa": self.packet.sources[sid]["texto"][:260]}
                   for sid in unread if sid not in batch]
        data = self.call("research", facet["id"], {"topico": self.packet.profile["topic"],
            "recorte": {k: facet[k] for k in ("id", "titulo", "foco")},
            "fontes": self.packet.views(batch), "catalogo": catalog,
            "achados_anteriores": state["findings"][-18:],
            "rodada": state["round"] + 1, "limite_rodadas": self.settings["research_rounds"]},
            lambda d: C.research_core(d, batch))
        # O núcleo já está persistido em chamadas antes de validar itens auxiliares.
        good, bad = C.findings(data, self.packet, batch)
        state["findings"].extend(good)
        state["quarantine"].extend(bad)
        state["assessments"].extend({k: r[k] for k in ("id", "pertinente", "tipo")} for r in data["avaliacoes"])
        state["seen"].extend(batch)
        state["round"] += 1
        next_ids = data.get("proximas_fontes")
        state["next"] = list(dict.fromkeys(s for s in next_ids if isinstance(s, str) and s in unread and s not in batch)) if isinstance(next_ids, list) else []
        requests = data.get("pedidos_busca")
        if isinstance(requests, list):
            state["requests"] = list(dict.fromkeys(state["requests"] + [s for s in requests if isinstance(s, str) and 0 < len(s) <= 1800]))[:30]
        gaps = data.get("lacunas")
        if isinstance(gaps, list):
            for s in gaps[:12]:
                self.gap(state, s, "pesquisa_" + str(state["round"]))
        # Concluir sem achados válidos não encerra prematuramente a procura.
        state["read_done"] = (data["concluir"] and bool(state["findings"])) or state["round"] >= self.settings["research_rounds"] or len(batch) == len(unread)
        state["status"] = "pesquisado" if state["read_done"] else "pesquisando"
        self.save(state)

    def writer_sources(self, facet, state):
        positive = {r["id"] for r in state["assessments"] if r["pertinente"] and r["tipo"] != "opiniao"}
        with_findings = {r["fonte"] for r in state["findings"] if r["tipo"] != "opiniao"}
        size = self.settings["batch_sources"]
        # Reserva espaço para evidências obtidas nas rodadas de aprofundamento.
        # Não deixe as primeiras 12 fontes esconderem tudo o que veio depois.
        batches = [state["seen"][i:i + size] for i in range(0, len(state["seen"]), size)]
        balanced = [batch[i] for i in range(size) for batch in batches if i < len(batch)]
        ids = [s for s in balanced if s in with_findings]
        ids.extend(s for s in balanced if s in positive)
        return list(dict.fromkeys(ids))[:self.settings["writer_sources"]]

    def write(self, facet, state, rejected=None):
        source_ids = self.writer_sources(facet, state)
        # A ausência de uma passagem não impede explicar princípios técnicos.
        # Complementos são declarados no bloco e auditados sem falsa atribuição.
        allowed = {c for s in source_ids for c in self.packet.by_source[s]}
        kept = C.approved(state, self.packet)
        maximum = self.settings["max_blocks"] - len(kept) if rejected is not None else self.settings["max_blocks"]
        if maximum <= 0:
            return
        data = self.call("write", facet["id"], {"topico": self.packet.profile["topic"],
            "recorte": {k: facet[k] for k in ("id", "titulo", "foco")},
            "outros_focos": [f["foco"] for f in self.packet.facets if f["id"] != facet["id"]],
            "fontes": self.packet.views(source_ids),
            "modo": "sintese_tecnica_autonoma_com_complementacao_declarada",
            "achados": [r for r in state["findings"] if r["fonte"] in source_ids],
            "limite_blocos": maximum, "limite_palavras_bloco": self.settings["max_block_words"],
            "blocos_mantidos": [{"id": b["id"], "texto": b["texto"]} for b in kept],
            "revisar": rejected or []},
            lambda d: C.draft(d, allowed, maximum, self.settings["max_block_words"], synthesis=True), tokens=9000)
        version = len(state["versions"]) + 1
        blocks = [{"id": f"{facet['id']}-V{version:02d}-B{i:03d}", **b}
                  for i, b in enumerate(data["blocos"], 1)]
        state["versions"].append({"version": version, "titulo": data["titulo"], "blocks": blocks, "source_ids": source_ids})
        if rejected is None:
            state["active_blocks"] = blocks
        else:
            keep_ids = {b["id"] for b in kept}
            state["active_blocks"] = [b for b in state["active_blocks"] if b["id"] in keep_ids] + blocks
            state["repairs"] += 1
        state["writer_sources"] = source_ids
        state.pop("gaps_done", None)
        state.pop("discovery_done", None)
        for s in data["lacunas"]:
            self.gap(state, s, f"redacao_V{version:02d}")
        self.save(state)

    def audit_one(self, state, block):
        sources = state["writer_sources"]
        allowed = {cid for s in sources for cid in self.packet.by_source[s]}
        core = self.call("audit", block["id"], {"bloco": block, "fontes": self.packet.views(sources)},
                         lambda d: C.audit(d, block, self.packet, allowed), tokens=4000)
        review = {**core, "allowed_citations": sorted(allowed), "seal": C.seal(block, core, self.packet)}
        return block["id"], review

    def finish(self, facet, state):
        if state["status"] == "sem_suporte":
            self.reconcile(facet, state)
            return
        if not state["active_blocks"]:
            self.write(facet, state)
        if state["status"] == "sem_suporte":
            return
        while True:
            pending = [b for b in state["active_blocks"] if b["id"] not in state["reviews"]]
            # Auditorias são independentes. Salve as concluídas mesmo se outra falhar.
            failures = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.settings["workers"]) as pool:
                tasks = {pool.submit(self.audit_one, state, b): b for b in pending}
                for future in concurrent.futures.as_completed(tasks):
                    try:
                        bid, review = future.result()
                        state["reviews"][bid] = review
                        for s in review["lacunas"]:
                            self.gap(state, s, bid)
                        self.save(state)
                    except Exception as exc:
                        failures.append(exc)
            if failures:
                raise failures[0]
            approved_ids = {b["id"] for b in C.approved(state, self.packet)}
            rejected = [{**b, "auditoria": {k: v for k, v in state["reviews"][b["id"]].items()
                        if k not in {"seal", "allowed_citations"}}}
                        for b in state["active_blocks"] if b["id"] not in approved_ids]
            if not rejected or state["repairs"] >= self.settings["audit_repairs"]:
                break
            self.write(facet, state, rejected)
        state["status"] = "auditado" if approved_ids else "sem_blocos_aprovados"
        self.save(state)
        self.reconcile(facet, state)
        # Descoberta opcional tem estado separado e não derruba o capítulo.
        if not state.get("discovery_done") and approved_ids:
            try:
                blocks = C.approved(state, self.packet)
                citations = {c for b in blocks for c in b["trechos"]}
                if not citations:
                    state["discovery_done"] = True
                    self.save(state)
                    return
                data = self.call("discover", facet["id"], {"blocos": blocks,
                    "provas": self.packet.support(sorted(citations)),
                    "recortes": [{k: f[k] for k in ("id", "foco")} for f in self.packet.facets]},
                    lambda d: C.obj(d, {"propostas"}), tokens=2500)
                if not isinstance(data["propostas"], list):
                    raise ValueError("Lista de propostas esperada")
                for row in data["propostas"][:2]:
                    try:
                        C.obj(row, {"relacao", "recorte_destino", "trechos", "consultas"})
                        C.text(row["relacao"])
                        C.refs(row["trechos"], citations)
                        C.strings(row["consultas"], 4)
                        if row["recorte_destino"] not in self.states:
                            raise ValueError("Recorte destino desconhecido")
                        state["discoveries"].append(row)
                    except (ValueError, TypeError, KeyError) as exc:
                        state["quarantine"].append({"etapa": "discover", "item": row, "erro": str(exc)})
            except Exception as exc:
                state["errors"].append({"stage": "discover", "optional": True, "error": str(exc)[:1000]})
                if self.stop.is_set():
                    self.save(state)
                    raise
            state["discovery_done"] = True
            self.save(state)

    def reconcile(self, facet, state):
        if state.get("gaps_done"):
            return
        blocks = C.approved(state, self.packet)
        if not state["gap_history"]:
            state["gaps_done"] = True
        elif not blocks:
            state["resolutions"] = [{"id": g["id"], "estado": "aberta", "parecer": "Não há bloco aprovado que resolva a pendência.", "blocos": [], "trechos": []} for g in state["gap_history"]]
            state["gaps_done"] = True
        else:
            citations = {c for b in blocks for c in b["trechos"]}
            # Lotes limitam custo/contexto mesmo após diversas revisões.
            resolutions = []
            for start in range(0, len(state["gap_history"]), 16):
                batch = state["gap_history"][start:start + 16]
                data = self.call("gaps", facet["id"], {"lacunas": batch, "blocos": blocks,
                    "provas": self.packet.support(sorted(citations))},
                    lambda d: C.gaps(d, {g["id"] for g in batch}, {b["id"]: b for b in blocks}, citations))
                resolutions.extend(data["resolucoes"])
            state["resolutions"] = resolutions
            state["gaps_done"] = True
        self.save(state)

    def execute(self, facet, action):
        state = self.states[facet["id"]]
        try:
            action(facet, state)
            state.pop("pending_error", None)
        except Exception as exc:
            state["pending_error"] = {"stage": action.__name__, "error": str(exc)[:1200]}
            state["errors"].append(state["pending_error"])
            self.progress(f"Pendente {facet['id']}: {type(exc).__name__}: {str(exc)[:250]}")
        self.save(state)

    def map_facets(self, facets, action):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.settings["workers"]) as pool:
            list(pool.map(lambda f: self.execute(f, action), facets))

    def consolidate(self):
        """Deduplicação sem reescrever prosa auditada nem apagar exceções."""
        blocks = [(f, b) for f in self.packet.facets for b in C.approved(self.states[f["id"]], self.packet)]
        signature = sha(canonical([b for _, b in blocks]), 64)
        old = read_json(self.output / "consolidacao.json")
        if old and old.get("signature") == signature and old.get("complete"):
            return old
        pairs, decisions, removed, seen_text = [], [], {}, {}
        for _, block in blocks:
            key = re.sub(r"\s+", " ", block["texto"]).strip()
            if key in seen_text:
                removed[block["id"]] = seen_text[key]
                decisions.append({"a": seen_text[key], "b": block["id"], "equivalentes": True,
                    "mesmas_condicoes": True, "parecer": "Texto integralmente idêntico; retenção determinística."})
            else:
                seen_text[key] = block["id"]
        blocks = [(f, b) for f, b in blocks if b["id"] not in removed]
        for i, (fa, a) in enumerate(blocks):
            sa, words_a = set(a["trechos"]), set(a["texto"].casefold().split())
            for fb, b in blocks[i + 1:]:
                sb, words_b = set(b["trechos"]), set(b["texto"].casefold().split())
                proof_overlap = len(sa & sb) / max(1, min(len(sa), len(sb)))
                lexical_overlap = len(words_a & words_b) / max(1, len(words_a | words_b))
                if proof_overlap >= .7 or (fa["grupo"] == fb["grupo"] and lexical_overlap >= .55):
                    pairs.append((a["id"], b["id"]))
        lookup = {b["id"]: b for _, b in blocks}
        complete = True
        errors = []
        for start in range(0, len(pairs), 8):
            batch = pairs[start:start + 8]
            try:
                data = self.call("dedup", str(start), {"pares": [{"a": lookup[a], "b": lookup[b]} for a, b in batch]},
                                 lambda d: C.duplicates(d, batch), tokens=5000)
                decisions.extend(data["comparacoes"])
            except Exception as exc:
                complete = False
                errors.append(str(exc)[:1000])
                if self.stop.is_set():
                    break
        for d in decisions:
            if d["equivalentes"] and d["mesmas_condicoes"]:
                # Retenção transitiva: o destino sempre termina em um bloco mantido.
                a, b = d["a"], d["b"]
                while a in removed:
                    a = removed[a]
                if a != b:
                    removed[b] = a
        for b in removed:
            while removed[b] in removed:
                removed[b] = removed[removed[b]]
        result = {"signature": signature, "complete": complete, "candidate_pairs": len(pairs),
                  "comparacoes": decisions, "removed": removed, "errors": errors}
        atomic_json(self.output / "consolidacao.json", result)
        return result

    def run(self):
        from .export import export_document
        self.output.mkdir(parents=True, exist_ok=True)
        owned_client = self.client is None
        with output_lock(self.output):
            identity = {"version": VERSION, "implementation": implementation(), "packet": self.packet.signature,
                "runtime": {k: v for k, v in self.settings.items() if k not in {"workers", "max_calls", "timeout"}}}
            prior = read_json(self.output / "identidade.json")
            if prior and prior != identity:
                raise ValueError("Código, pacote ou parâmetros mudaram. Use outra pasta de saída para preservar a execução anterior.")
            atomic_json(self.output / "identidade.json", identity)
            for facet in self.packet.facets:
                self.states[facet["id"]] = read_json(self.output / "recortes" / (facet["id"] + ".json")) or new_state(facet)
            if self.reuse:
                from .reuse import reuse_research
                reuse_research(self.packet, self.reuse, self.output, self.states, self.save)
            self.budget = PersistentBudget(self.output / "orcamento.json", self.settings["max_calls"])
            if owned_client:
                try:
                    load_dotenv(ROOT / "pipeline")
                    model, effort = self.settings["model"].rsplit(":", 1)
                    self.client = LLMClient(model, effort, self.output / ".local" / "llm.sqlite3",
                        self.output / "chamadas_llm.jsonl", provider="azure", budget=self.budget,
                        max_calls=self.settings["max_calls"], max_attempts=self.settings["max_attempts"],
                        timeout=self.settings["timeout"], response_dir=self.output / ".local" / "respostas_brutas")
                except Exception as exc:
                    self.progress("Falha de configuração do backend: " + str(exc)[:1200])
                    return export_document(self.packet, self.output, self.states, {}, self.budget.used,
                        self.timings, interruption="configuração do backend: " + str(exc)[:1200])
                backend = getattr(self.client, "identity", {})
                previous_backend = read_json(self.output / "backend.json")
                if previous_backend and previous_backend != backend:
                    self.client.close()
                    raise ValueError("Endpoint ou versão da API mudou. Use outra pasta de saída.")
                atomic_json(self.output / "backend.json", backend)
            started = time.monotonic()
            interruption = None
            consolidation = read_json(self.output / "consolidacao.json") or {}
            try:
                # A primeira rodada contempla TODOS os focos antes de aprofundar.
                for round_no in range(self.settings["research_rounds"]):
                    targets = [f for f in self.packet.facets if not self.states[f["id"]]["read_done"] and self.states[f["id"]]["round"] <= round_no]
                    self.map_facets(targets, self.research)
                    if self.stop.is_set():
                        break
                if not self.stop.is_set():
                    for attempt in range(self.settings["facet_retry_passes"] + 1):
                        targets = [f for f in self.packet.facets if self.states[f["id"]]["read_done"] and
                                   (not self.states[f["id"]].get("gaps_done") or self.states[f["id"]].get("pending_error") or
                                    (self.states[f["id"]]["status"] == "auditado" and not self.states[f["id"]].get("discovery_done")))]
                        # Redação de recortes distintos também pode avançar em
                        # paralelo. Publicação ocorre entre lotes, sem ler estados
                        # que outra thread esteja modificando naquele instante.
                        for start in range(0, len(targets), self.settings["workers"]):
                            self.map_facets(targets[start:start + self.settings["workers"]], self.finish)
                            export_document(self.packet, self.output, self.states, {}, self.budget.used, self.timings)
                            if self.stop.is_set():
                                break
                        if self.stop.is_set():
                            break
                    if not self.stop.is_set():
                        consolidation = self.consolidate()
                if self.stop.is_set():
                    interruption = "orçamento ou erro fatal; retome após corrigir a causa"
            except KeyboardInterrupt:
                self.stop.set()
                interruption = "interrupção pelo operador"
            finally:
                summary = export_document(self.packet, self.output, self.states, consolidation,
                    self.budget.used, self.timings, interruption=interruption,
                    session_seconds=round(time.monotonic() - started, 3))
                if owned_client:
                    self.client.close()
            return summary


def run(packet_path, output, overrides=None, client=None, progress=print, reuse=None):
    return Runner(Packet(packet_path), output, overrides, client, progress, reuse).run()
