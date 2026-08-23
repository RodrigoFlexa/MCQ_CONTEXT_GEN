#!/usr/bin/env python3
"""Acompanha o progresso do experimento lendo os arquivos parciais.

Não interfere na geração: só lê os .jsonl que os pipelines gravam questão
a questão. As metas (assuntos e questões por assunto) são lidas dos próprios
scripts, para não sair de sincronia quando você mudar a configuração.

    python progresso.py         # foto do momento
    python progresso.py -w      # atualiza a cada 10s (Ctrl-C para sair)
    python progresso.py -w 30   # atualiza a cada 30s
"""
import datetime
import json
import re
import sys
import time
from pathlib import Path

OUT_DIR = Path(__file__).parent / "mcq_output"

CONDICOES = [
    ("CONTEXT-GROUNDED", "geracao_mcq_petroles.py",
     "dataset_mcq_petroles_parcial.jsonl"),
    ("INSTRUCTION-ONLY", "geracao_mcq_instrucao.py",
     "dataset_mcq_instrucao_parcial.jsonl"),
]

BAR_W = 22
GREEN, YELLOW, DIM, BOLD, RESET = (
    "\033[32m", "\033[33m", "\033[2m", "\033[1m", "\033[0m")


def ler_config(script):
    """Extrai TOPICS e a meta por assunto do script, sem importá-lo."""
    path = Path(__file__).parent / script
    if not path.exists():
        return [], 0
    txt = path.read_text(encoding="utf-8")
    m = re.search(r"^N_QUESTOES_POR_ASSUNTO\s*=\s*(\d+)", txt, re.M)
    meta = int(m.group(1)) if m else 0
    ns = {}
    try:
        src = txt[txt.index("TOPICS = {"):]
        exec(src[:src.index("\n}\n") + 3], {}, ns)
    except Exception:
        return [], meta
    return list(ns.get("TOPICS", {})), meta


def ler_parcial(nome):
    """Lê o parcial tolerando a última linha ainda sendo escrita."""
    path = OUT_DIR / nome
    if not path.exists():
        return []
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return rows


def barra(feito, meta):
    if meta <= 0:
        return " " * BAR_W
    n = min(int(BAR_W * feito / meta), BAR_W)
    cor = GREEN if feito >= meta else (YELLOW if feito else DIM)
    return f"{cor}{'█' * n}{DIM}{'·' * (BAR_W - n)}{RESET}"


def ritmo(rows):
    """Questões por minuto e tempo desde a última, via generated_at."""
    ts = sorted(r["generated_at"] for r in rows if r.get("generated_at"))
    if len(ts) < 2:
        return None, None
    fmt = "%Y-%m-%dT%H:%M:%S"
    t0 = datetime.datetime.strptime(ts[0], fmt)
    t1 = datetime.datetime.strptime(ts[-1], fmt)
    mins = (t1 - t0).total_seconds() / 60
    qpm = len(ts) / mins if mins > 0 else None
    parado = (datetime.datetime.now() - t1).total_seconds() / 60
    return qpm, parado


def humano(minutos):
    if minutos is None:
        return "—"
    if minutos < 60:
        return f"{minutos:.0f}min"
    return f"{minutos / 60:.1f}h"


def render():
    linhas = []
    for titulo, script, parcial in CONDICOES:
        topics, meta = ler_config(script)
        total_meta = meta * len(topics)
        rows = ler_parcial(parcial)
        por_topico = {}
        for r in rows:
            por_topico[r.get("topic")] = por_topico.get(r.get("topic"), 0) + 1
        feito = len(rows)
        pct = 100 * feito / total_meta if total_meta else 0

        linhas.append(f"{BOLD}{titulo}{RESET}"
                      f"{' ' * max(1, 34 - len(titulo))}"
                      f"{feito:>3}/{total_meta:<3} {pct:>3.0f}%")

        if not rows:
            linhas.append(f"  {DIM}(ainda sem questões){RESET}")
        else:
            largura = max(len(t) for t in topics) if topics else 0
            for tid in topics:
                n = por_topico.get(tid, 0)
                marca = " ✓" if n >= meta else ""
                linhas.append(f"  {tid:<{largura}}  {barra(n, meta)} "
                              f"{n:>3}/{meta:<3}{GREEN}{marca}{RESET}")
            qpm, parado = ritmo(rows)
            if qpm:
                falta = total_meta - feito
                eta = humano(falta / qpm) if falta > 0 and qpm else "—"
                aviso = (f" {YELLOW}(sem novas há {parado:.0f}min){RESET}"
                         if parado and parado > 10 else "")
                linhas.append(f"  {DIM}{qpm:.1f} questões/min · "
                              f"restam ~{eta}{RESET}{aviso}")
        linhas.append("")
    return "\n".join(linhas)


def main():
    intervalo = None
    if "-w" in sys.argv:
        i = sys.argv.index("-w")
        intervalo = int(sys.argv[i + 1]) if len(sys.argv) > i + 1 else 10

    if intervalo is None:
        print(render())
        return
    try:
        while True:
            agora = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"\033[2J\033[H{DIM}{agora} · a cada {intervalo}s · "
                  f"Ctrl-C para sair{RESET}\n")
            print(render())
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
