#!/usr/bin/env python3
"""Baixa e normaliza exemplos QA de benchmarks para few-shot de formato.

Os registros exportados têm pergunta e resposta. --preserve-reasoning-context conserva
as sentenças de suporte do HotpotQA para demonstração de raciocínio no QA v11.
Alternativas não são exportadas. O contexto não vira evidência técnica de FPSO.
O catálogo inclui a atribuição/licença para manter a proveniência por registro.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT / "data" / "qa_examples.jsonl"
API = "https://datasets-server.huggingface.co"

# ARC e benchmarks QA de domínio geral: exemplos servem para formato/raciocínio,
# nunca como fonte técnica sobre operação de FPSO. SciQ (CC BY-NC) e OpenBookQA
# (licença não claramente indicada no material consultado) ficam fora do padrão.
CATALOG: list[dict[str, Any]] = [
    {
        "id": "pira_ptbr",
        "dataset": "paulopirozelli/pira",
        "config": "default",
        "split": "train",
        "license": "CC BY 4.0",
        "url": "https://github.com/C4AI/Pira",
        "language": "pt-BR",
        "question_fields": ["question_pt_origin"],
        "answer_fields": ["answer_pt_validate", "answer_pt_origin"],
        "quality_fields": {"question_meaningful": 4, "answer_equivalent": 4},
    },
    {
        "id": "arc_challenge",
        "dataset": "allenai/ai2_arc",
        "config": "ARC-Challenge",
        "split": "train",
        "license": "CC BY-SA 4.0",
        "url": "https://huggingface.co/datasets/allenai/ai2_arc",
        "language": "en",
        "question_fields": ["question"],
        "answer_fields": [],
        "answer_key_field": "answerKey",
        "choices_field": "choices",
    },
    {
        "id": "arc_easy",
        "dataset": "allenai/ai2_arc",
        "config": "ARC-Easy",
        "split": "train",
        "license": "CC BY-SA 4.0",
        "url": "https://huggingface.co/datasets/allenai/ai2_arc",
        "language": "en",
        "question_fields": ["question"],
        "answer_fields": [],
        "answer_key_field": "answerKey",
        "choices_field": "choices",
    },
    {
        # Perguntas de ciências que exigem combinar dois fatos; 8 alternativas na origem,
        # das quais só a correta é exportada como resposta.
        "id": "qasc",
        "dataset": "allenai/qasc",
        "config": "default",
        "split": "train",
        "license": "CC BY 4.0",
        "url": "https://huggingface.co/datasets/allenai/qasc",
        "language": "en",
        "question_fields": ["question"],
        "answer_fields": [],
        "answer_key_field": "answerKey",
        "choices_field": "choices",
    },
    {
        "id": "squad_v2",
        "dataset": "rajpurkar/squad_v2",
        "config": "default",
        "split": "train",
        "license": "CC BY-SA 4.0",
        "url": "https://huggingface.co/datasets/rajpurkar/squad_v2",
        "language": "en",
        "question_fields": ["question"],
        "answer_fields": ["answers"],
        "answer_nested_fields": ["text"],
        "require_nonempty_answer": True,
    },
    {
        "id": "hotpotqa",
        "dataset": "hotpotqa/hotpot_qa",
        "config": "distractor",
        "split": "train",
        "license": "CC BY-SA 4.0",
        "url": "https://github.com/hotpotqa/hotpot",
        "language": "en",
        "question_fields": ["question"],
        "answer_fields": ["answer"],
    },
    {
        "id": "boolq",
        "dataset": "google/boolq",
        "config": "default",
        "split": "train",
        "license": "CC BY-SA 3.0",
        "url": "https://huggingface.co/datasets/google/boolq",
        "language": "en",
        "question_fields": ["question"],
        "answer_fields": ["answer"],
    },
]

CHOICE_REFERENCES = re.compile(
    r"\b(which|what)\s+of\s+the\s+following\b|\b(select|choose|pick)\s+"
    r"(one|the correct|the best|an answer|a response)\b|\b(option|alternative)\s+[A-E]\b|"
    r"\b(?:qual|quais)\s+d[ao]s?\s+seguintes\b|\bassinale\b|\bselecione\s+(uma|a|o)\b|"
    r"\bwhich\s+of\s+these\b|\bwhich\s+(statement|sentence|choice|option)\b|"
    r"\b(opção|alternativa)\s+[A-E]\b",
    re.IGNORECASE,
)
CONTEXT_REFERENCES = re.compile(
    r"\b(according to|based on|in|from)\s+(the\s+)?(passage|text|article|paragraph|context)\b|"
    r"\b(the|above)\s+(passage|text|article|paragraph)\b|"
    r"\b(segundo|conforme|de acordo com)\s+(o\s+)?(texto|trecho|documento|passagem)\b|"
    r"\b(texto|trecho|passagem)\s+(acima|a seguir)\b",
    re.IGNORECASE,
)
LABEL_ONLY = re.compile(r"^\s*(?:[A-E]|\d+)\s*[).:-]?\s*$", re.IGNORECASE)
TAG = re.compile(r"<[^>]+>")


def get_json(url: str, retries: int = 4) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            req = Request(url, headers={"User-Agent": "PetroQuest-QA-examples/1.0"})
            with urlopen(req, timeout=90) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt + 1 < retries:
                time.sleep(min(2 ** attempt, 15))
    raise RuntimeError(f"Falha ao consultar {url}: {last_error}")


def choose_text(row: dict[str, Any], fields: list[str], nested_fields: list[str] | None = None) -> str:
    for field in fields:
        value: Any = row.get(field)
        if nested_fields:
            for nested in nested_fields:
                if isinstance(value, dict):
                    value = value.get(nested)
        if isinstance(value, dict) and "text" in value:
            value = value["text"]
        if isinstance(value, list):
            value = next((item for item in value if isinstance(item, str) and item.strip()), "")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def arc_answer(row: dict[str, Any]) -> str:
    key = str(row.get("answerKey", "")).strip()
    choices = row.get("choices") or {}
    labels = choices.get("label", []) if isinstance(choices, dict) else []
    texts = choices.get("text", []) if isinstance(choices, dict) else []
    for label, text in zip(labels, texts):
        if str(label).strip().casefold() == key.casefold():
            # Só a resposta correta é exportada; nenhuma alternativa acompanha a pergunta.
            return str(text).strip()
    return ""


def normalize(entry: dict[str, Any], wrapped: dict[str, Any]) -> dict[str, Any] | None:
    row = wrapped.get("row", {})
    question = choose_text(row, entry["question_fields"])
    if not question or CHOICE_REFERENCES.search(question) or CONTEXT_REFERENCES.search(question):
        return None

    if entry.get("answer_key_field"):
        answer = arc_answer(row)
    else:
        answer = choose_text(row, entry["answer_fields"], entry.get("answer_nested_fields"))
        # BoolQ usa booleano como resposta gold.
        if isinstance(row.get("answer"), bool):
            answer = "Yes" if row["answer"] else "No"
    if not answer or LABEL_ONLY.fullmatch(answer):
        return None
    if entry.get("require_nonempty_answer") and not answer.strip():
        return None

    for field, minimum in entry.get("quality_fields", {}).items():
        try:
            if float(row.get(field) or 0) < minimum:
                return None
        except (TypeError, ValueError):
            return None

    question = " ".join(TAG.sub(" ", question).split())
    answer = " ".join(TAG.sub(" ", answer).split())
    if len(question) < 12 or len(answer) < 1:
        return None
    return {
        "id": f"{entry['id']}:{row.get('id', row.get('id_qa', row.get('qa_id', wrapped.get('row_idx', 'unknown'))))}",
        "question": question,
        "answer": answer,
        "source_dataset": entry["dataset"],
        "source_url": entry["url"],
        "source_license": entry["license"],
        "source_language": entry["language"],
        "source_split": entry["split"],
        "example_role": "format_only",
        **({"reasoning_context": hotpot_support(row), "example_role": "format_and_reasoning_only"}
           if entry.get("preserve_reasoning_context") and entry["id"] == "hotpotqa" else {}),
    }


def hotpot_support(row: dict[str, Any]) -> list[dict[str, Any]]:
    """Preserva somente sentenças realmente anotadas como suporte, sem gerar explicações."""
    context = row.get('context') or {}
    facts = row.get('supporting_facts') or {}
    if not isinstance(context, dict) or not isinstance(facts, dict):
        return []
    passages = dict(zip(context.get('title', []), context.get('sentences', [])))
    out = []
    for title, index in zip(facts.get('title', []), facts.get('sent_id', [])):
        sentences = passages.get(title, [])
        if isinstance(index, int) and 0 <= index < len(sentences):
            out.append({'title': title, 'sentence_index': index, 'text': sentences[index]})
    return out


def dataset_rows(entry: dict[str, Any], max_rows: int, seed: int) -> list[dict[str, Any]]:
    params = {"dataset": entry["dataset"]}
    splits_url = f"{API}/splits?{urlencode(params)}"
    metadata = get_json(splits_url)
    exists = any(
        s.get("config") == entry["config"] and s.get("split") == entry["split"]
        for s in metadata.get("splits", [])
    )
    if not exists:
        available = ", ".join(f"{s.get('config')}/{s.get('split')}" for s in metadata.get("splits", []))
        raise RuntimeError(f"Split indisponível para {entry['id']}: {entry['config']}/{entry['split']}. Disponíveis: {available}")

    base = {
        "dataset": entry["dataset"],
        "config": entry["config"],
        "split": entry["split"],
        "length": 100,
    }
    first = get_json(f"{API}/rows?{urlencode({**base, 'offset': 0})}")
    total = int(first.get("num_rows_total", len(first.get("rows", []))))
    limit = min(max_rows, total)
    page_count = (total + 99) // 100
    page_indices = list(range(page_count))
    random.Random(f"{seed}:{entry['id']}").shuffle(page_indices)

    result = list(first.get("rows", [])) if page_indices and page_indices[0] == 0 else []
    seen_pages = {0} if result else set()
    for page in page_indices:
        if len(result) >= limit:
            break
        if page in seen_pages:
            continue
        start = page * 100
        payload = get_json(f"{API}/rows?{urlencode({**base, 'offset': start})}")
        result.extend(payload.get("rows", []))
        seen_pages.add(page)
    # Um lote de 100 é indivisível no endpoint; o limite final é aplicado abaixo.
    return result[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT, help="JSONL final com pergunta, resposta e proveniência")
    parser.add_argument("--max-per-dataset", type=int, default=500, help="Máximo de registros exportados por conjunto (0 = todos)")
    parser.add_argument("--seed", type=int, default=42, help="Semente para amostragem estável de páginas")
    parser.add_argument("--only", nargs="*", help="IDs opcionais: " + ", ".join(item["id"] for item in CATALOG))
    parser.add_argument("--preserve-reasoning-context", action="store_true",
                        help="Conserva sentenças anotadas de suporte do HotpotQA, sem alternativas")
    args = parser.parse_args()
    if args.max_per_dataset < 0:
        parser.error("--max-per-dataset deve ser >= 0")

    selected = [{**item, 'preserve_reasoning_context': args.preserve_reasoning_context}
                for item in CATALOG if not args.only or item["id"] in args.only]
    unknown = set(args.only or []) - {item["id"] for item in CATALOG}
    if unknown:
        parser.error(f"IDs desconhecidos: {', '.join(sorted(unknown))}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    all_items: list[dict[str, Any]] = []
    failures: list[str] = []
    for entry in selected:
        try:
            limit = args.max_per_dataset or 2**31 - 1
            raw = dataset_rows(entry, limit, args.seed)
            normalized = [item for wrapped in raw if (item := normalize(entry, wrapped))]
            # O filtro pode reduzir o total. Completar além da primeira amostra
            # fica explícito ao usuário para evitar downloads surpresa.
            counts[entry["id"]] = len(normalized)
            all_items.extend(normalized)
            print(f"{entry['id']}: {len(normalized)} exemplos normalizados", file=sys.stderr)
        except Exception as exc:
            failures.append(entry["id"])
            print(f"AVISO: {entry['id']} não foi baixado: {exc}", file=sys.stderr)

    if not all_items:
        print("Nenhuma fonte foi baixada; confira a conexão e tente novamente. O arquivo de saída não foi criado.", file=sys.stderr)
        return 1

    with args.out.open("w", encoding="utf-8", newline="\n") as output:
        for item in all_items:
            output.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(json.dumps({"arquivo": str(args.out), "total": len(all_items), "por_dataset": counts, "fontes_com_falha": failures}, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
