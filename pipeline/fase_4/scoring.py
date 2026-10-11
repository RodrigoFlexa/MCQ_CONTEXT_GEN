"""Scorer QA determinístico, refinamento limitado e avaliação técnica do Judge."""
import math
import re
import unicodedata

from pipeline.qa_references.download_qa_examples import CHOICE_REFERENCES, CONTEXT_REFERENCES
from .prompts_qa import refinement_prompt, judge_prompt

WEIGHTS = {"technical_correctness": 0.40, "clarity": 0.20,
           "answer_completeness": 0.20, "domain_relevance": 0.20}
BOOLEANS = ("technical_ok", "supported_by_sources", "scope_ok", "self_contained",
            "context_compatible", "no_unsupported_generalization", "normative_validity", "answer_claims_covered")


def collapse(text):
    return " ".join(text.split())


def normalize_question(raw):
    if not isinstance(raw, dict):
        return None
    if any(not isinstance(raw.get(key), str) or not raw[key].strip() for key in ("question", "answer")):
        return None
    evidence = raw.get("evidence", [])
    return {"question": collapse(raw["question"]), "answer": collapse(raw["answer"]),
            "target_id":raw.get('target_id','') if isinstance(raw.get('target_id',''),str) else '',
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
    if CONTEXT_REFERENCES.search(q + " " + a) or re.search(
        r"texto acima|(?:segundo|conforme|de acordo com) (?:o|os|a|as) (?:material|texto|trechos?|documento|corpus)|"
        r"(?:no|o) esquema|(?:estudo|modelo|trecho) citado|material fornecido|"
        r"(?:o|os) (?:material|trechos?|textos?|corpus) (?:cita|indica|mostra|trata|diz)|"
        r"aparecem explicitamente|não foram consideradas no",q+' '+a,re.I):
        reasons.append("depends_on_external_passage")
    if any(c.isalpha() and not any(script in unicodedata.name(c,'') for script in ('LATIN','GREEK')) for c in q+' '+a):
        reasons.append('unexpected_writing_system')
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


def parse_verdict(verdict, cfg, chunks=()):
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
    reasons=verdict.get('reasons')
    if not isinstance(reasons,dict) or any(not isinstance(reasons.get(k),str) or not reasons[k].strip() for k in BOOLEANS):
        return {'approved':False,'valid':False,'reason':'missing_check_reasons','raw':verdict}
    if type(verdict.get('repairable')) is not bool:
        return {'approved':False,'valid':False,'reason':'invalid_repairable','raw':verdict}
    alignment=verdict.get('evidence_alignment')
    ids={c['chunk_id'] for c in chunks}
    if verdict['supported_by_sources']:
        if not isinstance(alignment,list) or not alignment or any(not isinstance(x,dict) or
            not isinstance(x.get('claim'),str) or not x['claim'].strip() or not isinstance(x.get('chunk_ids'),list)
            or not x['chunk_ids'] or any(not isinstance(cid,str) or cid not in ids for cid in x['chunk_ids']) for x in alignment):
            return {'approved':False,'valid':False,'reason':'invalid_evidence_alignment','raw':verdict}
    score = round(sum(scores[key] * weight for key, weight in WEIGHTS.items()), 4)
    failed = [key for key in BOOLEANS if not verdict[key]]
    if score < cfg.minimum_quality:
        failed.append("quality_below_threshold")
    if scores['technical_correctness']<cfg.minimum_technical:failed.append('technical_score_below_floor')
    if scores['domain_relevance']<cfg.minimum_domain:failed.append('domain_score_below_floor')
    repairable=bool(failed and verdict['repairable'] and all(verdict[k] for k in BOOLEANS if k!='self_contained')
                    and scores['technical_correctness']>=cfg.minimum_technical and scores['domain_relevance']>=cfg.minimum_domain)
    return {"approved": not failed, "valid":True,"reason": ";".join(failed) or None, "nota": score,
            "scores": scores,'reasons':reasons,'evidence_alignment':alignment,'repairable':repairable,
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
    return {q["id"]: parse_verdict(None if q["id"] in duplicated else verdicts.get(q["id"]), cfg,context['chunks'])
            for q in questions}
