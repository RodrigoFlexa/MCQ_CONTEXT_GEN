"""CLI do piloto de dificuldade v2 (inventário x EC v13, avaliação cega).

  python -m pipeline.qa_research.inventario_docs run [opções]       todas as etapas (retomável)
  python -m pipeline.qa_research.inventario_docs relatorio <pasta>  refaz só o relatório
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from .core import ITENS, MODELOS, QA, RESPONDENTES, Piloto, read_json

ETAPAS = ("relacoes", "combinacoes", "questoes", "ec", "avaliar", "relatorio")
V1 = QA / "relatorios" / "piloto_inventario_20261023T042252Z"   # relações e acurácias da rodada v1


def _de_config(saida: Path) -> dict:
    cfg = read_json(saida / "config.json")
    return dict(itens=cfg["itens"], faceis=None, medias=None, dificeis=None, reserva=cfg["reserva"],
                ec_janelas=cfg["ec_janelas"], modelos=cfg["modelos"], respondentes=cfg["respondentes"],
                combinacoes_por_doc=cfg["combinacoes_por_doc"], sem_exemplos=cfg["sem_exemplos"],
                limite_blocos=cfg["limite_blocos"], reusar=cfg["reusar"], historico=cfg["historico"],
                cotas=cfg["cotas"])


def _piloto(saida: Path, cotas: dict | None = None, **kw) -> Piloto:
    if cotas:   # retomada: as cotas gravadas mandam
        um = next(iter(cotas.values()))
        kw.update(faceis=um["facil"], medias=um["media"])
        kw["dificeis"] = None
    p = Piloto(saida, **{k: v for k, v in kw.items() if v is not None})
    if cotas:
        p.cotas = cotas
    return p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.qa_research.inventario_docs")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--saida", type=Path, help="pasta de resultados; repetir a mesma pasta retoma de onde parou")
    r.add_argument("--itens", nargs="+", default=list(ITENS))
    r.add_argument("--faceis", type=int, default=10, help="fáceis por documento e método")
    r.add_argument("--medias", type=int, default=10, help="médias por documento e método")
    r.add_argument("--dificeis", type=int, help="difíceis por documento (padrão: uma por janela EC)")
    r.add_argument("--ec-janelas", type=int, default=36, help="janelas EC por documento (todas, se o documento tiver menos)")
    r.add_argument("--reserva", type=float, default=1.0, help="alvos extras por célula, usados só se faltar questão")
    r.add_argument("--combinacoes", type=int, default=40, help="máximo de encadeamentos por documento")
    r.add_argument("--reusar", type=Path, help=f"rodada com relações a reaproveitar (padrão: {V1.name}, se existir)")
    r.add_argument("--workers", type=int, default=6)
    r.add_argument("--etapas", nargs="+", choices=ETAPAS, default=list(ETAPAS))
    r.add_argument("--sem-exemplos", action="store_true", help="gera as questões do inventário sem os exemplos EC")
    r.add_argument("--limite-blocos", type=int, help="usa só os N primeiros blocos de cada documento (teste rápido)")
    r.add_argument("--respondentes", nargs="+", default=list(RESPONDENTES), help="deployment[:esforço] de cada respondente")
    for papel, padrao in MODELOS.items():
        r.add_argument(f"--modelo-{papel}", default=padrao, help=f"deployment[:esforço] (padrão {padrao})")
    rel = sub.add_parser("relatorio")
    rel.add_argument("saida", type=Path)
    a = ap.parse_args(argv)

    if a.cmd == "relatorio":
        p = _piloto(a.saida, **_de_config(a.saida))
        p.relatorio()
        print(f"Relatório: {a.saida / 'RELATORIO.md'}")
        return 0

    saida = a.saida or QA / "relatorios" / f"piloto_dificuldade_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"
    if (saida / "config.json").exists():
        print(f"Retomando {saida} com a configuração gravada.", flush=True)
        p = _piloto(saida, workers=a.workers, **_de_config(saida))
    else:
        reusar = a.reusar or (V1 if (V1 / "relacoes").exists() else None)
        historico = V1 if (V1 / "resultado.json").exists() else None
        p = _piloto(saida, itens=a.itens, faceis=a.faceis, medias=a.medias, dificeis=a.dificeis, ec_janelas=a.ec_janelas,
                    reserva=a.reserva, combinacoes_por_doc=a.combinacoes, reusar=reusar, historico=historico,
                    workers=a.workers, sem_exemplos=a.sem_exemplos, limite_blocos=a.limite_blocos,
                    respondentes=a.respondentes, modelos={papel: getattr(a, f"modelo_{papel}") for papel in MODELOS})
    print(f"Saída: {saida}\nCotas por documento: {p.cotas}\nReaproveitando relações de: {p.reusar}\n"
          f"Modelos: {p.modelos}\nRespondentes: {p.respondentes}", flush=True)
    falhas = p.run(tuple(a.etapas))
    print(f"\nRelatório: {saida / 'RELATORIO.md'}")
    if falhas:
        print(f"{falhas} unidades falharam ou ficaram pendentes; rode de novo com --saida {saida} para tentar só elas.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
