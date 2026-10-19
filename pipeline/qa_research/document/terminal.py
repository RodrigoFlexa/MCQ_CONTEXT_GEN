"""Aviso de término e comandos concretos para devolver a execução pelo Git."""
import shlex
import sys
from datetime import datetime
from pathlib import Path

from .common import ROOT


def command_path(path):
    path = Path(path).resolve()
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def completion(packet, output, destination=None, status="concluido"):
    output = Path(output).resolve()
    name = output.name.removeprefix("saida_documento_")
    destination = Path(destination).resolve() if destination else ROOT / "pipeline/qa_research/relatorios" / name
    if destination.exists():
        destination = destination.with_name(destination.name + "_retomada_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    face = "🙂"
    try:
        face.encode(sys.stdout.encoding or "utf-8")
    except UnicodeEncodeError:
        face = ":)"
    print("\nO código acabou de rodar no terminal " + face)
    print("Estado da execução: " + status)
    print("\nPara devolver os resultados, execute na raiz do projeto:\n")
    commands = [
        [sys.executable, "-m", "pipeline.qa_research.document", "collect", "--packet", command_path(packet),
         "--output", command_path(output), "--destination", command_path(destination)],
        ["git", "add", "--", command_path(destination)],
        ["git", "commit", "-m", "Resultados do documento Produtos quimicos - sintese v3"],
        ["git", "push", "origin", "codex/qa-evidencias-verificadas"],
    ]
    for command in commands:
        print(shlex.join(command))
    print(flush=True)
    return commands
