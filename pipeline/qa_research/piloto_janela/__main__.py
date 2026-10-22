"""CLI do piloto de geração por janela.

  python -m pipeline.qa_research.piloto_janela run [opções]          uma condição
  python -m pipeline.qa_research.piloto_janela experimento [opções]  condições A, B, C e D
  python -m pipeline.qa_research.piloto_janela modos [opções]        junto x separado (condição C)
  python -m pipeline.qa_research.piloto_janela resumo <pasta>
  python -m pipeline.qa_research.piloto_janela comparar <pasta do experimento>
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from .core import DESCRICAO_MODOS, MODOS, PROMPT_JUNTO, QA, SEM_PREFERENCIA, Piloto, comparar, resumir


def _comuns(p: argparse.ArgumentParser) -> None:
    p.add_argument("--itens", nargs="+", default=["01_01", "02_02"])
    p.add_argument("--saida", type=Path, help="pasta de resultados; repetir a mesma pasta retoma de onde parou")
    p.add_argument("--modelo", default="gpt-5-4-petrobras:high", help="deployment:esforço")
    p.add_argument("--min", dest="minimo", type=int, default=6)
    p.add_argument("--max", dest="maximo", type=int, default=8)
    p.add_argument("--max-tokens", type=int, default=16000)
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--limite", type=int, help="processa só os N primeiros focos de cada item (teste rápido)")
    p.add_argument("--orientacao", default=SEM_PREFERENCIA, help="texto de <orientacao_dificuldade>")
    p.add_argument("--anteriores", type=Path, help="pasta de uma rodada anterior, para <questoes_existentes>")
    p.add_argument("--dry-run", action="store_true", help="só grava os prompts, sem chamar o modelo")


def _piloto(a, saida: Path, condicao: str, janelas_por_item, modo: str = "junto", min_dificeis: int = 0,
            **kw) -> Piloto:
    return Piloto(saida, a.itens, a.modelo, minimo=a.minimo, maximo=a.maximo, max_tokens=a.max_tokens,
                  orientacao=a.orientacao, anteriores=a.anteriores, workers=a.workers, limite=a.limite,
                  dry_run=a.dry_run, condicao=condicao, janelas_por_item=janelas_por_item, modo=modo,
                  min_dificeis=min_dificeis, **kw)


def _pendentes(pasta: Path) -> int:
    return len(list(pasta.glob("**/falhas/*.json")))


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="piloto_janela")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="gera questões numa condição")
    _comuns(r)
    r.add_argument("--condicao", default="A", choices=["A", "B", "C", "D"])
    r.add_argument("--janelas-por-item", type=int, help="usa N focos espaçados ao longo de cada documento")
    r.add_argument("--modo", default="junto", choices=list(MODOS))
    r.add_argument("--min-dificeis", type=int, default=0)
    e = sub.add_parser("experimento", help="roda as condições nas mesmas janelas e compara")
    _comuns(e)
    e.add_argument("--condicoes", nargs="+", default=["A", "B", "C", "D"], choices=["A", "B", "C", "D"])
    e.add_argument("--janelas-por-item", type=int, default=20)
    m = sub.add_parser("modos", help="planejamento e redação juntos x separados, nas mesmas janelas")
    _comuns(m)
    m.set_defaults(minimo=4, maximo=4)
    m.add_argument("--min-dificeis", type=int, default=1)
    m.add_argument("--condicao", default="C", choices=["A", "B", "C", "D"])
    m.add_argument("--modos", nargs="+", default=list(MODOS), choices=list(MODOS))
    m.add_argument("--janelas-por-item", type=int, default=20)
    s = sub.add_parser("resumo", help="recalcula resumo e exportações de uma pasta")
    s.add_argument("pasta", type=Path)
    c = sub.add_parser("comparar", help="recalcula a comparação de um experimento")
    c.add_argument("pasta", type=Path)
    a = p.parse_args(argv)

    if a.cmd == "resumo":
        resumir(a.pasta)
        print((a.pasta / "RESUMO.md").read_text(encoding="utf-8"))
        return 0
    if a.cmd == "comparar":
        comparar(a.pasta)
        print((a.pasta / "COMPARACAO.md").read_text(encoding="utf-8"))
        return 0

    agora = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if a.cmd == "run":
        saida = a.saida or QA / "relatorios" / f"piloto_janela_{agora}"
        kw = {"prompt": PROMPT_JUNTO} if (a.min_dificeis or a.modo == "separado") else {}
        _piloto(a, saida, a.condicao, a.janelas_por_item, a.modo, a.min_dificeis, **kw).run()
        if a.dry_run:
            return 0
        print((saida / "RESUMO.md").read_text(encoding="utf-8"))
    elif a.cmd == "modos":
        saida = a.saida or QA / "relatorios" / f"experimento_modos_{agora}"
        pilotos = [(modo, _piloto(a, saida / modo, a.condicao, a.janelas_por_item, modo, a.min_dificeis,
                                  prompt=PROMPT_JUNTO)) for modo in a.modos]
        for modo, piloto in pilotos:   # valida prompts e exemplos de todos antes de gastar chamadas
            piloto._prompts()
            piloto._carregar_exemplos()
        for modo, piloto in pilotos:
            print(f"\n=== Modo {modo}: {DESCRICAO_MODOS[modo]} ===", flush=True)
            piloto.run()
        if a.dry_run:
            return 0
        comparar(saida, a.modos, titulo="Experimento de modos: planejamento e redação juntos x separados")
        print((saida / "COMPARACAO.md").read_text(encoding="utf-8"))
    else:
        saida = a.saida or QA / "relatorios" / f"experimento_exemplos_{agora}"
        pilotos = [(cond, _piloto(a, saida / cond, cond, a.janelas_por_item)) for cond in a.condicoes]
        for cond, piloto in pilotos:   # carrega os exemplos de todas antes de gastar chamadas
            piloto._carregar_exemplos()
        for cond, piloto in pilotos:
            print(f"\n=== Condição {cond} ===", flush=True)
            piloto.run()
        if a.dry_run:
            return 0
        comparar(saida, a.condicoes)
        print((saida / "COMPARACAO.md").read_text(encoding="utf-8"))
    if _pendentes(saida):
        print(f"{_pendentes(saida)} janelas falharam; rode o mesmo comando com --saida {saida} para tentar só essas.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
