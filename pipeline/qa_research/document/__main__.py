"""Entradas explícitas: preparar aqui, pesquisar no servidor, recolher para Git."""
import argparse
import json
from pathlib import Path

from .common import Packet, absolute


def main(argv=None):
    parser = argparse.ArgumentParser(description="Documento científico auditado, sem geração de QA")
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("prepare", help="Triagem lexical + E5 local; não chama Azure")
    prepare.add_argument("--profile", required=True)
    prepare.add_argument("--destination", required=True)
    prepare.add_argument("--feedback", help="pedidos_busca.json devolvido pelo servidor")
    prepare.add_argument("--lexical-only", action="store_true", help="Diagnóstico sem E5; não é o padrão")
    check = commands.add_parser("check", help="Verifica integridade do pacote sem dependências de ML")
    check.add_argument("--packet", required=True)
    run = commands.add_parser("run", help="Somente deep research documental via Azure")
    run.add_argument("--packet", required=True)
    run.add_argument("--output", required=True)
    run.add_argument("--workers", type=int)
    run.add_argument("--max-calls", type=int)
    run.add_argument("--reuse-research", help="Reutilizar leituras/achados de uma saída com o mesmo pacote; redação/auditoria são novas")
    run.add_argument("--results", help="Destino de coleta sugerido no aviso de término")
    collect = commands.add_parser("collect", help="Snapshot dos resultados para git add/commit/push")
    collect.add_argument("--output", required=True)
    collect.add_argument("--packet", required=True)
    collect.add_argument("--destination", required=True)
    args = parser.parse_args(argv)
    if args.command == "prepare":
        from .prepare import prepare as build
        result = build(absolute(args.profile), args.destination, not args.lexical_only, args.feedback)
    elif args.command == "check":
        packet = Packet(absolute(args.packet))
        result = {"valid": True, "signature": packet.signature, "sources": len(packet.sources),
                  "facets": len(packet.facets), "preparation": packet.preparation}
    elif args.command == "run":
        from .runner import run as execute
        from .terminal import completion
        overrides = {key: value for key, value in {"workers": args.workers, "max_calls": args.max_calls}.items() if value is not None}
        status = "falha; consulte o erro e retome após corrigir a causa"
        try:
            result = execute(absolute(args.packet), absolute(args.output), overrides,
                             reuse=absolute(args.reuse_research) if args.reuse_research else None)
            status = result["status"]
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if status == "concluido" else 2
        finally:
            completion(absolute(args.packet), absolute(args.output),
                       absolute(args.results) if args.results else None, status)
    else:
        from .export import collect as snapshot
        result = str(snapshot(absolute(args.output), absolute(args.destination), absolute(args.packet)))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
