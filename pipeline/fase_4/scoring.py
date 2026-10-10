"""Scorer QA determinístico, refinamento limitado e avaliação técnica do Judge."""
import math
import re

from pipeline.qa_references.download_qa_examples import CHOICE_REFERENCES, CONTEXT_REFERENCES
from .prompts_qa import refinement_prompt, judge_prompt

WEIGHTS = {"technical_correctness": 0.40, "clarity": 0.20,
           "answer_completeness": 0.20, "domain_relevance": 0.20}
BOOLEANS = ("technical_ok", "supported_by_sources", "scope_ok", "self_contained")


def collapse(text):
    return " ".join(text.split())


def normalize_question(raw):
    if not isinstance(raw, dict):
        return None
    if any(not isinstance(raw.get(key), str) or not raw[key].strip() for key in ("question", "answer")):
        return None
    evidence = raw.get("evidence", [])
    return {"question": collapse(raw["question"]), "answer": collapse(raw["answer"]),
            "concept": collapse(raw.get("concept", "")) if isinstance(raw.get("concept", ""), str) else "",
            "evidence": [{"chunk_id": x.get("chunk_id", ""), "quote": collapse(x.get("quote", ""))}
                         for x in evidence if isinstance(x, dict) and isinstance(x.get("quote"), str)
                         and isinstance(x.get("chunk_id"), str)] if isinstance(evidence, list) else []}


def score_qa(question, chunks, cfg):
    """O Scorer diagnostica forma e rastreabilidade; não usa similaridade como gate."""
    reasons = []
    q, a = question["question"], question["answer"]
    if CHOICE_REFERENCES.search(q + " " + a):
        reasons.append("references_answer_options")
    if CONTEXT_REFERENCES.search(q + " " + a) or re.search(r"texto acima|conforme o documento|segundo o texto|no trecho", q + " " + a, re.I):
        reasons.append("depends_on_external_passage")
    if re.fullmatch(r"[A-E][).:]?", a, re.I):
        reasons.append("answer_is_option_label")
    if "<NUMBER>" in q + a or re.search(r"\{(?:question|answer)\}|\[insira", q + a, re.I):
        reasons.append("unresolved_placeholder")
    if len(q.split()) > cfg.max_question_words:
        reasons.append("question_unnecessarily_long")
    if len(a.split()) > cfg.max_answer_words:
        reasons.append("answer_unnecessarily_long")
    acronyms = re.findall(r"\b[A-Z][A-Z0-9/-]{2,}\b", q)
    if len(set(acronyms)) > 6:
        reasons.append("excess_acronyms")
    lookup = {x["chunk_id"]: collapse(x["texto"]) for x in chunks}
    evidence = question.get("evidence", [])
    valid = []
    if not evidence:
        reasons.append("missing_source_evidence")
    for item in evidence:
        cid, quote = item.get("chunk_id"), item.get("quote", "")
        verified = cid in lookup and len(quote.split()) >= 4 and quote in lookup[cid]
        valid.append({"chunk_id": cid, "quote": quote, "literal_verified": verified})
        if not verified:
            reasons.append("invalid_source_quote")
    return {"needs_refinement": bool(reasons), "reasons": sorted(set(reasons)),
            "question_words": len(q.split()), "answer_words": len(a.split()),
            "acronyms": sorted(set(acronyms)), "evidence_checks": valid,
            "similarity_used_for_quality_gate": False}


def refine_question(client, question, diagnostic, context):
    system, user = refinement_prompt(question, diagnostic, context)
    result = client.complete_json(user, system=system, max_tokens=8000)
    if isinstance(result, dict) and result.get("unrepairable"):
        return None, str(result.get("reason", "unrepairable"))
    normalized = normalize_question(result)
    return normalized, str(result.get("changes", "")) if isinstance(result, dict) else "invalid_refinement"


def parse_verdict(verdict, cfg):
    if not isinstance(verdict, dict):
        return {"approved": False, "reason": "missing_judge_verdict"}
    if any(type(verdict.get(key)) is not bool for key in BOOLEANS):
        return {"approved": False, "reason": "invalid_judge_booleans", "raw": verdict}
    scores = {}
    for key in WEIGHTS:
        value = verdict.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
            return {"approved": False, "reason": "invalid_judge_scores", "raw": verdict}
        scores[key] = float(value)
    difficulty = verdict.get("difficulty")
    if difficulty not in ("facil", "media", "dificil"):
        return {"approved": False, "reason": "invalid_judge_difficulty", "raw": verdict}
    score = round(sum(scores[key] * weight for key, weight in WEIGHTS.items()), 4)
    failed = [key for key in BOOLEANS if not verdict[key]]
    if score < cfg.minimum_quality:
        failed.append("quality_below_threshold")
    return {"approved": not failed, "reason": ";".join(failed) or None, "nota": score,
            "difficulty": difficulty, "scores": scores,
            "checks": {key: verdict[key] for key in BOOLEANS}, "comment": verdict.get("comment", "")}


def judge_questions(client, questions, context, cfg):
    if not questions:
        return {}
    system, user = judge_prompt(questions, context)
    result = client.complete_json(user, system=system, max_tokens=10000)
    rows = result.get("evaluations", []) if isinstance(result, dict) else []
    if not isinstance(rows, list):
        rows = []
    verdicts, duplicated = {}, set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            continue
        if row["id"] in verdicts:
            duplicated.add(row["id"])
        verdicts[row["id"]] = row
    return {q["id"]: parse_verdict(None if q["id"] in duplicated else verdicts.get(q["id"]), cfg)
            for q in questions}
