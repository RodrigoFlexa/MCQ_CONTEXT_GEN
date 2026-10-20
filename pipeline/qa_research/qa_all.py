"""Execução sequencial e coleta dos itens QA, com retomada e isolamento de falhas."""
import argparse
import json
import shlex
import shutil
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from pipeline.inventario.llm import LLMError, is_fatal
from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from .document.common import ROOT, absolute, file_hash
from .document.program import load_program
from .qa_batch.config import Config, DEFAULT_CONFIG
from .qa_batch import inputs


def configurations(config=DEFAULT_CONFIG, output_root=None, from_item=None):
    base = Config.load(config)
    root = absolute(output_root) if output_root else base.output.parent
    program = load_program(base.data["program"])
    ids = [row["id"] for row in program["items"]]
    if from_item is not None:
        if from_item not in ids:
            raise ValueError("Item inicial não pertence ao programa: " + from_item)
        ids = ids[ids.index(from_item):]
    return [Config.load(config, item=item, output=root / item) for item in ids], root


def preflight(configs):
    for config in configs:
        inputs.document(config, inputs.topic(config))


def totals(rows):
    return {"processados": len(rows),
            "aprovados": sum(r["status"] == "aprovado_modelo" for r in rows),
            "pendentes": sum(r["status"] in {"pendente_revisao", "planejamento_insuficiente",
                                            "geracao_insuficiente"} for r in rows),
            "falhas": sum(r["status"] == "erro_execucao" for r in rows),
            "preservados": sum(r.get("preservado", False) for r in rows),
            "questoes_publicadas": sum(r.get("questoes_publicadas", 0) for r in rows)}


def recorded_seconds(output, fallback=0):
    """Usa latência já registrada, não o tempo quase zero de pular um lote pronto."""
    path = output / "chamadas_llm.jsonl"
    seconds = 0.0
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                value = json.loads(line).get("seconds", 0)
                if isinstance(value, (float, int)) and value > 0:
                    seconds += value
            except (ValueError, AttributeError):
                continue  # Uma última linha incompleta não impede a retomada.
    return seconds or fallback


def execute(configs, root, *, run_item=None, progress=print):
    from .qa_batch.runner import run
    run_item = run_item or run
    report = {"schema": "qa-all-run-v1", "total": len(configs), "itens": [], "status": "em_execucao"}
    samples = []
    code = 0
    with output_lock(root):
        try:
            progress(f"Conferindo {len(configs)} documentos antes de chamar a Azure...", flush=True)
            preflight(configs)
            atomic_json(root / "resumo_todos.json", report)
            for index, config in enumerate(configs, 1):
                before = read_json(config.output / "resumo.json")
                started = time.monotonic()
                progress(f"\n===== Tópico {index}/{len(configs)}: {config.item} =====", flush=True)
                row = {"item": config.item, "preservado": False, "questoes_publicadas": 0}
                stop = False
                try:
                    summary = run_item(config, progress=progress)
                    row.update(status=summary["status"], questoes_publicadas=summary.get("questoes_publicadas", 0),
                               motivo=summary.get("motivo", ""))
                    row["preservado"] = before is not None and before == summary
                except KeyboardInterrupt:
                    row.update(status="erro_execucao", tipo_falha="interrupcao", motivo="Interrompido pelo usuário")
                    code, stop = 130, True
                except Exception as exc:
                    row.update(status="erro_execucao", tipo_falha=getattr(exc, "kind", type(exc).__name__),
                               motivo=str(exc), etapa=getattr(exc, "tag", ""))
                    progress(f"{config.item}: {row['tipo_falha']}: {exc}", flush=True)
                    # Validação, limite por item e indisponibilidade após retentativas
                    # ficam neste lote. Configuração/credenciais exigem intervenção.
                    stop = not isinstance(exc, LLMError) or is_fatal(exc) or exc.kind == "fatal"
                    if stop:
                        code = 1
                row["segundos_execucao"] = round(time.monotonic() - started, 2)
                if not stop:
                    duration = recorded_seconds(config.output,
                        before.get("segundos_sessao", 0) if row["preservado"] else row["segundos_execucao"])
                    if duration > 0:
                        samples.append(duration)
                report["itens"].append(row)
                report.update(totals(report["itens"]))
                remaining = len(configs) - index
                report["eta_minutos"] = (round(sum(samples) / len(samples) * remaining / 60, 1)
                                          if samples else (0 if remaining == 0 else None))
                eta = f"{report['eta_minutos']:.1f} min" if report["eta_minutos"] is not None else "calculando"
                atomic_json(root / "resumo_todos.json", report)
                progress(f"Progresso {index}/{len(configs)} | aprovados {report['aprovados']} | "
                         f"pendentes {report['pendentes']} | falhas {report['falhas']} | "
                         f"preservados {report['preservados']} | ETA aproximada: {eta}", flush=True)
                if stop:
                    break
            if code == 0 and (report.get("falhas") or report.get("pendentes")):
                code = 2
            report["status"] = "finalizado" if len(report["itens"]) == len(configs) and code not in (1, 130) else "interrompido"
            return code, report
        except BaseException as exc:
            report["status"] = "interrompido"
            report.update(motivo=str(exc), erro=type(exc).__name__)
            raise
        finally:
            report.update(totals(report["itens"]))
            atomic_json(root / "resumo_todos.json", report)


def collect_all(configs, root, destination):
    from .qa_batch.export import collect
    from .portable import _publish
    root, destination = Path(root).resolve(), Path(destination).resolve()
    if destination.exists() or root == destination or root in destination.parents or destination in root.parents:
        raise ValueError("Use um destino novo e separado da execução")
    with output_lock(root):
        available = [c for c in configs if (c.output / "resumo.json").is_file()
                     and (c.output / "identidade.json").is_file()]
        if not available:
            raise ValueError("Não há resultados QA para coletar")
        destination.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".qa-all-results-", dir=destination.parent))
        try:
            rows = []
            for config in available:
                collect(config.output, staging / config.item)
                summary = read_json(staging / config.item / "resumo.json")
                rows.append({"item": config.item, "status": summary["status"],
                             "questoes_publicadas": summary.get("questoes_publicadas", 0)})
            atomic_json(staging / "indice.json", {"schema": "qa-all-results-v1", "total_programa": len(configs),
                "coletados": len(rows), "itens": rows,
                "nao_iniciados": [c.item for c in configs if c not in available]})
            summary = root / "resumo_todos.json"
            if summary.is_file() and not summary.is_symlink():
                shutil.copy2(summary, staging / summary.name)
            files = {p.relative_to(staging).as_posix(): file_hash(p) for p in staging.rglob("*") if p.is_file()}
            atomic_json(staging / "manifest_resultados.json", {"schema": "qa-all-results-v1", "files": files})
            _publish(staging, destination)
        finally:
            if (staging.exists() and staging.resolve().parent == destination.parent
                    and staging.name.startswith(".qa-all-results-")):
                shutil.rmtree(staging)
    return destination


def shown(path):
    try:
        return Path(path).relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def finished(root, config):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    destination = "pipeline/qa_research/relatorios/qa_todos_" + stamp
    print("\nO código acabou de rodar no terminal 🙂", flush=True)
    print("Para coletar TODOS os lotes e trazer pelo Git:")
    print(f"{shlex.quote(sys.executable)} -m pipeline.qa_research.qa_all collect --config {shlex.quote(config)} "
          f"--output-root {shlex.quote(shown(root))} --destination {destination}")
    print("git add -- " + destination)
    print('git commit -m "Resultados QA dos 40 subtopicos"')
    print("git push")


def main(argv=None):
    parser = argparse.ArgumentParser(description="QA nos itens do programa, com retomada e progresso")
    sub = parser.add_subparsers(dest="action", required=True)
    for action in ("run", "check", "collect"):
        p = sub.add_parser(action)
        p.add_argument("--config", default=DEFAULT_CONFIG)
        p.add_argument("--output-root")
        if action != "collect":
            p.add_argument("--from-item", help="Iniciar neste ID, por exemplo 03_02")
        else:
            p.add_argument("--destination", required=True)
    args = parser.parse_args(argv)
    root = None
    try:
        configs, root = configurations(args.config, args.output_root, getattr(args, "from_item", None))
        if args.action == "check":
            preflight(configs)
            print(json.dumps({"documentos_validados": len(configs), "saida": str(root), "chamadas_api": 0},
                             ensure_ascii=False, indent=2))
            return 0
        if args.action == "collect":
            print(collect_all(configs, root, absolute(args.destination)))
            return 0
        code, report = execute(configs, root)
        print(json.dumps({k: v for k, v in report.items() if k != "itens"}, ensure_ascii=False, indent=2))
        return code
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Falha: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrompido; checkpoints preservados.", file=sys.stderr)
        return 130
    finally:
        if args.action == "run" and root is not None:
            finished(root, args.config)


if __name__ == "__main__":
    raise SystemExit(main())
