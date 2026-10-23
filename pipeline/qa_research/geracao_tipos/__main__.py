"""CLI da geração híbrida por tipo de questão.

  python -m pipeline.qa_research.geracao_tipos run [opções]       reclassificação, janelas, compostas, auditoria
  python -m pipeline.qa_research.geracao_tipos relatorio <pasta>  refaz só o relatório
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from .core import ENCADEAMENTOS, ITENS, MODELOS, QA, Geracao, read_json

ETAPAS = ("reclassificar", "janelas", "compostas", "auditoria", "relatorio")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.qa_research.geracao_tipos")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--saida", type=Path, help="pasta de resultados; repetir a mesma pasta retoma de onde parou")
    r.add_argument("--itens", nargs="+", default=list(ITENS))
    r.add_argument("--ec-janelas", type=int, default=36, help="janelas por documento (todas, se o documento tiver menos)")
    r.add_argument("--encadeamentos", type=Path, default=ENCADEAMENTOS,
                   help="rodada com combinacoes/ e relacoes/ (padrão: piloto de dificuldade v2)")
    r.add_argument("--limite-compostas", type=int, help="usa só os N primeiros encadeamentos de cada documento")
    r.add_argument("--piloto", type=Path, default=ENCADEAMENTOS,
                   help="piloto com questoes_avaliadas.csv a reclassificar por tipo")
    r.add_argument("--workers", type=int, default=6)
    r.add_argument("--etapas", nargs="+", choices=ETAPAS, default=list(ETAPAS))
    for papel, padrao in MODELOS.items():
        r.add_argument(f"--modelo-{papel}", default=padrao, help=f"deployment[:esforço] (padrão {padrao})")
    rel = sub.add_parser("relatorio")
    rel.add_argument("saida", type=Path)
    rel.add_argument("--piloto", type=Path, default=ENCADEAMENTOS)
    a = ap.parse_args(argv)

    if a.cmd == "relatorio":
        cfg = read_json(a.saida / "config.json")
        g = Geracao(a.saida, itens=cfg["itens"], ec_janelas=cfg["ec_janelas"], modelos=cfg["modelos"],
                    encadeamentos=cfg["encadeamentos"] and Path(cfg["encadeamentos"]),
                    limite_compostas=cfg["limite_compostas"])
        g.relatorio(a.piloto)
        print(f"Relatório: {a.saida / 'RELATORIO.md'}")
        return 0

    saida = a.saida or QA / "relatorios" / f"geracao_tipos_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"
    g = Geracao(saida, itens=a.itens, ec_janelas=a.ec_janelas, encadeamentos=a.encadeamentos,
                limite_compostas=a.limite_compostas, workers=a.workers,
                modelos={p: getattr(a, f"modelo_{p}") for p in MODELOS})
    print(f"Saída: {saida}\nEncadeamentos: {a.encadeamentos}\nModelos: {g.modelos}", flush=True)
    falhas = g.run(tuple(a.etapas), piloto=a.piloto)
    print(f"\nRelatório: {saida / 'RELATORIO.md'}")
    if falhas:
        print(f"{falhas} unidades falharam; rode de novo com --saida {saida} para tentar só elas.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
