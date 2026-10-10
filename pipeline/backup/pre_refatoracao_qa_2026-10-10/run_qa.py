"""Geração retomável de QA PetroQuest e logging em modo de comparação de métricas."""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "pipeline"))
sys.path.insert(0, str(ROOT / "pipeline" / "fase_3"))

from fase_3.topicos import TOPICOS
from fase_4.metrics import SimilarityModel, all_similarities, entropy, lexical_metrics, metric_decisions
from fase_4.qa_prompt import SYSTEM_PROMPT, build_prompt

DEFAULT_OUT = ROOT / "pipeline" / "fase_4" / "saida_qa"
DIFFICULTIES = ("fácil", "média", "difícil")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def choose(rows, n, rng):
    if not rows:
        return []
    return rng.sample(rows, min(n, len(rows)))


def choose_external(rows, n, rng):
    """Amostra em rodízio de fontes para não concentrar few-shot em um dataset."""
    groups = {}
    for row in rows:
        # O id diferencia ARC-Easy de ARC-Challenge mesmo compartilhando dataset.
        source = str(row.get("id", "unknown")).split(":", 1)[0]
        groups.setdefault(source, []).append(row)
    for group in groups.values():
        rng.shuffle(group)
    result = []
    # Garante referências em português e mais de um exemplo ARC quando disponíveis.
    for source in ("pira_ptbr", "arc_challenge", "arc_easy"):
        if len(result) < n and groups.get(source):
            result.append(groups[source].pop())
    names = list(groups)
    rng.shuffle(names)
    while names and len(result) < n:
        remaining = []
        for name in names:
            if groups[name] and len(result) < n:
                result.append(groups[name].pop())
            if groups[name]:
                remaining.append(name)
        names = remaining
    return result


def load_inputs(args):
    raw_refs = read_jsonl(ROOT / "pipeline/qa_references/data/qa_examples.jsonl")
    refs = []
    seen = set()
    for row in raw_refs:
        key = " ".join(str(row.get("question", "")).casefold().split())
        if key and key not in seen:
            seen.add(key)
            refs.append(row)
    seeds = read_jsonl(ROOT / "pipeline/qa_references/review/sementes_qa_candidatas.jsonl")
    return refs, seeds


def parse_items(response):
    if isinstance(response, dict):
        items = response.get("items", [])
    else:
        items = []
    return [x for x in items if isinstance(x, dict) and str(x.get("question", "")).strip() and str(x.get("answer", "")).strip()]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--deployment", default=os.getenv("AOAI_DEFAULT_DEPLOYMENT", "gpt-5-4-petrobras"))
    p.add_argument("--effort", default="high", choices=["minimal", "low", "medium", "high"])
    p.add_argument("--limit-per-topic", type=int, default=100)
    p.add_argument("--batch-size", type=int, default=5)
    p.add_argument("--max-attempts-per-topic", type=int, default=500)
    p.add_argument("--max-calls", type=int, default=5000)
    p.add_argument("--topics", nargs="*", help="Nomes exatos dos tópicos; padrão: todos")
    p.add_argument("--output", type=Path, default=DEFAULT_OUT)
    p.add_argument("--similarity-threshold", type=float, default=0.50)
    p.add_argument("--observe-only", action="store_true", help="Registra métricas sem rejeitar por similaridade")
    p.add_argument("--no-embeddings", action="store_true", help="Desativa cosine; mantém Jaccard lexical e trigramas")
    p.add_argument("--format-examples", type=int, default=8)
    p.add_argument("--cross-topic-examples", type=int, default=4)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--resume", action="store_true")
    args = p.parse_args()

    from azure_openai_backend import AzureOpenAIBackend
    backend = AzureOpenAIBackend(deployment=args.deployment, reasoning_effort=args.effort,
                                 cache_enabled=False, max_tokens=2500)
    refs, seeds = load_inputs(args)
    if not refs:
        raise SystemExit("Sem exemplos externos. Execute primeiro pipeline/qa_references/download_qa_examples.py")
    chosen_topics = args.topics or list(TOPICOS)
    unknown = set(chosen_topics) - set(TOPICOS)
    if unknown:
        raise SystemExit(f"Tópicos desconhecidos: {', '.join(sorted(unknown))}")
    rng = random.Random(args.seed)
    model = None
    if not args.no_embeddings:
        try:
            model = SimilarityModel()
        except Exception as exc:
            print(f"Aviso: embeddings indisponíveis ({exc}); métricas lexicais continuam.", file=sys.stderr)

    args.output.mkdir(parents=True, exist_ok=True)
    accepted_path = args.output / "questoes_qa.jsonl"
    candidates_path = args.output / "candidatas_metricas.jsonl"
    topic_path = args.output / "resumo_topicos.jsonl"
    accepted = read_jsonl(accepted_path) if args.resume else []
    prior_candidates = read_jsonl(candidates_path) if args.resume else []
    if not args.resume:
        for path in (accepted_path, candidates_path, topic_path, args.output / "metricas_por_rodada.jsonl"):
            path.unlink(missing_ok=True)
    total_calls = 0
    run_meta = {"started_at": datetime.now(timezone.utc).isoformat(), "deployment": args.deployment,
                "effort": args.effort, "similarity_threshold": None if args.observe_only else args.similarity_threshold,
                "candidate_similarity_thresholds": [0.50, 0.70, 0.85], "max_per_topic": args.limit_per_topic}
    (args.output / "run_config.json").write_text(json.dumps(run_meta, ensure_ascii=False, indent=2), encoding="utf-8")

    for topic in chosen_topics:
        subtopics = list(TOPICOS[topic])
        existing_topic = [r for r in accepted if r.get("topic") == topic]
        attempts = 0
        rounds = 0
        subtopic_counts = Counter(r.get("subtopic") for r in existing_topic)
        round_stats = []
        while len(existing_topic) < args.limit_per_topic and attempts < args.max_attempts_per_topic and total_calls < args.max_calls:
            # Alterna subtópicos, para que 100 signifique o total do tópico.
            subtopic = subtopics[rounds % len(subtopics)]
            rounds += 1
            difficulty = DIFFICULTIES[(len(existing_topic) + attempts) % 3]
            try:
                cross = [s for s in seeds if topic.casefold() not in s.get("topic_path", "").casefold()]
                seen_questions = {r.get("question") for r in prior_candidates}
                prior = prior_candidates + [r for r in accepted if r.get("question") not in seen_questions]
                example_rows = choose_external(refs, args.format_examples, rng)
                cross_rows = choose(cross, args.cross_topic_examples, rng)
                used = [str(r.get("concept", "")) for r in existing_topic if r.get("concept")]
                prompt = build_prompt(topic=topic, subtopic=subtopic, difficulty=difficulty,
                                      format_examples=example_rows, cross_topic_examples=cross_rows,
                                      used_concepts=used,
                                      prior_questions=[r.get("question", "") for r in existing_topic[-20:]],
                                      count=args.batch_size)
                result = backend.complete_json(prompt, system=SYSTEM_PROMPT, max_tokens=2500, default={"items": []})
            except Exception as exc:
                append_jsonl(topic_path, {"topic": topic, "subtopic": subtopic, "event": "api_error", "error": str(exc), "round": rounds})
                raise
            total_calls += 1
            attempts += args.batch_size
            batch_rows = []
            for item in parse_items(result):
                question = re.sub(r"\s+", " ", item["question"]).strip()
                answer = re.sub(r"\s+", " ", item["answer"]).strip()
                prior_q = [r["question"] for r in prior]
                sims = all_similarities(question, prior_q, model)
                lex = lexical_metrics(question, prior_q)
                decisions = metric_decisions(sims, args.similarity_threshold)
                reject = False if args.observe_only else decisions["active_cosine_reject"]
                if decisions["exact_reject"]:
                    reject = True
                row = {"question": question, "answer": answer, "topic": topic, "subtopic": subtopic,
                       "difficulty": difficulty, "concept": str(item.get("concept", "")).strip(),
                       "metrics": {**sims, **lex}, "counterfactual_decisions": decisions,
                       "accepted": not reject, "rejection_reason": "exact_duplicate" if decisions["exact_reject"] else ("cosine_threshold" if reject else None),
                       "metric_policy": "observe_only" if args.observe_only else f"cosine>={args.similarity_threshold:.2f}",
                       "source_examples": [x.get("id") for x in example_rows], "cross_topic_seed_ids": [x.get("review_id") for x in cross_rows],
                       "created_at": datetime.now(timezone.utc).isoformat()}
                append_jsonl(candidates_path, row)
                prior_candidates.append(row)
                prior.append(row)
                batch_rows.append(row)
                if not reject and len(existing_topic) < args.limit_per_topic:
                    existing_topic.append(row)
                    accepted.append(row)
                    subtopic_counts[subtopic] += 1
                    append_jsonl(accepted_path, row)
            accepted_concepts = [r.get("concept", "") for r in existing_topic]
            h_now = entropy(accepted_concepts)
            h_prev = round_stats[-1]["entropy_normalized"] if round_stats else 0.0
            round_stats.append({
                "topic": topic, "round": rounds, "subtopic": subtopic, "difficulty": difficulty,
                "accepted_total": len(existing_topic), "accepted_this_round": sum(r["accepted"] for r in batch_rows),
                "generated_this_round": len(batch_rows), "acceptance_rate": round(sum(r["accepted"] for r in batch_rows) / max(1, len(batch_rows)), 4),
                "entropy_normalized": h_now, "entropy_delta": round(h_now - h_prev, 4),
                "unique_concepts": len(set(c for c in accepted_concepts if c)),
                "mean_cosine_this_round": round(sum(r["metrics"]["cosine"] for r in batch_rows if r["metrics"]["cosine"] is not None) / max(1, sum(r["metrics"]["cosine"] is not None for r in batch_rows)), 4) if batch_rows else None,
                "max_cosine_this_round": max((r["metrics"]["cosine"] for r in batch_rows if r["metrics"]["cosine"] is not None), default=None),
                "shadow_reject_rates": {key: round(sum(r["counterfactual_decisions"][key] for r in batch_rows) / max(1, len(batch_rows)), 4) for key in ("cosine_050_reject", "cosine_070_reject", "cosine_085_reject", "lexical_jaccard_050_reject", "char_trigram_050_reject", "combined_or_070_lex050_reject", "combined_and_050_lex050_reject")},
            })
            last3 = round_stats[-3:]
            round_stats[-1]["saturation_would_trigger_diagnostic"] = len(existing_topic) >= 12 and len(last3) == 3 and all(x["entropy_delta"] < 0.01 and x["accepted_this_round"] <= 1 for x in last3)
            append_jsonl(args.output / "metricas_por_rodada.jsonl", round_stats[-1])
            print(f"[{topic} / {subtopic}] rodada={rounds} aceitas={len(existing_topic)}/{args.limit_per_topic} tentativas={attempts}", flush=True)
        stop_reason = "max_accepted" if len(existing_topic) >= args.limit_per_topic else ("max_attempts" if attempts >= args.max_attempts_per_topic else "max_calls")
        summary = {"topic": topic, "accepted": len(existing_topic), "by_subtopic": dict(subtopic_counts),
                   "attempts": attempts, "rounds": rounds, "stop_reason": stop_reason,
                   "concept_entropy": entropy([r.get("concept", "") for r in existing_topic]),
                   "unique_concepts": len(set(r.get("concept", "") for r in existing_topic if r.get("concept"))),
                   "lexical_diversity_mean": round(sum(r["metrics"]["type_token_ratio"] for r in existing_topic) / max(1, len(existing_topic)), 4),
                   "similarity_thresholds_shadow": [0.50, 0.70, 0.85],
                   "saturation_diagnostic_only": True}
        append_jsonl(topic_path, summary)
        print(json.dumps(summary, ensure_ascii=False), flush=True)
        if total_calls >= args.max_calls:
            break

    run_meta["finished_at"] = datetime.now(timezone.utc).isoformat()
    run_meta["api_calls"] = total_calls
    (args.output / "run_config.json").write_text(json.dumps(run_meta, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
