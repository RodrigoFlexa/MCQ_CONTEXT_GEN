"""CLI do experimento A/B. Uso: python -m pipeline.qa_research.experimento_ab <comando> [opções]

  plano                 mostra braços, documentos e volume previsto (sem API)
  preparar              copia os documentos antigo/refinado para a pasta do experimento (sem API)
  calibrar              etapa 0: embeddings, pares rotulados, AUC, limiares e juiz da deduplicação
  gerar --braco A       etapas 1-2: geração v21 do braço (A, B, C ou D); C e D exigem A e B prontos
  avaliar --braco A     etapa 3: gap com/sem contexto (GPT-4.1 Nano/Mini/4.1) e sustentação dos gabaritos
  comparar              tabela 2x2 com efeitos e IC 95% (COMPARACAO.md)
  sustentacao --braco B etapa 4: checagem de sustentação + resposta mínima sobre as questões do braço (B_sust)

Repetir qualquer comando com a mesma pasta retoma de onde parou; nada já concluído é refeito.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from pipeline.qa_research.piloto_janela.core import atomic_json, blocos, read_json

from . import comum as C


def info_braco(nome: str) -> dict:
    base = nome.split("_")[0]
    if base not in C.BRACOS:
        raise SystemExit(f"Braço inválido: {nome} (use A, B, C, D ou <braço>_sust)")
    return {**C.BRACOS[base], "base": base, "sustentacao": nome.endswith("_sust")}


def _calibracao(exp: Path) -> Path:
    arq = exp / "calibracao" / "calibracao.json"
    if not arq.exists():
        raise SystemExit(f"Falta a calibração ({arq}). Rode antes: calibrar")
    return arq


def _gerador(exp: Path, nome: str, workers: int, dedup: str):
    from .geracao import GeracaoAB
    info = info_braco(nome)
    docs = C.docs_do_braco(exp, info["base"])
    if not (exp / "docs" / "manifesto.json").exists():
        raise SystemExit("Documentos não preparados. Rode antes: preparar")
    reusar = []
    if info["reusar"] and not info["sustentacao"]:
        origem = exp / "bracos" / info["reusar"]
        faltam = [i for i in C.ITENS if not (origem / "topicos" / i / "combinacoes.json").exists()]
        if faltam:
            raise SystemExit(f"O braço {nome} reaproveita o inventário de {info['reusar']} (mesmo documento), que ainda "
                             f"não terminou para {faltam}. Rode antes: gerar --braco {info['reusar']}")
        reusar = [origem]
    return GeracaoAB(exp / "bracos" / nome, C.ITENS, docs=docs, unidade=info["unidade"], braco=nome, reusar=reusar,
                     calibracao=_calibracao(exp) if dedup == "incremental" else None, dedup=dedup,
                     sustentacao=info["sustentacao"], workers=workers)


def plano(exp: Path) -> None:
    print(f"Experimento: {C.relativo(exp)}")
    print(f"Documentos: {', '.join(C.ITENS)} (fonte {C.relativo(C.FONTE_DOCS)})")
    for b, info in C.BRACOS.items():
        docs = C.FONTE_DOCS / info["docs"]
        n = sum(len(blocos(i, docs)[1]) for i in C.ITENS)
        print(f"  {b}: documento {info['docs']:8s} | unidade {info['unidade']:8s} | {n} focos (1 chamada cada) | "
              f"até 25 compostas por documento | inventário " + (f"de {info['reusar']}" if info["reusar"] else "novo"))
    print("Etapa 0 (calibração): embeddings 3-small e 3-large das 2.818 questões; ~170 pares x (referência + 3 juízes).")
    print("Etapa 3 (avaliação): por braço, 2 condições x 3 modelos + juiz + 1 auditoria de sustentação por questão.")
    print("Sem chamadas de API neste comando.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.qa_research.experimento_ab", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("comando", choices=["plano", "preparar", "calibrar", "gerar", "avaliar", "comparar", "sustentacao"])
    ap.add_argument("--experimento", type=Path, default=C.EXPERIMENTO)
    ap.add_argument("--braco")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--judge-workers", type=int, default=2)
    ap.add_argument("--dedup", choices=["incremental", "llm"], default="incremental")
    ap.add_argument("--por-faixa", type=int, default=8, help="calibração: pares sorteados por faixa de cosseno e modelo")
    ap.add_argument("--recalcular", action="store_true", help="calibração: só recalcula (usa rotulos_humanos.csv)")
    ap.add_argument("--mini-deployment", default="gpt-4-1-mini-petrobras")
    a = ap.parse_args(argv)
    exp = a.experimento if a.experimento.is_absolute() else C.ROOT / a.experimento

    if a.comando == "plano":
        plano(exp)
        return 0
    if a.comando == "preparar":
        m = C.preparar_documentos(exp)
        for k, v in m["documentos"].items():
            print(f"  {k}: {v['blocos']} blocos, {v['capitulos']} capítulos, {v['palavras']} palavras")
        return 0
    if a.comando == "calibrar":
        from .calibracao import Calibracao
        falhas = Calibracao(exp / "calibracao", por_faixa=a.por_faixa, workers=a.workers).run(recalcular=a.recalcular)
        print(f"Resumo: {C.relativo(exp / 'calibracao' / 'CALIBRACAO.md')}")
        if falhas:
            print(f"{falhas} rótulos falharam; repita o comando para tentar só eles.")
        return 2 if falhas else 0
    if a.comando == "comparar":
        from .metricas import comparar
        emb = media = None
        cal = exp / "calibracao" / "calibracao.json"
        if cal.exists():
            import numpy as np
            c = read_json(cal)
            emb = C.embedder(c["embedding"], exp / "calibracao")
            media = np.asarray(read_json(exp / "calibracao" / c["media"]), dtype=float)
        comparar(exp, embedder=emb, media_vec=media)
        print(f"Tabela: {C.relativo(exp / 'COMPARACAO.md')}")
        return 0
    if not a.braco:
        raise SystemExit("Informe --braco")
    if a.comando == "gerar":
        g = _gerador(exp, a.braco, a.workers, a.dedup)
        falhas = g.run()
        if falhas:
            print(f"[{a.braco}] {falhas} unidades falharam (isoladas; as demais foram salvas). Repita o mesmo comando "
                  "para tentar só elas.")
            return 2
        print(f"[{a.braco}] geração concluída: {C.relativo(exp / 'bracos' / a.braco / 'RELATORIO.md')}")
        return 0
    if a.comando == "sustentacao":
        origem, nome = exp / "bracos" / a.braco, a.braco + "_sust"
        if not (origem / "geracao_concluida.json").exists():
            raise SystemExit(f"O braço {a.braco} ainda não concluiu a geração")
        destino = exp / "bracos" / nome
        if not destino.exists():   # cópia: mesmas questões e caches; decisões de deduplicação são refeitas
            shutil.copytree(origem, destino, ignore=shutil.ignore_patterns(
                "dedup_incremental", "geracao_concluida.json", "aprovadas.jsonl", "finalizado.json", "resultado.json",
                "config.json", "RELATORIO.md"))
        g = _gerador(exp, nome, a.workers, a.dedup)
        g.config()
        cfg = read_json(destino / "config.json")
        atomic_json(destino / "config.json", {**cfg, "origem": C.relativo(origem)})
        falhas = g.run()
        if falhas:
            print(f"[{nome}] {falhas} unidades falharam; repita o mesmo comando.")
            return 2
        print(f"[{nome}] concluído: {C.relativo(destino / 'resultado.json')}. Avalie com: avaliar --braco {nome}")
        return 0
    if a.comando == "avaliar":
        from .avaliacao import executar
        st = executar(exp / "bracos" / a.braco, exp / "avaliacao" / a.braco, workers=a.workers,
                      judge_workers=a.judge_workers, mini=a.mini_deployment)
        print(f"[{a.braco}] avaliação {'concluída' if st == 0 else 'incompleta; repita o mesmo comando'}")
        return st
    return 1


if __name__ == "__main__":
    sys.exit(main())
