"""Orquestração nova: pesquisa adaptativa → capítulo auditado → alvo → QA curta."""
import copy
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from pipeline.inventario.llm import BudgetExceeded, CallFailed, ContentFiltered
from pipeline.inventario.textutil import atomic_json, norm, read_json, sha
from . import contracts as C, prompts as P
from .gates import checked_chapter, checked_question, checked_units


DOCUMENT_TERMINAL = {"auditado_modelo", "parcial", "sem_suporte"}
QA_TERMINAL = {"aprovada_modelo", "rejeitada", "redundante", "sem_questao"}


def source_record(chunk):
    """Texto original integral; localização desconhecida permanece desconhecida."""
    text = chunk.get("texto", "")
    if not text.strip() or not chunk.get("chunk_id"):
        raise ValueError("Recuperador retornou trecho sem texto ou identidade")
    keep = {k: copy.deepcopy(v) for k, v in chunk.items() if k != "neighbor_chunks"}
    keep.update(id="E" + sha(chunk["chunk_id"] + "\n" + text, 16),
                texto_sha256=sha(text, 64))
    return keep


def facet_key(facet):
    return norm("|".join(facet[k].strip() for k in ("servico", "fenomeno_produto", "decisao")))


def block_approved(review):
    return all(review[key] is True for key in C.DOCUMENT_FLAGS)


def unit_eligible(unit):
    review = unit.get("auditoria", {})
    if not all(review.get(key) is True for key in C.ATOM_FLAGS):
        return False
    if unit["tipo"] in ("opiniao", "hipotese"):
        return False
    if unit["tipo"] == "requisito_normativo" and not (unit["jurisdicao"].strip() and unit["edicao"].strip()):
        return False
    return True


def unit_descriptor(unit):
    return {key: copy.deepcopy(unit[key]) for key in
            ("id", "proposicao", "tipo", "contexto", "condicoes", "alvo")}


class ResearchPipeline:
    def __init__(self, config, index, clients, progress=None):
        self.config, self.index, self.clients = config, index, clients
        self.out = Path(config.output)
        self.progress = progress or (lambda message: None)
        self.event_lock = threading.Lock()

    def event(self, stage, identifier, message):
        row = {"at": datetime.now(timezone.utc).isoformat(), "etapa": stage,
               "id": identifier, "mensagem": message}
        with self.event_lock:
            path = self.out / "eventos.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            self.progress(f"[{stage}] {identifier}: {message}")

    def call(self, role, stage, identifier, payload, validator, max_tokens=10000):
        prompt = getattr(P, stage)
        identity = [role, self.config.models[role], prompt, payload]
        digest = sha(json.dumps(identity, ensure_ascii=False, sort_keys=True), 40)
        path = self.out / "chamadas" / (digest + ".json")
        previous = read_json(path)
        if previous and "resultado" in previous:
            validator(previous["resultado"])
            return copy.deepcopy(previous["resultado"])
        request = {"papel": role, "etapa": stage, "id": identifier,
                   "prompt": prompt, "entrada": payload}
        atomic_json(path, request)
        self.event(stage, identifier, f"Executando {role}")

        def validate(data):
            try:
                if not isinstance(data, dict):
                    raise ValueError("Retorne um objeto JSON")
                validator(data)
            except (KeyError, TypeError, AttributeError, IndexError) as exc:
                raise ValueError(f"Objeto incompatível com o schema: {type(exc).__name__}") from exc

        result = self.clients[role].json(
            prompt, json.dumps(payload, ensure_ascii=False), tag="research_" + stage.lower(),
            item=identifier, max_tokens=max_tokens, validate=validate)
        validate(result)  # Também valida clientes injetados nos testes.
        atomic_json(path, {**request, "resultado": result})
        return copy.deepcopy(result)

    def plan(self):
        path = self.out / "plano.json"
        if path.exists():
            return read_json(path)
        data = self.call("planejador", "PLAN", "topico", {
            "topico": self.config.topic, "limite_recortes": self.config.initial_facets},
            lambda d: C.plan(d, self.config.topic, self.config.initial_facets))
        facets, seen = [], set()
        for facet in data["recortes"]:
            key = facet_key(facet)
            if key in seen:
                continue
            seen.add(key)
            facets.append({**facet, "id": "R" + sha(key, 14), "origem": "planejamento"})
        result = {**data, "recortes": facets, "descobertas_nao_investigadas": [],
                  "observacao": "Mapa de pesquisa limitado ao corpus e ao orçamento; não é exaustividade demonstrada."}
        atomic_json(path, result)
        return result

    def retrieve(self, state, queries):
        queries_seen = {norm(row["consulta"]) for row in state["buscas"]}
        known = {e["texto_sha256"] for e in state["evidencias"]}
        new_chunks = 0
        for query in queries[:self.config.queries_per_round]:
            if norm(query) in queries_seen:
                continue
            queries_seen.add(norm(query))
            excluded = {value for e in state["evidencias"]
                        for value in (e["chunk_id"], e.get("content_hash")) if value}
            chunks = self.index.search(query, limit=self.config.chunks_per_query,
                                       exclude=excluded, neighbors=True)
            trace = {"consulta": query, "retornados": len(chunks), "incluidos": []}
            # Cada vizinho é explicitamente contado no mesmo orçamento de fontes.
            expanded = list(chunks)
            expanded.extend(n for c in chunks for n in c.get("neighbor_chunks", []))
            for chunk in expanded:
                if len(state["evidencias"]) >= self.config.max_evidence:
                    break
                evidence = source_record(chunk)
                if evidence["texto_sha256"] in known:
                    continue
                known.add(evidence["texto_sha256"])
                state["evidencias"].append(evidence)
                trace["incluidos"].append(evidence["id"])
                new_chunks += 1
            state["buscas"].append(trace)
        return new_chunks

    def research_facet(self, facet):
        path = self.out / "recortes" / (facet["id"] + ".json")
        state = read_json(path) or {"id": facet["id"], "recorte": facet, "fase": "pesquisa",
            "status": "em_andamento", "evidencias": [], "buscas": [], "rodadas": 0,
            "analises": [], "versoes": [], "auditorias": [], "lacunas": [], "descobertas": []}
        if state["status"] in DOCUMENT_TERMINAL:
            if state["status"] != "sem_suporte" and not checked_chapter(state):
                raise ValueError(f"Checkpoint de capítulo inválido: {path}; restaure o arquivo ou use nova saída")
            return state
        state.pop("erro", None)

        def save():
            atomic_json(path, state)

        def finish(status):
            state.update(status=status, fase="concluida", validacao_humana="pendente")
            save()
            return state

        save()
        try:
            if state["fase"] == "pesquisa":
                if not state["rodadas"]:
                    self.retrieve(state, facet["consultas"])
                    state["rodadas"] += 1
                    save()
                while True:
                    data = self.call("pesquisador", "RESEARCH", facet["id"], {
                        "topico": self.config.topic, "recorte": facet,
                        "evidencias": state["evidencias"], "buscas_realizadas": state["buscas"],
                        "limite_consultas": self.config.queries_per_round,
                        "rodadas_restantes": max(0, self.config.research_rounds - state["rodadas"])},
                        lambda d: C.research(d, state["evidencias"], self.config.topic,
                                             self.config.queries_per_round))
                    state["analises"].append(data)
                    state["lacunas"].extend(v for v in data["lacunas"] if v not in state["lacunas"])
                    state["descobertas"].extend(data["descobertas"])
                    relevant = {r["evidencia_id"] for r in data["avaliacoes_fontes"] if r["pertinente"]}
                    state["fontes_pertinentes"] = sorted(relevant)
                    state["orientacao"] = data["orientacao"]
                    if data["acao"] == "insuficiente" or not relevant and data["acao"] == "redigir":
                        state["motivo"] = data["orientacao"]
                        return finish("sem_suporte")
                    if data["acao"] == "redigir":
                        break
                    if state["rodadas"] >= self.config.research_rounds or len(state["evidencias"]) >= self.config.max_evidence:
                        state["lacunas"].append("Pesquisa interrompida no limite configurado; persistiam pedidos de busca.")
                        state["limite_pesquisa"] = True
                        break
                    added = self.retrieve(state, data["consultas"])
                    state["rodadas"] += 1
                    save()
                    if not added:
                        state["lacunas"].append("Consultas propostas sem novos trechos neste índice; não prova ausência no domínio.")
                        state["limite_pesquisa"] = True
                        break
                if not state.get("fontes_pertinentes"):
                    return finish("sem_suporte")
                state["fase"] = "redacao"
                save()

            relevant_sources = [e for e in state["evidencias"] if e["id"] in state["fontes_pertinentes"]]
            if state["fase"] == "redacao":
                doc = self.call("redator", "WRITE", facet["id"], {
                    "topico": self.config.topic, "recorte": facet, "evidencias": relevant_sources,
                    "avaliacoes_fontes": state["analises"][-1]["avaliacoes_fontes"],
                    "orientacao": state["orientacao"], "lacunas_pesquisa": state["lacunas"]},
                    lambda d: C.document(d, relevant_sources), 14000)
                state["versoes"].append(self.assign_blocks(doc, facet["id"]))
                state["fase"] = "auditoria"
                save()
            while state["fase"] == "auditoria":
                doc = state["versoes"][-1]
                audit = self.call("auditor", "AUDIT_DOCUMENT", facet["id"], {
                    "topico": self.config.topic, "recorte": facet,
                    "capitulo": doc, "evidencias": relevant_sources},
                    lambda d: C.audit_document(d, doc["blocos"], relevant_sources), 12000)
                # Cada parecer é ligado à versão que realmente avaliou.
                state["auditorias"].append({"versao": len(state["versoes"]), **audit})
                state["lacunas"].extend(x for x in audit["lacunas"] if x not in state["lacunas"])
                accepted = {r["id"] for r in audit["avaliacoes"] if block_approved(r)}
                if len(accepted) == len(doc["blocos"]) or len(state["versoes"]) > self.config.max_repairs:
                    state["capitulo"] = {"titulo": doc["titulo"],
                        "blocos": [b for b in doc["blocos"] if b["id"] in accepted],
                        "lacunas": list(dict.fromkeys(state["lacunas"] + doc["lacunas"]))}
                    state["blocos_reprovados"] = [b["id"] for b in doc["blocos"] if b["id"] not in accepted]
                    state["lacunas"] = state["capitulo"]["lacunas"]
                    if not accepted:
                        return finish("sem_suporte")
                    status = "auditado_modelo" if len(accepted) == len(doc["blocos"]) and not state.get("limite_pesquisa") else "parcial"
                    return finish(status)
                # Falta de suporte pode motivar pesquisa nova, antes da reescrita.
                if (audit["consultas"] and state["rodadas"] < self.config.research_rounds
                        and len(state["evidencias"]) < self.config.max_evidence):
                    added = self.retrieve(state, audit["consultas"])
                    state["rodadas"] += 1
                    if added:
                        feedback = self.call("pesquisador", "RESEARCH", facet["id"] + ":lacuna_auditoria", {
                            "topico": self.config.topic, "recorte": facet,
                            "evidencias": state["evidencias"], "buscas_realizadas": state["buscas"],
                            "limite_consultas": self.config.queries_per_round,
                            "rodadas_restantes": max(0, self.config.research_rounds - state["rodadas"]),
                            "pedido_auditor": audit},
                            lambda d: C.research(d, state["evidencias"], self.config.topic,
                                                 self.config.queries_per_round))
                        state["analises"].append(feedback)
                        state["descobertas"].extend(feedback["descobertas"])
                        state["lacunas"].extend(feedback["lacunas"])
                        pertinent = set(state["fontes_pertinentes"]) | {
                            r["evidencia_id"] for r in feedback["avaliacoes_fontes"] if r["pertinente"]}
                        state["fontes_pertinentes"] = sorted(pertinent)
                        relevant_sources = [e for e in state["evidencias"] if e["id"] in pertinent]
                        if feedback["acao"] == "buscar":
                            state["lacunas"].append(feedback["orientacao"])
                    save()
                revision = self.call("redator", "WRITE", facet["id"] + ":revisao", {
                    "topico": self.config.topic, "recorte": facet, "evidencias": relevant_sources,
                    "capitulo_anterior": doc, "auditoria": audit,
                    "lacunas_pesquisa": state["lacunas"]}, lambda d: C.document(d, relevant_sources), 14000)
                state["versoes"].append(self.assign_blocks(revision, facet["id"]))
                save()
        except (BudgetExceeded, CallFailed, ContentFiltered) as exc:
            state.update(erro=type(exc).__name__, motivo=str(exc), status="pendente_execucao")
            save()
            raise
        raise RuntimeError(f"Fase não reconhecida em {facet['id']}: {state['fase']}")

    @staticmethod
    def assign_blocks(doc, facet_id):
        return {**doc, "blocos": [{**b, "id": f"{facet_id}-B{i:03d}"}
                                   for i, b in enumerate(doc["blocos"], 1)]}

    def research(self):
        plan = self.plan()
        done, interrupted = set(), False
        while True:
            pending = [f for f in plan["recortes"] if f["id"] not in done]
            if not pending:
                break
            batch = pending[:self.config.workers]
            with ThreadPoolExecutor(max_workers=self.config.workers) as pool:
                futures = {pool.submit(self.research_facet, f): f for f in batch}
                results = {}
                for future in as_completed(futures):
                    facet = futures[future]
                    try:
                        results[facet["id"]] = future.result()
                    except BudgetExceeded:
                        interrupted = True
                    except (CallFailed, ContentFiltered) as exc:
                        self.event("falha", facet["id"], str(exc))
            # Ordem de incorporação independe da velocidade dos workers.
            seen = {facet_key(f) for f in plan["recortes"]}
            for facet in batch:
                done.add(facet["id"])
                state = results.get(facet["id"])
                if not state:
                    continue
                for proposal in state["descobertas"]:
                    key = facet_key(proposal)
                    if key in seen:
                        continue
                    seen.add(key)
                    discovery = {**proposal, "id": "R" + sha(key, 14),
                                 "origem": "descoberta_no_corpus", "recorte_pai": facet["id"]}
                    if len(plan["recortes"]) < self.config.max_facets:
                        plan["recortes"].append(discovery)
                    elif not any(f["id"] == discovery["id"] for f in plan["descobertas_nao_investigadas"]):
                        plan["descobertas_nao_investigadas"].append(discovery)
            atomic_json(self.out / "plano.json", plan)
            if interrupted:
                break
        return not interrupted

    def extract_facet(self, state):
        path = self.out / "unidades" / (state["id"] + ".json")
        previous = read_json(path)
        if previous:
            expected = [u for u in previous["unidades"] if unit_eligible(u)]
            if checked_units(previous, state, self.config) != expected:
                raise ValueError(f"Checkpoint de unidades inválido: {path}")
            return previous
        blocks = state.get("capitulo", {}).get("blocos", [])
        if not blocks:
            return {"recorte_id": state["id"], "unidades": [], "motivo": "Nenhum bloco auditado"}
        allowed = {eid for block in blocks for eid in block["fontes"]}
        sources = [e for e in state["evidencias"] if e["id"] in allowed]
        raw = self.call("extrator", "EXTRACT", state["id"], {
            "topico": self.config.topic, "recorte": state["recorte"],
            "capitulo_auditado": state["capitulo"], "evidencias": sources,
            "limite_unidades": self.config.max_atoms_per_facet,
            "limite_palavras": self.config.answer_words},
            lambda d: C.atoms(d, blocks, sources, self.config.max_atoms_per_facet, self.config.answer_words))
        units = [{**u, "id": state["id"] + "-U" + sha(json.dumps(u, sort_keys=True, ensure_ascii=False), 14),
                  "recorte_id": state["id"]} for u in raw["unidades"]]
        if units:
            audit = self.call("auditor", "AUDIT_ATOMS", state["id"], {
                "topico": self.config.topic, "unidades": units, "evidencias": sources},
                lambda d: C.audit_atoms(d, units))
            reviews = {a["id"]: a for a in audit["avaliacoes"]}
            for unit in units:
                unit["auditoria"] = reviews[unit["id"]]
                unit["elegivel_qa"] = unit_eligible(unit)
        result = {"recorte_id": state["id"], "unidades": units, "motivo": raw["motivo"]}
        atomic_json(path, result)
        return result

    def qa_item(self, unit, state, previous):
        path = self.out / "questoes" / (unit["id"] + ".json")
        checkpoint = read_json(path)
        if checkpoint and checkpoint["status"] in QA_TERMINAL:
            if checkpoint["status"] == "aprovada_modelo" and not checked_question(checkpoint, unit, state, self.config):
                raise ValueError(f"Checkpoint de QA inválido: {path}")
            return checkpoint
        row = {"id": unit["id"], "recorte_id": unit["recorte_id"], "unidade": unit,
               "status": "pendente_validacao", "validacao_humana": "pendente"}

        def finish(status, reason):
            row.update(status=status, motivo=reason)
            atomic_json(path, row)
            return row

        try:
            identity = {k: unit[k] for k in ("proposicao", "contexto", "condicoes", "alvo")}
            if any(identity == {k: p["unidade"][k] for k in identity} for p in previous):
                return finish("redundante", "Mesma unidade e alvo já cobertos")
            if previous:
                novelty = self.call("novidade", "NOVELTY", unit["id"], {
                    "candidata": unit_descriptor(unit),
                    "anteriores": [unit_descriptor(r["unidade"]) for r in previous]},
                    lambda d: C.novelty(d, [r["id"] for r in previous]), 5000)
                row["novidade"] = novelty
                if any(c["classe"] == "redundante" for c in novelty["comparacoes"]):
                    return finish("redundante", "Alvo de conhecimento já coberto")
            sources_by_id = {e["id"]: e for e in state["evidencias"]}
            source_ids = {s["evidencia_id"] for s in unit["suporte"]}
            sources = [sources_by_id[eid] for eid in sorted(source_ids)]
            question = self.call("autor_qa", "GENERATE_QA", unit["id"], {
                "topico": self.config.topic, "unidade": unit, "evidencias": sources,
                "limite_palavras": self.config.answer_words},
                lambda d: C.question(d, unit, self.config.answer_words), 4000)
            row["candidata"] = question
            if question["status"] != "ok":
                return finish("sem_questao", question["motivo"])
            if any(norm(p["pergunta"].strip()) == norm(question["pergunta"].strip()) for p in previous):
                return finish("redundante", "Pergunta textual já aprovada anteriormente")
            # A busca independente pode trazer contraevidência além do suporte do autor.
            extra = self.index.search(question["pergunta"], limit=self.config.chunks_per_query)
            independent_sources = {e["id"]: e for e in sources}
            for chunk in extra:
                e = source_record(chunk)
                independent_sources.setdefault(e["id"], e)
            independent_sources = list(independent_sources.values())
            row["evidencias_verificacao"] = independent_sources
            blind_payload = {"pergunta": question["pergunta"], "evidencias": independent_sources,
                             "limite_palavras": self.config.answer_words}
            # Deliberadamente sem unidade, gabarito, variantes, capítulo ou QA anterior.
            blind = self.call("respondente", "ANSWER_BLIND", unit["id"], blind_payload,
                              lambda d: C.blind_answer(d, independent_sources, self.config.answer_words), 5000)
            row["resolucao_independente"] = blind
            audit = self.call("adversario", "AUDIT_QA", unit["id"], {
                "topico": self.config.topic, "questao": question, "unidade_alvo": unit,
                "resolucao_independente": blind, "evidencias": independent_sources,
                "limite_palavras": self.config.answer_words}, C.audit_qa, 7000)
            row["auditoria"] = audit
            passed = (all(audit[key] is True for key in C.QA_FLAGS)
                      and not audit["outras_respostas"] and blind["status"] == "respondida"
                      and not blind["outras_respostas"] and not blind["condicoes_ausentes"])
            if passed:
                row.update(pergunta=question["pergunta"], resposta=question["resposta"],
                           variantes=question["variantes"])
                return finish("aprovada_modelo", audit["parecer"])
            return finish("rejeitada", audit["parecer"])
        except (BudgetExceeded, CallFailed, ContentFiltered) as exc:
            finish("pendente_validacao", str(exc))
            raise

    def generate_qa(self):
        plan = read_json(self.out / "plano.json")
        if not plan:
            raise ValueError("Execute a etapa de pesquisa antes de gerar QA")
        states, queues = {}, {}
        for facet in plan["recortes"]:
            state = read_json(self.out / "recortes" / (facet["id"] + ".json"))
            if not state or state["status"] not in ("auditado_modelo", "parcial"):
                continue
            states[facet["id"]] = state
            pack = self.extract_facet(state)
            queues[facet["id"]] = [u for u in pack["unidades"] if u["elegivel_qa"]]
        # Rodízio entre recortes; não consumir toda a meta no primeiro capítulo.
        order = []
        while any(queues.values()):
            for queue in queues.values():
                if queue:
                    order.append(queue.pop(0))
        approved, attempts = [], 0
        for unit in order:
            if len(approved) >= self.config.target_qa or attempts >= self.config.max_candidates:
                break
            attempts += 1
            try:
                row = self.qa_item(unit, states[unit["recorte_id"]], approved)
            except BudgetExceeded:
                return False
            except (CallFailed, ContentFiltered) as exc:
                self.event("falha_qa", unit["id"], str(exc))
                continue
            if row["status"] == "aprovada_modelo":
                approved.append(row)
            self.event("qa", unit["id"], f"{row['status']}; {len(approved)} aprovadas")
        return True
