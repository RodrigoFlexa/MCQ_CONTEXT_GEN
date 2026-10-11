"""Orquestra domínio -> QA -> Scorer/Refiner -> Judge -> persistência e métricas."""
from collections import Counter
import hashlib

from .config import DIFFICULTIES, SCHEMA_VERSION
from .domain import DomainResources, TOPICOS, fingerprint
from .examples import ExamplePool, build_seed_bank, load_external, sample_external
from .metrics import MetricsIndex, metric_decisions, saturation_signals, entropy, tokens
from .prompts_qa import SYSTEM_PROMPT, build_prompt
from . import prompts_qa
from .scoring import normalize_question, score_qa, refine_question, judge_questions
from .storage import (RunStore, BudgetedClient, CallLimitReached, utc_now,
                      atomic_json, write_jsonl)


def build_clients(cfg, store, backends=None):
    if backends is None:
        from azure_openai_backend import AzureOpenAIBackend
        deployments = {"preparation": cfg.preparation_deployment, "generator": cfg.deployment,
                       "refiner": cfg.deployment, "judge": cfg.judge_deployment}
        backends = {role: AzureOpenAIBackend(deployment=name, reasoning_effort=cfg.effort,
                    api_style="reasoning", max_tokens=12000, reasoning_min_tokens=12000, request_timeout=300,
                    cache_enabled=False) for role, name in deployments.items()}
    return {role: BudgetedClient(backends[role], role, store)
            for role in ("preparation", "generator", "refiner", "judge")}


def process_batch(raw_items, context, difficulty, batch_id, quality_examples,
                  external_examples, cfg, store, clients, metrics, requested):
    processed = []
    for position, raw in enumerate(raw_items[:requested]):
        qid = f"{batch_id}-q{position}"
        normalized = normalize_question(raw)
        row = {"schema_version": SCHEMA_VERSION, "id": qid, "origin": "generated_qa_v2",
               "topic": context["topic"], "subtopic": context["subtopic"],
               "requested_difficulty": difficulty, "batch_id": batch_id,
               "doc_id": context["doc_id"], "facet_id": context["facet_id"],
               "facet_title": context.get("facet_title", ""), "focus": context["focus"],
               "source_chunks": context["chunks"], "corpus_signature": context["corpus_signature"],
               "quality_example_ids": [q["id"] for q in quality_examples],
               "format_example_ids": [q.get("id") for q in external_examples],
               "created_at": utc_now(), "original": raw, "refinements": [],
               "accepted": False, "quality_approved": False,
               "cosine_filter_enabled": cfg.enable_cosine_filter}
        if normalized is None:
            row.update(question="", answer="", rejection_reason="invalid_qa_format", scorer=None, judge=None)
            processed.append(row)
            continue
        normalized["id"] = qid
        row["metrics_original"] = metrics.measure(normalized)
        diagnostic = score_qa(normalized, context["chunks"], cfg)
        row["scorer_original"] = diagnostic
        for attempt in range(cfg.max_refinements):
            if not diagnostic["needs_refinement"]:
                break
            refined, changes = refine_question(clients["refiner"], normalized, diagnostic, context)
            if refined is None:
                row["refinements"].append({"attempt": attempt + 1, "unrepairable": True, "changes": changes})
                break
            refined["id"] = qid
            new_diagnostic = score_qa(refined, context["chunks"], cfg)
            row["refinements"].append({"attempt": attempt + 1, "question": refined,
                                       "scorer": new_diagnostic, "changes": changes})
            normalized, diagnostic = refined, new_diagnostic
        row.update(normalized)
        row["scorer"] = diagnostic
        row["refined"] = bool(row["refinements"])
        if diagnostic["needs_refinement"]:
            row["rejection_reason"] = "unresolved_scorer:" + ";".join(diagnostic["reasons"])
        processed.append(row)

    ready = [{key: row[key] for key in ("id", "question", "answer", "concept", "evidence")}
             for row in processed if row.get("scorer") and not row["scorer"]["needs_refinement"]]
    # O Judge só vê a versão final; não recebe notas do gerador ou do Scorer.
    verdicts = judge_questions(clients["judge"], ready, context, cfg)
    for row in processed:
        if not row["question"]:
            store.commit(row)
            continue
        row["metrics"] = metrics.measure(row)
        row["counterfactual_decisions"] = metric_decisions(row["metrics"], cfg.similarity_threshold)
        verdict = verdicts.get(row["id"])
        row["judge"] = verdict
        if verdict is not None:
            row["nota"] = verdict.get("nota")
            row["difficulty"] = verdict.get("difficulty")
            row["quality_approved"] = verdict["approved"]
            row["rejection_reason"] = verdict["reason"]
        approved = row["quality_approved"]
        if approved and cfg.enable_cosine_filter and row["counterfactual_decisions"]["configured_cosine_would_reject"]:
            approved = False
            row["rejection_reason"] = "cosine_filter_explicitly_enabled"
        # Duplicata exata e demais similaridades ficam só nos diagnósticos nesta
        # rodada. Assim não há gate de diversidade escondido no Scorer ou Judge.
        row["accepted"] = approved
        store.commit(row)
        metrics.add_many([row])
    return processed


def record_round(store, cfg, domain, topic, subtopic, number, requested, difficulty,
                 batch_id, rows, before, error=None):
    current = domain.entropy(store.accepted, topic)
    sub_current = domain.entropy(store.accepted, topic, subtopic)
    observed = [r for r in store.records if r.get("question")]
    all_candidates_entropy = domain.entropy(observed, topic)
    accepted_topic = [r for r in store.accepted if r["topic"] == topic]
    previous = [r for r in store.rounds if r["topic"] == topic]
    cosines = [r["metrics"]["cosine"] for r in rows if r.get("metrics") and r["metrics"]["cosine"] is not None]
    measurable = [r for r in rows if r.get("counterfactual_decisions")]
    item = {"topic": topic, "subtopic": subtopic, "round": number, "batch_id": batch_id,
            "requested_difficulty": difficulty, "requested": requested, "generated": len(rows),
            "accepted_this_round": sum(r["accepted"] for r in rows), "accepted_total": len(accepted_topic),
            "acceptance_rate": sum(r["accepted"] for r in rows) / max(1, len(rows)),
            "quality_rejected": sum(not r.get("quality_approved") for r in rows),
            "entropy": current, "entropy_subtopic": sub_current,
            "entropy_all_candidates": all_candidates_entropy,
            "entropy_gain": round(current["value"] - before["value"], 6)
                if current["value"] is not None and before["value"] is not None else None,
            "entropy_reliable": current["reliable"],
            "new_clusters": current["clusters_visited"] - before["clusters_visited"],
            "concept_tag_entropy_secondary": entropy([r.get("concept", "") for r in accepted_topic]),
            "pooled_lexical_entropy_secondary": entropy([w for r in accepted_topic for w in tokens(r["question"])]),
            "mean_cosine": sum(cosines) / len(cosines) if cosines else None,
            "max_cosine": max(cosines) if cosines else None,
            "mean_type_token_ratio": sum(r["metrics"]["type_token_ratio"] for r in measurable) / len(measurable) if measurable else None,
            "shadow_reject_rates": {key: sum(r["counterfactual_decisions"][key] for r in measurable) / len(measurable)
                                    for key in measurable[0]["counterfactual_decisions"]} if measurable else {},
            "cosine_filter_enabled": cfg.enable_cosine_filter,
            "saturation_stop_enabled": cfg.enable_saturation_stop, "error": error, "at": utc_now()}
    item["saturation_diagnostics"] = saturation_signals(previous, item, cfg)
    store.log_round(item)
    return item


def execute(cfg, *, backends=None, domain=None, seeds=None, external=None):
    """Entradas injetáveis permitem verificar o fluxo completo sem chamadas Azure."""
    cfg.validate()
    selected = cfg.topics or list(TOPICOS)
    if set(selected) - set(TOPICOS):
        raise ValueError("Tópicos desconhecidos: " + ", ".join(set(selected) - set(TOPICOS)))
    store = RunStore(cfg)
    summaries = {}
    try:
        with open(prompts_qa.__file__, "rb") as prompt_file:
            prompt_signature = hashlib.sha256(prompt_file.read()).hexdigest()
        if store.meta.get("prompt_signature") and store.meta["prompt_signature"] != prompt_signature:
            raise ValueError("Os prompts mudaram. Use outra saída para manter a comparação reprodutível.")
        store.meta["prompt_signature"] = prompt_signature
        external = load_external(cfg.external_examples) if external is None and not cfg.prepare_only else (external or [])
        seeds = build_seed_bank(cfg) if seeds is None and not cfg.prepare_only else (seeds or [])
        if not cfg.prepare_only:
            signatures = {"seeds": fingerprint(seeds), "external": fingerprint(external)}
            if store.meta.get("example_signatures") and store.meta["example_signatures"] != signatures:
                raise ValueError("Os bancos de exemplos mudaram. Use outra saída para manter a comparação reprodutível.")
            store.meta["example_signatures"] = signatures
            write_jsonl(cfg.output / "external_examples_used.jsonl", external)
        if seeds:
            write_jsonl(cfg.output / "banco_seed_qa.jsonl", seeds)
        clients = build_clients(cfg, store, backends)
        domain = DomainResources(cfg, clients["preparation"]).prepare(selected) if domain is None else domain
        store.meta["corpus_signature"] = domain.signature
        store.meta["domain_required"] = True
        store.meta["quality_roles"] = ["scorer", "refiner", "judge"]
        if cfg.prepare_only:
            store.status("prepared")
            return store
        if not seeds or not external:
            raise ValueError("A geração exige seeds avaliadas e exemplos externos QA")
        metrics = MetricsIndex(domain.emb, [*seeds, *store.records])
        pool = ExamplePool(cfg, seeds, store.accepted)
        store.status("generating")
        consecutive_errors = 0
        for topic in selected:
            covered = domain.covered_subtopics(topic)
            if not covered:
                summaries[topic] = {"topic": topic, "accepted": 0, "stop_reason": "no_domain_evidence"}
                store.event("domain_coverage", summaries[topic])
                continue
            stop_reason = None
            while sum(q["topic"] == topic for q in store.accepted) < cfg.limit_per_topic:
                state = store.state["topics"].get(topic, {"rounds": 0, "requested_candidates": 0})
                remaining_attempts = cfg.max_attempts_per_topic - state["requested_candidates"]
                if remaining_attempts <= 0:
                    stop_reason = "max_attempts"
                    break
                if store.state["api_calls"] >= cfg.max_calls:
                    stop_reason = "max_calls"
                    break
                history = [r for r in store.rounds if r["topic"] == topic]
                if cfg.enable_saturation_stop and history and history[-1]["saturation_diagnostics"]["configured_saturation_would_stop"]:
                    stop_reason = "topic_saturated"
                    break
                accepted_topic = [q for q in store.accepted if q["topic"] == topic]
                requested = min(cfg.batch_size, cfg.limit_per_topic - len(accepted_topic), remaining_attempts)
                subtopic = covered[state["rounds"] % len(covered)]
                difficulty_counts = Counter(r["requested_difficulty"] for r in history)
                difficulty = min(DIFFICULTIES, key=lambda d: difficulty_counts[d])
                number = store.reserve_round(topic, requested)
                tag = hashlib.sha256(topic.encode()).hexdigest()[:12]
                batch_id = f"qa-v2-{tag}-r{number}"
                before = domain.entropy(store.accepted, topic)
                try:
                    cursor = (number - 1) // len(covered)
                    context = domain.materialize(topic, subtopic, cursor)
                    examples = pool.sample_quality(topic, number)
                    formats = sample_external(external, cfg.format_examples, f"{cfg.seed}:{batch_id}")
                    prompt = build_prompt(topic=topic, subtopic=subtopic, scope=context["scope"],
                              focus=context["focus"], document=context["document"], chunks=context["chunks"],
                              difficulty=difficulty, quality_examples=examples, format_examples=formats,
                              previous_questions=[q["question"] for q in accepted_topic],
                              used_concepts=[q.get("concept", "") for q in accepted_topic],
                              count=requested, batch_id=batch_id)
                    result = clients["generator"].complete_json(prompt, system=SYSTEM_PROMPT, max_tokens=12000)
                    items = result.get("items") if isinstance(result, dict) else None
                    if not isinstance(items, list):
                        raise ValueError("O gerador não retornou uma lista items válida")
                    store.event("generated_batch", {"batch_id": batch_id, "doc_id": context["doc_id"],
                                "raw_items": items, "requested": requested})
                    rows = process_batch(items, context, difficulty, batch_id, examples,
                                         formats, cfg, store, clients, metrics, requested)
                    consecutive_errors = 0
                    report = record_round(store, cfg, domain, topic, subtopic, number,
                                          requested, difficulty, batch_id, rows, before)
                except CallLimitReached:
                    stop_reason = "max_calls"
                    store.event("api_budget", {"topic": topic, "batch_id": batch_id})
                    break
                except Exception as exc:
                    consecutive_errors += 1
                    store.event("round_error", {"topic": topic, "batch_id": batch_id,
                                "error_type": type(exc).__name__, "error": str(exc)[:500]})
                    record_round(store, cfg, domain, topic, subtopic, number, requested,
                                 difficulty, batch_id, [], before, error=type(exc).__name__)
                    if consecutive_errors >= cfg.max_consecutive_api_failures:
                        raise RuntimeError("Falhas consecutivas de etapa excederam o limite técnico; checkpoint preservado") from exc
                    continue
                domain.emb.salvar_cache()
                store.status("generating")
                print(f"[{topic} / {subtopic}] rodada={number} geradas={len(rows)} "
                      f"aceitas={report['accepted_total']}/{cfg.limit_per_topic} "
                      f"H={report['entropy']['value']} cosine={report['mean_cosine']}", flush=True)
            accepted_topic = [q for q in store.accepted if q["topic"] == topic]
            summaries[topic] = {"topic": topic, "accepted": len(accepted_topic),
                "stop_reason": stop_reason or "max_accepted", "entropy": domain.entropy(store.accepted, topic),
                "by_subtopic": dict(Counter(q["subtopic"] for q in accepted_topic)),
                "difficulty_by_judge": dict(Counter(q["difficulty"] for q in accepted_topic)),
                "requested_candidates": store.state["topics"].get(topic, {}).get("requested_candidates", 0),
                "uncovered_subtopics": [s for s in TOPICOS[topic] if s not in covered],
                "cosine_filter_enabled": cfg.enable_cosine_filter,
                "saturation_stop_enabled": cfg.enable_saturation_stop}
            atomic_json(cfg.output / "resumo_topicos.json", list(summaries.values()))
            if stop_reason == "max_calls":
                break
        write_jsonl(cfg.output / "resumo_topicos.jsonl", list(summaries.values()))
        write_jsonl(cfg.output / "pares_qa.jsonl", [{"question": q["question"], "answer": q["answer"]} for q in store.accepted])
        write_jsonl(cfg.output / "seeds_especialista_e_geradas.jsonl",
                    [q for q in seeds if q["origin"] == "expert_approved"] + store.accepted)
        domain.emb.salvar_cache()
        store.status("completed" if len(summaries) == len(selected) and all(
            r["accepted"] >= cfg.limit_per_topic for r in summaries.values()) else "finished_with_limits")
        return store
    except Exception:
        store.status("failed")
        raise
