"""CLI da geração híbrida por tipo de questão.

  python -m pipeline.qa_research.geracao_tipos run [opções]       reclassificação, janelas, compostas, auditoria
  python -m pipeline.qa_research.geracao_tipos relatorio <pasta>  refaz só o relatório
  python -m pipeline.qa_research.geracao_tipos meta [opções]      v17: gera e audita até N válidas por tópico
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from .core import ENCADEAMENTOS, ITENS, MODELOS, QA, Geracao, read_json

ETAPAS = ("reclassificar", "janelas", "compostas", "auditoria", "relatorio")
# Um tópico por área (02_02 fica de fora: os exemplos curados saíram dele).
ITENS_META = ("01_01", "02_03", "03_01", "04_02", "05_02", "06_05", "07_04", "08_03", "09_02", "10_01")


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
                   help="piloto com questoes_avaliadas.csv a reclassificar por tipo (etapa reclassificar)")
    r.add_argument("--exemplos", type=Path, help="banco de exemplos e contraexemplos (padrão: geracao_tipos/exemplos.json)")
    r.add_argument("--workers", type=int, default=6)
    r.add_argument("--etapas", nargs="+", choices=ETAPAS, default=[e for e in ETAPAS if e != "reclassificar"],
                   help="reclassificar (as questões do piloto v2) só roda se pedida")
    for papel, padrao in MODELOS.items():
        r.add_argument(f"--modelo-{papel}", default=padrao, help=f"deployment[:esforço] (padrão {padrao})")
    rel = sub.add_parser("relatorio")
    rel.add_argument("saida", type=Path)
    rel.add_argument("--piloto", type=Path, default=ENCADEAMENTOS)
    mt = sub.add_parser("meta")
    mt.add_argument("--saida", type=Path, help="pasta de resultados; repetir a mesma pasta retoma de onde parou")
    mt.add_argument("--itens", nargs="+", default=list(ITENS_META),
                    help="tópicos (padrão: um por área); use 'todos' para os 40")
    mt.add_argument("--meta", type=int, default=100, help="questões válidas por tópico")
    mt.add_argument("--max-rodadas", type=int, default=4)
    mt.add_argument("--max-passagens", type=int, default=3, help="vezes que a mesma janela pode ser usada")
    mt.add_argument("--reusar", type=Path, nargs="+", default=None,
                    help="rodadas com relações e encadeamentos a reaproveitar (padrão: geracao_meta v16 e piloto v2)")
    mt.add_argument("--banco-inicial", type=Path, nargs="*", default=None,
                    help="banco_dinamico.json herdados (padrão: o da geracao_meta v16); vazio para começar do zero")
    mt.add_argument("--exemplos", type=Path, help="banco curado (padrão: geracao_tipos/exemplos.json)")
    mt.add_argument("--workers", type=int, default=8)
    mt.add_argument("--relatorio", action="store_true", help="só refaz o relatório da pasta")
    a = ap.parse_args(argv)

    if a.cmd == "meta":
        from .rodadas import MODELOS as MODELOS_META
        from .rodadas import BANCO_INICIAL, REUSAR, GeracaoMeta
        from pipeline.qa_research.piloto_janela.core import PROGRAMA
        itens = ([r["id"] for r in read_json(PROGRAMA)["items"]] if a.itens == ["todos"] else a.itens)
        saida = a.saida or QA / "relatorios" / f"geracao_meta_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"
        kw = {"exemplos": a.exemplos} if a.exemplos else {}
        g = GeracaoMeta(saida, itens, meta=a.meta, max_rodadas=a.max_rodadas, max_passagens=a.max_passagens,
                        reusar=a.reusar or REUSAR, workers=a.workers,
                        banco_inicial=BANCO_INICIAL if a.banco_inicial is None else a.banco_inicial, **kw)
        if a.relatorio:
            g.relatorio()
            print(f"Relatório: {saida / 'RELATORIO.md'}")
            return 0
        print(f"Saída: {saida}\nTópicos: {itens}\nMeta: {a.meta} válidas por tópico\nModelos: {MODELOS_META}", flush=True)
        falhas = g.run()
        print(f"\nRelatório: {saida / 'RELATORIO.md'}")
        if falhas:
            print(f"{falhas} unidades falharam; rode de novo com --saida {saida} para tentar só elas.")
            return 2
        return 0

    if a.cmd == "relatorio":
        cfg = read_json(a.saida / "config.json")
        g = Geracao(a.saida, itens=cfg["itens"], ec_janelas=cfg["ec_janelas"], modelos=cfg["modelos"],
                    encadeamentos=cfg["encadeamentos"] and Path(cfg["encadeamentos"]),
                    limite_compostas=cfg["limite_compostas"])
        g.relatorio(a.piloto if (a.saida / "reclassificacao").exists() else None)
        print(f"Relatório: {a.saida / 'RELATORIO.md'}")
        return 0

    saida = a.saida or QA / "relatorios" / f"geracao_tipos_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"
    g = Geracao(saida, itens=a.itens, ec_janelas=a.ec_janelas, encadeamentos=a.encadeamentos,
                limite_compostas=a.limite_compostas, workers=a.workers, **({"exemplos": a.exemplos} if a.exemplos else {}),
                modelos={p: getattr(a, f"modelo_{p}") for p in MODELOS})
    print(f"Saída: {saida}\nEncadeamentos: {a.encadeamentos}\nModelos: {g.modelos}", flush=True)
    falhas = g.run(tuple(a.etapas), piloto=a.piloto if "reclassificar" in a.etapas else None)
    print(f"\nRelatório: {saida / 'RELATORIO.md'}")
    if falhas:
        print(f"{falhas} unidades falharam; rode de novo com --saida {saida} para tentar só elas.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
