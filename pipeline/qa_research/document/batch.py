"""Lote documental no servidor: biblioteca padrão, checkpoints e chamadas Azure.

Não importa a preparação local nem bibliotecas de embeddings. Os itens são
sequenciais; a concorrência interna do Runner é o teto global de chamadas.
"""
import argparse
import json
import re
import shlex
import sys
from datetime import datetime
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from .common import ROOT, Packet, absolute, canonical, file_hash
from .program import (DEFAULT_PACKETS, DEFAULT_PROGRAM, DEFAULT_OUTPUT,
                      DEFAULT_RESULTS, load_program)

DEFAULT_BATCH = DEFAULT_PACKETS + "/lote.json"


def load_batch(path=DEFAULT_BATCH):
    manifest = read_json(absolute(path))
    if not manifest or manifest.get("schema") != "document-batch-v1":
        raise ValueError("Lote ausente; conclua a preparação local antes de enviar ao servidor")
    program = load_program(manifest["program"])
    if file_hash(absolute(manifest["program"])) != manifest["program_sha256"]:
        raise ValueError("O programa mudou depois da preparação")
    if [r["id"] for r in manifest["items"]] != [r["id"] for r in program["items"]]:
        raise ValueError("Frases ausentes ou repetidas no lote")
    for row, expected in zip(manifest["items"], program["items"]):
        if not re.fullmatch(r"\d{2}_\d{2}", row["id"]):
            raise ValueError("ID inválido")
        path = absolute(row["packet"])
        if not path.is_relative_to(ROOT):
            raise ValueError("Pacote deve estar dentro do checkout")
        packet = Packet(path)
        if packet.signature != row["signature"] or row["profile_sha256"] != expected["profile_sha256"]:
            raise ValueError("Assinatura divergente: " + row["id"])
        if packet.profile != read_json(absolute(expected["profile"])):
            raise ValueError("Perfil do pacote diverge da frase: " + row["id"])
        for key in ("area_id", "area", "subtopico"):
            if row[key] != expected[key]:
                raise ValueError("Metadados de agrupamento divergentes: " + row["id"])
    return manifest


def choose(items, only=None):
    if not only:
        return items
    selected = [r for r in items if r["id"] in only or r["area_id"] in only]
    if any(not any(k in (r["id"], r["area_id"]) for r in items) for k in only):
        raise ValueError("Área/frase desconhecida: " + ", ".join(only))
    return selected


def usage(output, items):
    return sum((read_json(output / r["id"] / "orcamento.json") or {}).get("tentativas_reservadas", 0) for r in items)


def run_batch(batch_path=DEFAULT_BATCH, output=DEFAULT_OUTPUT, only=None, workers=3,
              max_calls=None, total_max_calls=None, progress=print, execute=None):
    manifest = load_batch(batch_path)  # Verifica todos os pacotes antes da primeira chamada.
    if workers < 1 or (max_calls is not None and max_calls < 1) or (total_max_calls is not None and total_max_calls < 1):
        raise ValueError("Limites e concorrência devem ser positivos")
    selected = choose(manifest["items"], only)
    output = absolute(output)
    from .runner import run, implementation
    execute = execute or run
    rows = {}
    with output_lock(output):
        identity = {"schema": "document-batch-run-v1", "manifest_sha256": file_hash(absolute(batch_path)),
                    "implementation": implementation()}
        prior = read_json(output / "identidade_lote.json")
        if prior and prior != identity:
            raise ValueError("Código ou lote mudou. Preserve esta saída e use uma nova pasta")
        atomic_json(output / "identidade_lote.json", identity)
        prior_status = read_json(output / "resumo_lote.json") or {}
        rows.update(prior_status.get("items", {}))
        interruption = None
        for i, row in enumerate(selected, 1):
            identifier = row["id"]
            folder = output / identifier
            previous = read_json(folder / "resumo.json")
            item_identity = read_json(folder / "identidade.json") or {}
            if previous and previous.get("status") == "concluido":
                if previous.get("packet_signature") != row["signature"] or item_identity.get("implementation") != identity["implementation"]:
                    raise ValueError("Saída concluída incompatível: " + identifier)
                progress("Documento concluído; sem novas chamadas: " + identifier)
                rows[identifier] = previous
                continue
            settings = Packet(absolute(row["packet"])).profile["runtime"]
            cap = max_calls if max_calls is not None else settings["max_calls"]
            if cap < 1 or workers < 1:
                raise ValueError("Limites devem ser positivos")
            if total_max_calls is not None:
                used = usage(output, manifest["items"])
                already = (read_json(folder / "orcamento.json") or {}).get("tentativas_reservadas", 0)
                remaining = total_max_calls - used
                if remaining <= 0:
                    interruption = "orçamento total do lote atingido"
                    break
                cap = min(cap, already + remaining)
            seed = None
            if identifier == "02_02" and not (folder / "identidade.json").exists():
                prior_research = ROOT / "pipeline/qa_research/relatorios/produtos_quimicos_v3"
                old = read_json(prior_research / "identidade.json") or {}
                if old.get("packet") == row["signature"]:
                    seed = prior_research
            progress(f"Documento {i}/{len(selected)}: {identifier} {row['subtopico']}")
            summary = execute(absolute(row["packet"]), folder,
                overrides={"workers": workers, "max_calls": cap}, progress=progress, reuse=seed)
            rows[identifier] = summary
            state = {"items": rows, "selected": [r["id"] for r in selected],
                "concluidos": sum(s.get("status") == "concluido" for s in rows.values()),
                "documentos_com_conteudo": sum(s.get("blocos_publicados", 0) > 0 for s in rows.values()),
                "status": "em_andamento"}
            atomic_json(output / "resumo_lote.json", state)
            if summary.get("interrupcao"):
                # Orçamento individual não impede as outras frases. Erro de
                # credenciais/backend e cancelamento param o lote imediatamente.
                spent = (read_json(folder / "orcamento.json") or {}).get("tentativas_reservadas", 0)
                if spent < cap or "operador" in summary["interrupcao"]:
                    interruption = summary["interrupcao"]
                    break
        pending = [r["id"] for r in manifest["items"] if rows.get(r["id"], {}).get("status") != "concluido"]
        result = {"items": rows, "selected": [r["id"] for r in selected], "pendentes": pending,
            "concluidos": sum(s.get("status") == "concluido" for s in rows.values()),
            "status": "interrompido" if interruption else ("parcial_com_pendencias" if pending else "concluido"),
            "interrupcao": interruption}
        atomic_json(output / "resumo_lote.json", result)
        return result


def collect_batch(batch_path, output, destination):
    from .export import collect
    manifest = load_batch(batch_path)
    output, destination = absolute(output), absolute(destination)
    if output == destination or output in destination.parents or destination in output.parents:
        raise ValueError("Resultados devem ficar separados da execução")
    with output_lock(output):
        identity = read_json(output / "identidade_lote.json") or {}
        if identity.get("manifest_sha256") != file_hash(absolute(batch_path)):
            raise ValueError("Execução pertence a outro lote")
        # Uma coleta interrompida pode ser retomada, mas nunca sobrescreve um snapshot.
        destination.mkdir(parents=True, exist_ok=True)
        with output_lock(destination):
            receipt = read_json(destination / "coleta_lote.json")
            binding = {"source": str(output), "manifest_sha256": identity["manifest_sha256"]}
            if receipt and receipt != binding:
                raise ValueError("Destino pertence a outra coleta")
            if not receipt and any(p.name != ".run.lock" for p in destination.iterdir()):
                raise ValueError("Destino deve ser novo ou uma coleta interrompida do mesmo lote")
            atomic_json(destination / "coleta_lote.json", binding)
            if (destination / "manifest_resultados_lote.json").exists():
                verify_results(destination)
                return destination
            collected, missing = [], []
            for row in manifest["items"]:
                source, target = output / row["id"], destination / row["id"]
                if not (source / "resumo.json").is_file():
                    missing.append(row["id"])
                    continue
                if not target.exists():
                    collect(source, target, absolute(row["packet"]))
                verify_results(target, "manifest_resultados.json")
                collected.append({**row, "summary": read_json(target / "resumo.json")})
            if not collected:
                raise ValueError("Não há documento ou resumo para coletar")
            atomic_json(destination / "resumo_lote.json", read_json(output / "resumo_lote.json") or {})
            atomic_json(destination / "indice.json", {"items": collected, "nao_executados": missing})
            assemble_areas(destination, collected)
            files = {p.relative_to(destination).as_posix(): file_hash(p)
                for p in destination.rglob("*") if p.is_file() and p.name != ".run.lock"}
            atomic_json(destination / "manifest_resultados_lote.json", {"schema": "document-batch-results-v1", "files": files})
    return destination


def verify_results(path, manifest_name="manifest_resultados_lote.json"):
    path = Path(path).resolve()
    data = read_json(path / manifest_name)
    if not data or not isinstance(data.get("files"), dict):
        raise ValueError("Manifesto de resultados ausente")
    for name, digest in data["files"].items():
        target = (path / name).resolve()
        if not target.is_relative_to(path) or target.is_symlink() or file_hash(target) != digest:
            raise ValueError("Resultado alterado: " + name)


def assemble_areas(destination, rows):
    """Agrupa documentos sem LLM e sem inserir referências no texto de contexto."""
    destination = Path(destination)
    folder = destination / "areas"
    folder.mkdir(exist_ok=True)
    for ai in sorted({r["area_id"] for r in rows}):
        selected = [r for r in rows if r["area_id"] == ai]
        title = selected[0]["area"]
        sections, lines = [], ["# " + title, ""]
        for row in selected:
            document = read_json(destination / row["id"] / "documento.json")
            if not document:
                continue
            subtitle = row["subtopico"] if row["subtopico"] != "Geral" else title
            sections.append({"titulo": subtitle, "capitulos": document["capitulos"]})
            lines.extend(["## " + subtitle, ""])
            for chapter in document["capitulos"]:
                lines.extend(["### " + chapter["titulo"], ""])
                for block in chapter["blocos"]:
                    lines.extend(["#### " + block["subtitulo"], "", block["texto"], ""])
        atomic_json(folder / (ai + ".json"), {"titulo": title, "secoes": sections})
        (folder / (ai + ".md")).write_text("\n".join(lines), encoding="utf-8")
    links = ["# Documentos por área", "", "Estados e pendências: indice.json e resumo_lote.json.", ""]
    links.extend(f"- [{ai} — {next(r['area'] for r in rows if r['area_id'] == ai)}](areas/{ai}.md)" for ai in sorted({r["area_id"] for r in rows}))
    (destination / "INDICE.md").write_text("\n".join(links) + "\n", encoding="utf-8")


def preparation_report(manifest, destination):
    """Relatório auxiliar de cobertura e plano; nunca usado como fonte de QA."""
    from collections import Counter
    sources, entries, executions = {}, [], {}
    lines = ["# Preparação local das dez áreas", "",
        "Relatório de preparação e buscas; não é documento de conhecimento para QA.", "",
        "Cobertura parcial dos originais disponíveis, sem garantia de exaustividade.", ""]
    for row in manifest["items"]:
        packet = Packet(absolute(row["packet"]))
        sources.update(packet.sources)
        execution = packet.preparation.get("execution")
        if execution:
            executions[canonical(execution)] = execution
        entries.append({"id": row["id"], "area": row["area"], "subtopico": row["subtopico"],
            "sources": len(packet.sources), "input_mode": packet.preparation["input_mode"],
            "scanned_windows": packet.preparation["scanned_windows"],
            "facets": [{"id": f["id"], "titulo": f["titulo"], "sources": len(f["fontes"])} for f in packet.facets]})
        lines.extend([f"## {row['id']} — {row['subtopico']}", "", packet.profile["topic"]["escopo"], ""])
        for f in packet.facets:
            lines.extend(["### " + f["titulo"], "", f["foco"], "",
                f"Fontes selecionadas: {len(f['fontes'])}.", "",
                "Âncoras: " + "; ".join(f["termos"]) + ".", "", "Consultas:", ""])
            lines.extend("- " + q for q in f["consultas"])
            lines.append("")
            for gate in f.get("post_context_groups", []):
                lines.extend(["Contexto adicional obrigatório (um dos termos): " + "; ".join(gate) + ".", ""])
    report = {"schema": "document-batch-preparation-report-v1", "areas": len({r['area_id'] for r in manifest['items']}),
        "phrases": len(entries), "facets": sum(len(e["facets"]) for e in entries),
        "unique_sources": len(sources), "unique_texts": len({s['texto_sha256'] for s in sources.values()}),
        "collections": dict(Counter(s.get("collection", "unknown") for s in sources.values())),
        "known_document_sources": sum(s["qualidade"]["documento_identificado"] for s in sources.values()),
        "sources_with_removed_numbers": sum(bool(s["qualidade"]["marcadores_numericos"]) for s in sources.values()),
        "execution": list(executions.values()), "items": entries}
    destination = absolute(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    atomic_json(destination.with_suffix(".json"), report)
    destination.write_text("\n".join(lines), encoding="utf-8")
    return report


def completion_batch(batch_path, output, destination, status):
    from .terminal import command_path
    destination = absolute(destination)
    if destination.exists():
        destination = destination.with_name(destination.name + "_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    face = "🙂"
    try:
        face.encode(sys.stdout.encoding or "utf-8")
    except UnicodeEncodeError:
        face = ":)"
    print("\nO código acabou de rodar no terminal " + face)
    print("Estado da execução: " + status)
    commands = [[sys.executable, "-m", "pipeline.qa_research.document.batch", "collect",
        "--batch", command_path(absolute(batch_path)), "--output", command_path(absolute(output)),
        "--destination", command_path(destination)],
        ["git", "add", "--", command_path(destination)],
        ["git", "commit", "-m", "Resultados documentais das dez areas FPSO"],
        ["git", "push", "origin", "codex/qa-evidencias-verificadas"]]
    print("\nPara devolver os resultados, execute na raiz do projeto:\n")
    for command in commands:
        print(shlex.join(command))
    print(flush=True)
    return commands


def main(argv=None):
    parser = argparse.ArgumentParser(description="Dez áreas / quarenta frases: preparação local e documentos no Azure")
    commands = parser.add_subparsers(dest="command", required=True)
    program = commands.add_parser("program", help="Materializar perfis da curadoria manual; sem LLM")
    program.add_argument("--program", default=DEFAULT_PROGRAM)
    prepare = commands.add_parser("prepare", help="Uma varredura e E5 local compartilhado; não chama Azure")
    prepare.add_argument("--program", default=DEFAULT_PROGRAM)
    prepare.add_argument("--destination", default=DEFAULT_PACKETS)
    prepare.add_argument("--device", choices=("auto", "cuda", "cpu"), default="auto")
    prepare.add_argument("--batch-size", type=int, default=64)
    check = commands.add_parser("check", help="Valida todos os pacotes sem bibliotecas de ML")
    check.add_argument("--batch", default=DEFAULT_BATCH)
    check.add_argument("--report", help="Gravar relatório auxiliar de preparação e das consultas curadas (.md/.json)")
    run = commands.add_parser("run", help="Gerar documentos usando somente Azure no servidor")
    run.add_argument("--batch", default=DEFAULT_BATCH)
    run.add_argument("--output", default=DEFAULT_OUTPUT)
    run.add_argument("--results", default=DEFAULT_RESULTS)
    run.add_argument("--only", nargs="+", help="IDs de áreas (02) ou frases (02_01)")
    run.add_argument("--workers", type=int, default=3)
    run.add_argument("--max-calls", type=int, help="Teto cumulativo de tentativas POR FRASE")
    run.add_argument("--total-max-calls", type=int, help="Teto cumulativo de tentativas para o lote inteiro")
    collect = commands.add_parser("collect", help="Coletar os checkpoints e reunir os documentos em dez áreas")
    collect.add_argument("--batch", default=DEFAULT_BATCH)
    collect.add_argument("--output", default=DEFAULT_OUTPUT)
    collect.add_argument("--destination", default=DEFAULT_RESULTS)
    args = parser.parse_args(argv)
    if args.command == "program":
        from .program import build_program
        result = build_program(args.program)
        print(f"Programa: {result['areas']} áreas, {len(result['items'])} frases")
    elif args.command == "prepare":
        from .batch_prepare import prepare_program
        prepare_program(args.program, args.destination, args.device, args.batch_size)
    elif args.command == "check":
        result = load_batch(args.batch)
        if args.report:
            preparation_report(result, args.report)
        print(canonical({"valid": True, "areas": len({r['area_id'] for r in result['items']}),
            "phrases": len(result["items"]), "facets": sum(r["facets"] for r in result["items"]),
            "empty_facets": {r["id"]: r["empty_facets"] for r in result["items"] if r["empty_facets"]}}))
    elif args.command == "run":
        status = "falha; checkpoints preservados"
        try:
            result = run_batch(args.batch, args.output, args.only, args.workers, args.max_calls, args.total_max_calls)
            status = result["status"]
            print(canonical({k: v for k, v in result.items() if k != "items"}))
            return 0 if status == "concluido" else 2
        finally:
            completion_batch(args.batch, args.output, args.results, status)
    else:
        print(collect_batch(args.batch, args.output, args.destination))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
