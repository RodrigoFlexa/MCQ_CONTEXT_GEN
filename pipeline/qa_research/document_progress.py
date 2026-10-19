"""Acompanhamento de documentos, sem alterar a identidade da pesquisa.

Fica fora de document/*.py: mudanças na apresentação do progresso não invalidam
pesquisas já iniciadas. O painel só lê checkpoints; watch nunca chama o backend.
"""
import argparse
import json
import math
import re
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

from .document import batch
from .document.common import absolute
from .document.program import DEFAULT_OUTPUT, DEFAULT_RESULTS

STAGES = {"research": "pesquisa", "write": "redação", "audit": "auditoria",
          "gaps": "revisão de lacunas", "discover": "revisão da cobertura",
          "dedup": "consolidação"}
FINAL = {"concluido", "parcial_com_pendencias", "interrompido"}


def checkpoint(path):
    """Uma troca atômica ou arquivo ainda ausente não pode parar a pesquisa."""
    path = Path(path)
    try:
        with path.open(encoding="utf-8-sig") as stream:
            stamp = path.stat().st_mtime
            data = json.load(stream)
        return (data if isinstance(data, dict) else {}), stamp
    except (OSError, ValueError):
        return {}, 0.


def load_items(path, only=None):
    manifest, _ = checkpoint(absolute(path))
    items = manifest.get("items")
    if manifest.get("schema") != "document-batch-v1" or not isinstance(items, list) or not items:
        raise ValueError("Lote ausente ou inválido; informe o mesmo --batch da geração")
    for row in items:
        if (not isinstance(row, dict) or not re.fullmatch(r"\d{2}_\d{2}", str(row.get("id", "")))
                or type(row.get("facets")) is not int or row["facets"] < 1
                or not isinstance(row.get("subtopico"), str)
                or not re.fullmatch(r"\d{2}", str(row.get("area_id", "")))):
            raise ValueError("Metadados inválidos no lote")
    if len({r["id"] for r in items}) != len(items):
        raise ValueError("IDs repetidos no lote")
    return batch.choose(items, only)


def snapshot(items, output, now=None, session_start=None):
    """Contagens vêm de resumos publicados, não do número de pastas criadas.

    O resumo do lote distingue uma tentativa encerrada de um resumo parcial
    exportado enquanto a auditoria ainda está em andamento.
    """
    now = time.time() if now is None else now
    output = Path(output)
    _, identity_time = checkpoint(output / "identidade_lote.json")
    started = session_start if session_start is not None else (identity_time or now)
    root, root_time = checkpoint(output / "resumo_lote.json")
    returned = root.get("items", {})
    returned = returned if isinstance(returned, dict) else {}
    finished = root.get("status") in FINAL and root_time >= started
    processed, complete, partial, remaining = [], [], [], []
    samples, candidates = [], []
    for row in items:
        identifier = row["id"]
        folder = output / identifier
        summary, summary_time = checkpoint(folder / "resumo.json")
        _, began = checkpoint(folder / "identidade.json")
        activity, activity_time = checkpoint(folder / "progresso.json")
        done = summary.get("status") == "concluido"
        # Tentativas parciais de uma sessão anterior continuam por processar.
        ended = (done or (summary_time >= started and bool(summary)
                         and returned.get(identifier) == summary))
        if ended:
            processed.append(identifier)
            (complete if done else partial).append(identifier)
            seconds = summary.get("session_seconds", 0)
            if (not summary.get("interrupcao") and summary.get("status") in {"concluido", "parcial_com_pendencias"}
                    and isinstance(seconds, (int, float)) and math.isfinite(seconds) and seconds >= 1):
                samples.append((seconds, row["facets"]))
        else:
            remaining.append(row)
            if max(began, activity_time) >= started and not finished:
                candidates.append((max(began, activity_time), identifier,
                    {"id": identifier, "titulo": row["subtopico"], "began": began,
                     "stage": STAGES.get(activity.get("etapa"), "preparação/pesquisa"),
                     "last_activity_seconds": max(0., now - (activity_time or began)),
                     "elapsed_seconds": max(0., now - began) if began else 0.}))
    active = max(candidates)[2] if candidates else None
    eta, note = None, "calculando; aguardando o primeiro documento processado"
    if not remaining:
        eta, note = 0., "todos os documentos selecionados foram processados"
    elif finished:
        note = "execução encerrada; há documentos por processar"
    elif samples:
        # Documentos têm 4 a 12 recortes. Ponderar por recortes evita tratar
        # Produtos químicos como se custasse o mesmo que uma frase menor.
        per_facet = sum(s for s, _ in samples) / sum(w for _, w in samples)
        estimate = per_facet * sum(r["facets"] for r in remaining)
        if active:
            estimate -= active["elapsed_seconds"]
        if estimate > 0:
            eta = estimate
            note = f"aproximada, com base em {len(samples)} documento(s), ponderada por recortes"
        else:
            note = "recalculando; o documento atual ultrapassou a média observada"
    return {"total": len(items), "processed": len(processed), "completed": len(complete),
        "with_pending": len(partial), "remaining": len(remaining), "active": active,
        "elapsed_seconds": max(0., now - started), "eta_seconds": eta,
        "eta_note": note, "sample_documents": len(samples), "finished": finished,
        "status": root.get("status"), "timestamp": now}


def duration(seconds):
    seconds = max(0, int(seconds))
    hours, rest = divmod(seconds, 3600)
    minutes, seconds = divmod(rest, 60)
    if hours:
        return f"{hours}h {minutes:02}min"
    return f"{minutes}min {seconds:02}s" if minutes else f"{seconds}s"


def render(state):
    percent = 100 * state["processed"] / max(1, state["total"])
    clock = datetime.fromtimestamp(state["timestamp"]).astimezone()
    lines = [f"[Andamento {clock:%H:%M:%S}] Documentos processados: {state['processed']}/{state['total']} ({percent:.0f}%)"
             f" | Concluídos: {state['completed']} | Com pendências: {state['with_pending']}"]
    active = state["active"]
    if active:
        lines.append(f"Atual: {active['id']} — {active['titulo']} | Última etapa: {active['stage']}"
                     f" (há {duration(active['last_activity_seconds'])})")
    elif not state["finished"] and state["remaining"]:
        lines.append("Preparando/verificando o próximo documento.")
    eta = state["eta_seconds"]
    timing = "Decorrido nesta sessão: " + duration(state["elapsed_seconds"])
    if eta is not None:
        if state["remaining"] and eta > 0:
            end = datetime.fromtimestamp(state["timestamp"] + eta).astimezone()
            timing += f" | Restante estimado: ~{duration(eta)} | Término estimado: {end:%d/%m %H:%M %Z}"
        else:
            timing += " | Restante desta rodada: 0s"
    else:
        timing += " | Restante estimado: " + state["eta_note"]
    lines.append(timing)
    if eta is not None and eta > 0:
        lines.append("Estimativa " + state["eta_note"] + ".")
    if state["finished"] and state["with_pending"]:
        lines.append("Processado indica tentativa encerrada; os documentos com pendências continuam identificados no resumo.")
    return "\n".join(lines)


class Monitor:
    def __init__(self, items, output, interval=30., emit=print, session_start=None):
        if not math.isfinite(interval) or interval <= 0:
            raise ValueError("O intervalo de progresso deve ser positivo e finito")
        self.items, self.output, self.interval = items, Path(output), interval
        self.emit, self.session_start = emit, session_start
        self.stop_event = threading.Event()
        self.thread = None

    def report(self):
        state = snapshot(self.items, self.output, session_start=self.session_start)
        self.emit("\n" + render(state) + "\n")
        return state

    def _loop(self):
        while not self.stop_event.wait(self.interval):
            self._safe_report()

    def _safe_report(self):
        # O painel é observabilidade: uma falha de leitura/saída não deve
        # interromper nem modificar o motor e seus checkpoints.
        try:
            self.report()
        except (OSError, ValueError, KeyError, TypeError):
            pass

    def __enter__(self):
        self._safe_report()
        self.thread = threading.Thread(target=self._loop, name="document-progress", daemon=True)
        self.thread.start()
        return self

    def __exit__(self, *exc):
        self.stop_event.set()
        self.thread.join()
        self._safe_report()


def parser():
    p = argparse.ArgumentParser(description="Documentos com contagem e estimativa de término no terminal")
    commands = p.add_subparsers(dest="command", required=True)
    for command, help_text in (("run", "Executar o lote com acompanhamento periódico"),
                               ("watch", "Acompanhar uma execução existente, sem chamadas ao backend")):
        sub = commands.add_parser(command, help=help_text)
        sub.add_argument("--batch", default=batch.DEFAULT_BATCH)
        sub.add_argument("--output", default=DEFAULT_OUTPUT)
        sub.add_argument("--only", nargs="+", help="Áreas (02) ou frases (02_01); use a mesma seleção da geração")
        sub.add_argument("--progress-interval", type=float, default=30., help="Intervalo do resumo em segundos (padrão: 30)")
        if command == "run":
            sub.add_argument("--results", default=DEFAULT_RESULTS)
            sub.add_argument("--workers", type=int, default=3)
            sub.add_argument("--max-calls", type=int)
            sub.add_argument("--total-max-calls", type=int)
    return p


def main(argv=None):
    p = parser()
    args = p.parse_args(argv)
    if not math.isfinite(args.progress_interval) or args.progress_interval <= 0:
        p.error("--progress-interval deve ser positivo e finito")
    items = load_items(args.batch, args.only)
    output = absolute(args.output)
    def emit(text):
        print(text, flush=True)
    if args.command == "watch":
        monitor = Monitor(items, output, args.progress_interval, emit)
        try:
            while True:
                if monitor.report()["finished"]:
                    return 0
                time.sleep(args.progress_interval)
        except KeyboardInterrupt:
            print("\nAcompanhamento encerrado; a geração continua no outro terminal.", flush=True)
            return 0
    status = "falha; checkpoints preservados"
    try:
        with Monitor(items, output, args.progress_interval, emit, session_start=time.time()):
            result = batch.run_batch(args.batch, output, args.only, args.workers,
                args.max_calls, args.total_max_calls, progress=emit)
            status = result["status"]
        print(json.dumps({k: v for k, v in result.items() if k != "items"}, ensure_ascii=False), flush=True)
        return 0 if status == "concluido" else 2
    except KeyboardInterrupt:
        status = "interrompido pelo operador; checkpoints preservados"
        return 130
    finally:
        batch.completion_batch(args.batch, output, args.results, status)


if __name__ == "__main__":
    raise SystemExit(main())
