"""CLI do piloto inventário (estilo qa_v7) x configuração EC.

  python -m pipeline.qa_research.inventario_docs run [opções]       todas as etapas (retomável)
  python -m pipeline.qa_research.inventario_docs relatorio <pasta>  refaz só o relatório
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from .core import ITENS, MODELOS, QA, Piloto, ec_mais_recente

ETAPAS = ("relacoes", "combinacoes", "questoes", "avaliar", "relatorio")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.qa_research.inventario_docs")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--saida", type=Path, help="pasta de resultados; repetir a mesma pasta retoma de onde parou")
    r.add_argument("--ec", type=Path, help="questoes.jsonl da configuração EC (padrão: experimento_externos mais recente)")
    r.add_argument("--itens", nargs="+", default=list(ITENS))
    r.add_argument("--total", type=int, default=100, help="questões por método (padrão 100)")
    r.add_argument("--combinacoes", type=int, default=15, help="máximo de combinações por documento")
    r.add_argument("--workers", type=int, default=6)
    r.add_argument("--etapas", nargs="+", choices=ETAPAS, default=list(ETAPAS))
    r.add_argument("--sem-exemplos", action="store_true", help="gera sem os exemplos EC no prompt da questão")
    r.add_argument("--limite-blocos", type=int, help="usa só os N primeiros blocos de cada documento (teste rápido)")
    for papel, padrao in MODELOS.items():
        r.add_argument(f"--modelo-{papel}", default=padrao, help=f"deployment[:esforço] (padrão {padrao})")
    rel = sub.add_parser("relatorio")
    rel.add_argument("saida", type=Path)
    a = ap.parse_args(argv)

    if a.cmd == "relatorio":
        import json
        cfg = json.loads((a.saida / "config.json").read_text(encoding="utf-8"))
        p = Piloto(a.saida, Path(cfg["ec"]), itens=cfg["itens"], total=cfg["total"], modelos=cfg["modelos"],
                   combinacoes_por_doc=cfg["combinacoes_por_doc"], sem_exemplos=cfg["sem_exemplos"],
                   limite_blocos=cfg.get("limite_blocos"))
        p.relatorio()
        print(f"Relatório: {a.saida / 'RELATORIO.md'}")
        return 0

    ec = a.ec or ec_mais_recente()
    if not ec or not Path(ec).exists():
        print("Não encontrei as questões EC (relatorios/experimento_externos_*/EC/questoes.jsonl). Use --ec.")
        return 1
    saida = a.saida or QA / "relatorios" / f"piloto_inventario_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"
    modelos = {papel: getattr(a, f"modelo_{papel}") for papel in MODELOS}
    p = Piloto(saida, Path(ec), itens=a.itens, total=a.total, modelos=modelos, combinacoes_por_doc=a.combinacoes,
               workers=a.workers, sem_exemplos=a.sem_exemplos, limite_blocos=a.limite_blocos)
    print(f"Saída: {saida}\nEC: {ec}\nModelos: {modelos}", flush=True)
    falhas = p.run(tuple(a.etapas))
    print(f"\nRelatório: {saida / 'RELATORIO.md'}")
    if falhas:
        print(f"{falhas} unidades falharam ou ficaram pendentes; rode de novo com --saida {saida} para tentar só elas.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
