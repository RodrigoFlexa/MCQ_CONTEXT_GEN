"""Publica apenas blocos cujo conteúdo e suporte continuam aprovados."""
import json
import shutil
import tempfile
from collections import Counter
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json, sha, write_jsonl
from ..portable import _publish
from . import VERSION, contracts as C
from .common import Packet, canonical, file_hash


def export_document(packet, output, states, consolidation, reserved, timings,
                    interruption=None, session_seconds=None):
    output = Path(output)
    approved = {fid: C.approved(s, packet) for fid, s in states.items()}
    current_signature = sha(canonical([b for f in packet.facets for b in approved[f["id"]]]), 64)
    # Uma consolidação de versão anterior jamais apaga blocos novos.
    removed = consolidation.get("removed", {}) if consolidation.get("signature") == current_signature else {}
    kept = {fid: [b for b in bs if b["id"] not in removed] for fid, bs in approved.items()}
    all_blocks = {b["id"]: b for bs in approved.values() for b in bs}
    chapters, ledger, coverage, requests, rejected = [], [], [], [], []
    for facet in packet.facets:
        fid, state = facet["id"], states[facet["id"]]
        resolutions = {r["id"]: r for r in state["resolutions"]}
        facet_gaps = []
        for entry in state["gap_history"]:
            row = resolutions.get(entry["id"])
            try:
                if not state.get("gaps_done") or not row:
                    raise ValueError("Reavaliação pendente")
                citations = {c for b in approved[fid] for c in b["trechos"]}
                C.gaps({"resolucoes": [row]}, {entry["id"]}, {b["id"]: b for b in approved[fid]}, citations)
                item = {**entry, **row}
            except (ValueError, TypeError, KeyError):
                item = {**entry, "estado": "nao_reavaliada", "parecer": "Reavaliação ainda não concluída.", "blocos": [], "trechos": []}
            item["blocos_apos_consolidacao"] = list(dict.fromkeys(removed.get(b, b) for b in item["blocos"]))
            facet_gaps.append(item)
            ledger.append({"recorte": fid, **item})
        merged_into = list(dict.fromkeys(removed[b["id"]] for b in approved[fid] if b["id"] in removed))
        pending = not state["read_done"] or bool(state.get("pending_error")) or (
            state["status"] not in {"sem_suporte", "sem_blocos_aprovados", "auditado"}) or (
            state["status"] == "auditado" and not state.get("gaps_done"))
        coverage.append({"id": fid, "titulo": facet["titulo"], "grupo": facet["grupo"], "status": state["status"],
            "pendente": pending, "fontes_disponiveis": len(facet["fontes"]), "fontes_lidas": len(state["seen"]),
            "rodadas": state["round"], "achados_validos": len(state["findings"]),
            "blocos_aprovados": len(approved[fid]), "blocos_publicados": len(kept[fid]),
            "consolidado_em": merged_into, "lacunas": dict(Counter(g["estado"] for g in facet_gaps)),
            "erro_pendente": state.get("pending_error")})
        chapters.append({"id": fid, "titulo": facet["titulo"], "grupo": facet["grupo"], "foco": facet["foco"],
                         "blocos": kept[fid], "consolidado_em": merged_into, "lacunas": facet_gaps})
        queries = list(state["requests"])
        for other in states.values():
            for proposal in other["discoveries"]:
                if proposal["recorte_destino"] == fid:
                    queries.extend(proposal["consultas"])
        if not kept[fid] and not merged_into:
            queries.extend(facet["consultas"])
        requests.append({"facet_id": fid, "queries": list(dict.fromkeys(queries))[:30]})
        for b in state["active_blocks"]:
            if b["id"] not in all_blocks:
                rejected.append({"recorte": fid, "bloco": b, "auditoria": state["reviews"].get(b["id"]),
                                 "motivo": "Sem aprovação íntegra nos cinco critérios"})
    used_citations = list(dict.fromkeys(c for bs in kept.values() for b in bs for c in b["trechos"]))
    sources = list(dict.fromkeys(packet.citations[c]["fonte"] for c in used_citations))
    refs = {sid: i for i, sid in enumerate(sources, 1)}
    calls = []
    log = output / "chamadas_llm.jsonl"
    malformed_logs = 0
    if log.is_file():
        for line in log.read_text(encoding="utf-8").splitlines():
            try:
                calls.append(json.loads(line))
            except ValueError:
                malformed_logs += 1
    pending = [r["id"] for r in coverage if r["pendente"]]
    consolidation_complete = consolidation.get("signature") == current_signature and consolidation.get("complete") is True
    pending_stages = [] if consolidation_complete else ["consolidacao"]
    summary = {"version": VERSION, "document_only": True,
        "status": "interrompido" if interruption else ("parcial_com_pendencias" if pending or pending_stages else "concluido"),
        "interrupcao": interruption, "packet_signature": packet.signature,
        "recortes": len(coverage), "recortes_pendentes": pending, "etapas_pendentes": pending_stages,
        "recortes_com_conteudo": sum(bool(kept[f["id"]]) or bool(r["consolidado_em"]) for f, r in zip(packet.facets, coverage)),
        "blocos_publicados": sum(len(bs) for bs in kept.values()), "fontes_citadas": len(sources),
        "tentativas_reservadas": reserved, "tentativas_registradas": len(calls),
        "tentativas_sem_log": max(0, reserved - len(calls)), "linhas_log_invalidas": malformed_logs,
        "respostas_validas": sum(r.get("ok") is True for r in calls),
        "respostas_invalidas": sum(r.get("ok") is False for r in calls),
        "prompt_tokens": sum(r.get("prompt_tokens", 0) for r in calls),
        "completion_tokens": sum(r.get("completion_tokens", 0) for r in calls),
        "tempos_sessao": timings, "session_seconds": session_seconds,
        "consolidacao_completa": consolidation_complete,
        "limites": packet.preparation["limitations"], "input_mode": packet.preparation["input_mode"]}
    document = {"topic": packet.profile["topic"], "summary": summary, "capitulos": chapters,
                "referencias": [{"numero": refs[sid], "fonte": packet.sources[sid]} for sid in sources]}
    atomic_json(output / "documento.json", document)
    atomic_json(output / "cobertura.json", coverage)
    atomic_json(output / "lacunas.json", ledger)
    atomic_json(output / "pedidos_busca.json", {"topic": packet.profile["topic"], "requests": requests})
    atomic_json(output / "rejeicoes.json", rejected)
    atomic_json(output / "resumo.json", summary)
    write_jsonl(output / "evidencias_citadas.jsonl", (packet.sources[sid] for sid in sources))
    write_jsonl(output / "suporte.jsonl", packet.support(used_citations))
    lines = ["# " + packet.profile["topic"]["titulo"], "", "Síntese documental baseada em passagens originais do corpus.", "",
        f"Estado da execução: **{summary['status']}**. Blocos publicados: {summary['blocos_publicados']}.", "",
        "A auditoria é automatizada por modelo e verificações de integridade; não substitui revisão técnica especializada.", "",
        "## Alcance das fontes", "", *["- " + s for s in summary["limites"]], ""]
    group = None
    for chapter in chapters:
        if group != chapter["grupo"]:
            group = chapter["grupo"]
            lines.extend(["## " + group, ""])
        lines.extend(["### " + chapter["titulo"], ""])
        for block in chapter["blocos"]:
            numbers = sorted({refs[packet.citations[c]["fonte"]] for c in block["trechos"]})
            lines.extend([block["texto"] + " " + " ".join(f"[{n}]" for n in numbers), "",
                          "<!-- bloco: " + block["id"] + " -->", ""])
        if not chapter["blocos"]:
            lines.extend(["Conteúdo consolidado nos blocos " + ", ".join(chapter["consolidado_em"]) + "." if chapter["consolidado_em"] else
                          "Ainda não há conteúdo aprovado para publicação neste recorte.", ""])
        current = [g for g in chapter["lacunas"] if g["estado"] in {"aberta", "parcial"}]
        if current:
            lines.extend(["**Lacunas atuais:**", "", *[f"- ({g['estado']}) {g['texto']} — {g['parecer']}" for g in current], ""])
        unreviewed = [g for g in chapter["lacunas"] if g["estado"] == "nao_reavaliada"]
        if unreviewed:
            lines.extend(["**Pendências de reavaliação:**", "", *["- " + g["texto"] for g in unreviewed], ""])
    lines.extend(["## Referências e procedência", ""])
    for sid in sources:
        s = packet.sources[sid]
        known = s["qualidade"]["documento_identificado"]
        lines.extend([f"[{refs[sid]}] {s.get('title') or 'Título não identificado'}. "
            f"Coleção: {s.get('collection', 'indeterminada')}. "
            f"Documento individual: {'identificado' if known else 'limite indeterminado no texto agregado'}. "
            f"Página: {s.get('page_ini') if s.get('page_ini') is not None else 'não identificada'}. "
            f"Fonte `{sid}`; chunk original `{s['chunk_id']}`.", ""])
    (output / "documento_auditado.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def collect(output, destination, packet_path):
    """Snapshot verificável para Git, excluindo credenciais, índices e caches."""
    output, destination = Path(output).resolve(), Path(destination).resolve()
    if destination.exists() or output == destination or output in destination.parents or destination in output.parents:
        raise ValueError("Use um destino novo e separado da execução")
    packet = Packet(packet_path)
    with output_lock(output):
        identity = read_json(output / "identidade.json")
        if not identity or identity["packet"] != packet.signature:
            raise ValueError("Saída não pertence ao pacote informado")
        destination.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".results-", dir=destination.parent))
        try:
            filenames = ("documento_auditado.md", "documento.json", "cobertura.json", "lacunas.json", "pedidos_busca.json",
                "rejeicoes.json", "resumo.json", "evidencias_citadas.jsonl", "suporte.jsonl", "identidade.json",
                "orcamento.json", "backend.json", "consolidacao.json", "progresso.json", "chamadas_llm.jsonl")
            for name in filenames:
                src = output / name
                if src.is_file() and not src.is_symlink():
                    shutil.copy2(src, staging / name)
            if not (staging / "resumo.json").is_file():
                raise ValueError("Execução ainda não produziu resumo verificável")
            for directory in ("recortes", "chamadas"):
                for src in (output / directory).glob("*.json"):
                    if src.is_symlink():
                        raise ValueError("Link simbólico inesperado nos resultados")
                    (staging / directory).mkdir(exist_ok=True)
                    shutil.copy2(src, staging / directory / src.name)
            for src in (output / ".local" / "respostas_brutas").glob("*.json"):
                if src.is_symlink():
                    raise ValueError("Link simbólico inesperado nas respostas")
                (staging / "respostas_brutas").mkdir(exist_ok=True)
                shutil.copy2(src, staging / "respostas_brutas" / src.name)
            (staging / "pacote").mkdir()
            for name in ("manifest.json", "profile.json", "preparation.json", "facets.json"):
                shutil.copy2(packet.path / name, staging / "pacote" / name)
            files = {p.relative_to(staging).as_posix(): file_hash(p) for p in staging.rglob("*") if p.is_file()}
            atomic_json(staging / "manifest_resultados.json", {"schema": "document-results-v2", "files": files,
                "packet_signature": packet.signature})
            _publish(staging, destination)
        finally:
            if staging.exists() and staging.parent == destination.parent and staging.name.startswith(".results-"):
                shutil.rmtree(staging)
    return destination
