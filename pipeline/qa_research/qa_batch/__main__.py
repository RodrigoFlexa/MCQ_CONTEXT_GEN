"""Prévia offline, checagem de entrada, execução unitária e coleta de resultados."""
import argparse
import json
import shlex
import sys
from datetime import datetime, timezone
from pathlib import Path

from ..document.common import ROOT, absolute
from .config import Config, DEFAULT_CONFIG
from . import inputs


def shown(path):
    try:
        return Path(path).relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def finished(config):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    destination = f"pipeline/qa_research/relatorios/qa_lote_9_{config.item}_{stamp}"
    # Comandos concretos para Bash, o terminal usado no servidor.
    command = f"python -m pipeline.qa_research.qa_batch collect --output {shlex.quote(shown(config.output))} --destination {destination}"
    print("\nO código acabou de rodar no terminal 🙂", flush=True)
    print("Para trazer os resultados pelo Git (terminal do servidor):", flush=True)
    print(command)
    print("git add -- " + destination)
    print(f'git commit -m "Resultados QA de {config.item}"')
    print("git push")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Um lote QA: 9 questões, 3 por dificuldade; sem reindexação")
    sub = parser.add_subparsers(dest="action", required=True)
    for action in ("plan", "check", "run"):
        p = sub.add_parser(action)
        p.add_argument("--config", default=DEFAULT_CONFIG)
        p.add_argument("--item", help="Uma frase do especialista, por exemplo 02_02")
        p.add_argument("--document", help="documento.json; padrão: snapshot documental do item")
        p.add_argument("--output", help="Diretório exclusivo deste lote")
    p = sub.add_parser("collect")
    p.add_argument("--output", required=True)
    p.add_argument("--destination", required=True)
    args = parser.parse_args(argv)
    try:
        if args.action == "collect":
            from .export import collect
            print(collect(absolute(args.output), absolute(args.destination)))
            return 0
        config = Config.load(args.config, item=args.item, document=args.document, output=args.output)
        if args.action == "run":
            try:
                from .runner import run
                summary = run(config)
                print(json.dumps(summary, ensure_ascii=False, indent=2))
                return 0 if summary["status"] == "aprovado_modelo" else 2
            finally:
                finished(config)
        selected = inputs.topic(config)
        info = {"item": selected, "documento": str(config.document), "saida": str(config.output),
                "models": config.models, "quantidade": 9, "por_dificuldade": 3,
                "max_refinamentos": config.data["max_refinements"],
                "limite_tentativas_cumulativo": config.data["max_calls"],
                "chamadas_sem_retentativas": "4 sem refinamento; 7 com um refinamento",
                "chamadas_api_executadas": 0}
        if args.action == "check":
            source = inputs.document(config, selected)
            info["entrada"] = {k: v for k, v in source.items() if k != "contexto_tecnico"}
        else:
            info["documento_disponivel"] = config.document.is_file()
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"Falha: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrompido; checkpoints preservados.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
