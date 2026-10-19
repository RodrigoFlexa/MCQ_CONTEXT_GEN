"""Exporta apenas capítulos/blocos e QA que passaram pelos filtros reais."""
import csv
from collections import Counter
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json, write_jsonl
from .gates import checked_chapter, checked_question, checked_units


def collect(directory):
    return [read_json(path) for path in sorted(Path(directory).glob("*.json"))]


def export_run(config, index_info, interrupted=None):
    out = Path(config.output)
    out.mkdir(parents=True, exist_ok=True)
    plan = read_json(out / "plano.json") or {"recortes": [], "eixos": {},
                                             "descobertas_nao_investigadas": []}
    planned = {f["id"] for f in plan["recortes"]}
    states = {s["id"]: s for s in collect(out / "recortes") if s["id"] in planned}
    packs = collect(out / "unidades")
    all_units = [u for p in packs if p["recorte_id"] in planned for u in p["unidades"]]
    verified_units = {u["id"]: u for p in packs if p["recorte_id"] in states
                      for u in checked_units(p, states[p["recorte_id"]], config)}
    questions = collect(out / "questoes")
    accepted = [q for q in questions if q["id"] in verified_units
                and q["recorte_id"] in states
                and checked_question(q, verified_units[q["id"]], states[q["recorte_id"]], config)]
    invalid = [q["id"] for q in questions if q["status"] == "aprovada_modelo"
               and not any(a["id"] == q["id"] for a in accepted)]
    approved_ids = {q["id"] for q in accepted}
    sources = {}
    for state in states.values():
        for source in state.get("evidencias", []):
            sources[source["id"]] = source
    for question in questions:
        for source in question.get("evidencias_verificacao", []):
            sources.setdefault(source["id"], source)
    chapters, coverage = [], []
    for facet in plan["recortes"]:
        state = states.get(facet["id"], {})
        chapter = checked_chapter(state) or {}
        blocks = chapter.get("blocos", [])
        if state.get("status") in ("auditado_modelo", "parcial") and not blocks:
            invalid.append(facet["id"])
        if blocks:
            chapters.append({"recorte_id": facet["id"], "recorte": facet,
                             "status": state["status"], **chapter})
        units = [u for u in all_units if u["recorte_id"] == facet["id"]]
        coverage.append({"id": facet["id"], "titulo": facet["titulo"],
            "servico": facet["servico"], "fenomeno_produto": facet["fenomeno_produto"],
            "decisao": facet["decisao"], "status": state.get("status", "nao_investigado"),
            "buscas": len(state.get("buscas", [])), "blocos_auditados": len(blocks),
            "unidades": len(units), "unidades_elegiveis": sum(u["id"] in verified_units for u in units),
            "qa_aprovadas_modelo": sum(q["recorte_id"] == facet["id"] for q in accepted),
            "lacunas": state.get("lacunas", []), "erro": state.get("erro")})
    document = {"topico": config.topic, "capitulos": chapters,
                "auditoria": "modelo; validação humana pendente", "cobertura": "limitada; não exaustiva",
                "indice": index_info}
    atomic_json(out / "documento.json", document)
    atomic_json(out / "cobertura.json", {"eixos": plan.get("eixos", {}), "recortes": coverage,
        "descobertas_nao_investigadas": plan.get("descobertas_nao_investigadas", []),
        "lacunas_planejamento": plan.get("lacunas_planejamento", []), "corpus": index_info})
    write_jsonl(out / "evidencias.jsonl", list(sources.values()))
    write_jsonl(out / "unidades.jsonl", all_units)
    write_jsonl(out / "qa_aprovadas.jsonl", accepted)
    write_jsonl(out / "qa_nao_aprovadas.jsonl", [q for q in questions if q["id"] not in approved_ids])
    with (out / "qa.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["pergunta", "resposta"])
        writer.writeheader()
        writer.writerows({k: q[k] for k in writer.fieldnames} for q in accepted)
    body = ["# " + config.topic["titulo"], "", config.topic["escopo"], "",
            "Documento composto somente de blocos aprovados pela auditoria de modelo. "
            "Validação humana pendente. A cobertura se limita ao corpus consultado, "
            "aos recortes e ao orçamento; não representa tudo o que existe sobre o tópico.", ""]
    cited = set()
    for chapter in chapters:
        body.extend(["## " + chapter["titulo"], "", "Estado: " + chapter["status"], ""])
        for block in chapter["blocos"]:
            body.extend([block["texto"], "", " ".join("[" + eid + "]" for eid in block["fontes"]), ""])
            cited.update(block["fontes"])
        if chapter["lacunas"]:
            body.extend(["### Lacunas deste recorte", "", *["- " + gap for gap in chapter["lacunas"]], ""])
    body.extend(["## Referências rastreáveis", ""])
    for eid in sorted(cited):
        source = sources[eid]
        location = []
        for label, key in (("página", "page_ini"), ("linha", "linha_ini")):
            if source.get(key) is not None:
                location.append(f"{label} {source[key]}")
        metadata = "; ".join([str(source.get("collection", "")), source["chunk_id"], *location])
        body.append(f"- [{eid}] {source.get('title', 'Título indisponível')}. {metadata}.")
    (out / "documento_auditado.md").write_text("\n".join(body) + "\n", encoding="utf-8")
    budget = read_json(out / "orcamento.json") or {"tentativas_reservadas": 0}
    embedding_budget = read_json(out / "orcamento_embeddings.json") or {"tentativas_reservadas": 0}
    failed = any(c["erro"] or c["status"] in ("nao_investigado", "pendente_execucao") for c in coverage)
    pending_qa = any(q["status"] == "pendente_validacao" for q in questions)
    summary = {"topico": config.topic["titulo"], "recortes_planejados": len(coverage),
        "recortes_por_status": dict(Counter(c["status"] for c in coverage)),
        "capitulos_publicados": len(chapters), "unidades": len(all_units),
        "unidades_elegiveis": len(verified_units),
        "qa_por_status": dict(Counter(q["status"] for q in questions)),
        "qa_aprovadas_modelo": len(accepted), "meta_qa": config.target_qa,
        "meta_atingida": len(accepted) >= config.target_qa,
        "interrupcao": interrupted, "pendencias_execucao": failed or pending_qa or bool(invalid) or bool(interrupted),
        "bloqueados_integridade": invalid,
        "tentativas_api_cumulativas": budget["tentativas_reservadas"],
        "tentativas_embeddings_cumulativas": embedding_budget["tentativas_reservadas"],
        "retrieval_mode": config.retrieval_mode,
        "indice_hibrido_pronto": index_info.get("retrieval_mode") == "hybrid",
        "corpus_bruto_completo": index_info.get("corpus_bruto_completo", False),
        "validacao_humana": "pendente", "exaustividade": "não demonstrada"}
    atomic_json(out / "resumo.json", summary)
    report = ["# Resultado da execução", "",
        f"- Recortes planejados: {len(coverage)}; capítulos publicados: {len(chapters)}.",
        f"- Unidades extraídas: {len(all_units)}; elegíveis: {summary['unidades_elegiveis']}.",
        f"- QA aprovadas pelo modelo: {len(accepted)}; meta: {config.target_qa}.",
        f"- Tentativas de API cumulativas: {summary['tentativas_api_cumulativas']}.",
        f"- Tentativas de embeddings cumulativas: {summary['tentativas_embeddings_cumulativas']}.",
        f"- Recuperação: {config.retrieval_mode}; índice híbrido pronto: {summary['indice_hibrido_pronto']}.",
        f"- Corpus bruto completo disponível: {summary['corpus_bruto_completo']}.",
        "- Validação humana: pendente. Exaustividade: não demonstrada.", "",
        "A ausência de uma alternativa encontrada não garante unicidade universal. "
        "A resposta deve ser determinada no contexto explicitado."]
    if interrupted:
        report.extend(["", "Interrupção: " + interrupted])
    (out / "relatorio.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return summary
