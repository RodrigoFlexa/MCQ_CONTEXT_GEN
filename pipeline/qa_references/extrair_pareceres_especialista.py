#!/usr/bin/env python3
"""Classifica o DOCX revisado e separa sementes QA candidatas.

Extrai o enunciado, a alternativa correta marcada em negrito e o parecer
imediatamente seguinte. Não carrega alternativas para o arquivo de sementes.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from docx import Document


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Comentários especialista" / "Questoes_100_por_topico_revisadas.docx"
OUT = ROOT / "pipeline" / "qa_references" / "review"
QUESTION = re.compile(r"^\s*(\d+)\.\s+(.+)$", re.DOTALL)
OPTION = re.compile(r"^\s*([A-D])\)\s*(.*)$", re.DOTALL)
COMMENT = re.compile(r"^\s*Comentário:\s*(.*)$", re.IGNORECASE | re.DOTALL)
REPEATED = re.compile(
    r"repet|semelhan|parecid|idêntic|mesmo cenário|assunto e contexto|"
    r"quest(?:ão|ões) anterior(?:es)?|variaç(?:ão|ões) no enunciado",
    re.I,
)
OUT_OF_SCOPE = re.compile(
    r"fora do contexto|fora da realidade|fora do objetivo|não faz parte|não é questão|"
    r"não propriamente|não condiz|incompatível|mais de .* do que|questão de .* e não",
    re.I,
)
TECHNICAL = re.compile(
    r"erro[s]? (?:de )?conceito|conceito[s]? (?:equivocado|errado|confuso|conflitante)|"
    r"premissa (?:equivocada|incorreta)|cenário improvável|imperfeiç|incorreto|"
    r"alternativa correta .* (?:confusa|não menciona|não traz)|enunciado confuso|"
    r"não menciona aspectos|resposta correta seria",
    re.I,
)
APPROVED = re.compile(r"^\s*aprovad[ao]", re.I)
DISCARD = re.compile(r"descartar|descartad[ao]", re.I)


def visible_question_paragraph(paragraph) -> bool:
    return bool(QUESTION.match(paragraph.text.strip()))


def answer_option(paragraphs: list[Any], question_index: int) -> tuple[str, str]:
    for para in paragraphs[question_index + 1 : question_index + 5]:
        match = OPTION.match(para.text.strip())
        if match and any(run.bold for run in para.runs):
            return match.group(1), match.group(2).strip()
    return "", ""


def review_comment(paragraphs: list[Any], question_index: int) -> str:
    for para in paragraphs[question_index + 1 : question_index + 9]:
        match = COMMENT.match(para.text.strip())
        if match:
            return match.group(1).strip()
        if visible_question_paragraph(para):
            break
    return ""


def classify(comment: str) -> tuple[str, list[str], bool]:
    flags: list[str] = []
    if REPEATED.search(comment):
        flags.append("repeticao_ou_semelhanca")
    if OUT_OF_SCOPE.search(comment):
        flags.append("aderencia_ao_topico_ou_fpos_questionada")
    if TECHNICAL.search(comment):
        flags.append("ressalva_tecnica_ou_de_clareza")
    if DISCARD.search(comment):
        status = "descartar"
    elif APPROVED.search(comment) and flags:
        status = "aprovada_com_ressalvas"
    elif APPROVED.search(comment):
        status = "aprovada"
    elif comment:
        status = "revisar_manual"
    else:
        status = "sem_parecer_extraido"
    seed = status == "aprovada" and not flags
    return status, flags, seed


def main() -> None:
    doc = Document(SOURCE)
    paras = doc.paragraphs
    current_headings: list[str] = []
    rows: list[dict[str, Any]] = []
    sequential_id = 0

    for index, para in enumerate(paras):
        match = QUESTION.match(para.text.strip())
        if not match:
            text = para.text.strip()
            style = (para.style.name or "").lower()
            if text and ("heading" in style or "título" in style or "title" in style):
                level_match = re.search(r"([1-9])", style)
                level = int(level_match.group(1)) if level_match else 1
                current_headings = current_headings[: level - 1] + [text]
            continue

        sequential_id += 1
        letter, answer = answer_option(paras, index)
        comment = review_comment(paras, index)
        status, flags, seed = classify(comment)
        rows.append({
            "review_id": sequential_id,
            "topic_path": " > ".join(current_headings),
            "question": match.group(2).strip(),
            "answer": answer,
            "source_correct_option": letter,
            "review_comment": comment,
            "review_status": status,
            "flags": flags,
            "seed_candidate": seed and bool(answer),
            "seed_note": "aprovada sem ressalva extraída; alternativas removidas" if seed else "",
        })

    OUT.mkdir(parents=True, exist_ok=True)
    all_path = OUT / "questoes_revisadas_classificadas.jsonl"
    seeds_path = OUT / "sementes_qa_candidatas.jsonl"
    csv_path = OUT / "questoes_revisadas_classificadas.csv"
    summary_path = OUT / "resumo_curadoria.md"
    with all_path.open("w", encoding="utf-8", newline="\n") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")
    seeds = [row for row in rows if row["seed_candidate"]]
    with seeds_path.open("w", encoding="utf-8", newline="\n") as file:
        for row in seeds:
            # Formato QA intencional: nenhum distrator/alternativa no arquivo.
            file.write(json.dumps({k: row[k] for k in ("review_id", "topic_path", "question", "answer", "review_comment", "seed_note")}, ensure_ascii=False) + "\n")
    columns = list(rows[0]) if rows else []
    with csv_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            normalized = dict(row)
            normalized["flags"] = "; ".join(row["flags"])
            writer.writerow(normalized)

    statuses = Counter(row["review_status"] for row in rows)
    flag_counts = Counter(flag for row in rows for flag in row["flags"])
    missing_answer = sum(not row["answer"] for row in rows)
    lines = [
        "# Curadoria inicial da revisão do especialista",
        "",
        f"- Questões numeradas extraídas: **{len(rows)}**",
        f"- Questões com resposta correta identificada por negrito: **{len(rows) - missing_answer}**",
        f"- Pareceres de aprovação sem ressalvas detectadas, candidatos a seed: **{len(seeds)}**",
        f"- Questões sem alternativa correta marcada: **{missing_answer}**",
        "",
        "## Classificação do parecer",
        "",
        "| Categoria | Questões |",
        "|---|---:|",
    ]
    for label in ("aprovada", "aprovada_com_ressalvas", "descartar", "revisar_manual", "sem_parecer_extraido"):
        lines.append(f"| {label} | {statuses[label]} |")
    lines += ["", "## Sinalizadores encontrados", "", "| Sinalizador | Questões |", "|---|---:|"]
    for label, count in flag_counts.most_common():
        lines.append(f"| {label} | {count} |")
    lines += [
        "",
        "## Regra conservadora de seeds",
        "",
        "A lista de seeds contém somente questões explicitamente aprovadas sem ressalvas extraídas, com resposta correta identificada. Aprovação com observação, repetição/semelhança, dúvida de escopo, ressalva técnica ou parecer ausente fica fora da lista automática e exige decisão humana. Observações apenas sobre distratores não bloqueiam uma semente QA, pois as alternativas não são exportadas.",
        "",
        "A classificação por expressões é uma triagem inicial, não substitui a leitura humana. Em particular, comentários que apontam repetição entre itens precisam ser comparados com as questões citadas e com as sementes já existentes.",
        "",
    ]
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"questions": len(rows), "statuses": statuses, "flags": flag_counts, "seed_candidates": len(seeds), "outputs": [str(all_path), str(seeds_path), str(csv_path), str(summary_path)]}, ensure_ascii=False, indent=2, default=dict))


if __name__ == "__main__":
    main()
