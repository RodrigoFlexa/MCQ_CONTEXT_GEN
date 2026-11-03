"""CLI do experimento A/B. Uso: python -m pipeline.qa_research.experimento_ab <comando> [opções]

  plano                 mostra braços, documentos e volume previsto (sem API)
  preparar              copia os documentos antigo/refinado para a pasta do experimento (sem API)
  calibrar              etapa 0: embeddings, pares rotulados, AUC, limiares e juiz da deduplicação
  gerar --braco A       etapas 1-2: geração v21 do braço (A, B, C ou D); C e D exigem A e B prontos
  avaliar --braco A     etapa 3: gap com/sem contexto (GPT-4.1 Nano/Mini/4.1) e sustentação dos gabaritos
  comparar              tabela 2x2 com efeitos e IC 95% (COMPARACAO.md)
  sustentacao --braco B etapa 4: checagem de sustentação + resposta mínima sobre as questões do braço (B_sust)
  saturar --braco D     rodadas extras por foco até saturar (D_sat), sobre a mesma 1ª rodada do braço
  v22 --braco B         gerador v22 (0 a 4 questões por foco, auditor por questão com o texto-fonte, sem refinador,
                        rodadas até saturar) com os documentos e o inventário de B (B_v22)

Braços derivados combinam sufixos: D_sat (saturação), D_sust (sustentação), D_sat_sust (os dois).

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
    partes = nome.split("_")
    base, sufixos = partes[0], partes[1:]
    if base not in C.BRACOS or any(s not in ("sat", "sust", "v22") for s in sufixos) or len(set(sufixos)) != len(sufixos):
        raise SystemExit(f"Braço inválido: {nome} (use A, B, C, D, <braço>_sat, <braço>_sust, <braço>_sat_sust ou "
                         "<braço>_v22)")
    sust = nome.endswith("_sust")
    return {**C.BRACOS[base], "base": base, "sustentacao": sust, "saturacao": "sat" in sufixos and not sust,
            "derivado": bool(sufixos)}


def _copiar_braco(origem: Path, destino: Path, manter_dedup: bool) -> None:
    """Cópia de um braço concluído: mesmas questões e caches (nenhuma chamada repetida)."""
    if not (origem / "geracao_concluida.json").exists():
        raise SystemExit(f"O braço {origem.name} ainda não concluiu a geração")
    if not destino.exists():
        ignorar = ["geracao_concluida.json", "aprovadas.jsonl", "finalizado.json", "resultado.json", "config.json",
                   "RELATORIO.md", "saturacao.json"] + ([] if manter_dedup else ["dedup_incremental"])
        shutil.copytree(origem, destino, ignore=shutil.ignore_patterns(*ignorar))


def _calibracao(exp: Path) -> Path:
    arq = exp / "calibracao" / "calibracao.json"
    if not arq.exists():
        raise SystemExit(f"Falta a calibração ({arq}). Rode antes: calibrar")
    return arq


def _gerador(exp: Path, nome: str, workers: int, dedup: str, saturacao: dict | None = None):
    from .geracao import GeracaoAB
    info = info_braco(nome)
    docs = C.docs_do_braco(exp, info["base"])
    if not (exp / "docs" / "manifesto.json").exists():
        raise SystemExit("Documentos não preparados. Rode antes: preparar")
    reusar = []
    if info["reusar"] and not info["derivado"]:
        origem = exp / "bracos" / info["reusar"]
        faltam = [i for i in C.ITENS if not (origem / "topicos" / i / "combinacoes.json").exists()]
        if faltam:
            raise SystemExit(f"O braço {nome} reaproveita o inventário de {info['reusar']} (mesmo documento), que ainda "
                             f"não terminou para {faltam}. Rode antes: gerar --braco {info['reusar']}")
        reusar = [origem]
    return GeracaoAB(exp / "bracos" / nome, C.ITENS, docs=docs, unidade=info["unidade"], braco=nome, reusar=reusar,
                     calibracao=_calibracao(exp) if dedup == "incremental" else None, dedup=dedup,
                     sustentacao=info["sustentacao"], saturacao=(saturacao or {}) if info["saturacao"] else None,
                     workers=workers)


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
    ap.add_argument("comando", choices=["plano", "preparar", "calibrar", "gerar", "avaliar", "comparar", "sustentacao",
                                        "saturar", "v22"])
    ap.add_argument("--experimento", type=Path, default=C.EXPERIMENTO)
    ap.add_argument("--braco")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--judge-workers", type=int, default=2)
    ap.add_argument("--dedup", choices=["incremental", "llm"], default="incremental")
    ap.add_argument("--por-faixa", type=int, default=8, help="calibração: pares sorteados por faixa de cosseno e modelo")
    ap.add_argument("--recalcular", action="store_true", help="calibração: só recalcula (usa rotulos_humanos.csv)")
    ap.add_argument("--mini-deployment", default="gpt-4-1-mini-petrobras")
    ap.add_argument("--max-rodadas", type=int, default=5, help="saturação: visitas máximas por foco (inclui a 1ª)")
    ap.add_argument("--paciencia", type=int, default=1, help="saturação: rodadas seguidas sem conhecimento novo para fechar")
    ap.add_argument("--onda", type=int, default=4, help="v22: focos gerados ao mesmo tempo em cada documento")
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
    sat = {"max_rodadas": a.max_rodadas, "paciencia": a.paciencia}
    if a.comando == "gerar":
        if info_braco(a.braco)["derivado"]:
            raise SystemExit("Braços derivados são criados com os comandos saturar ou sustentacao")
        g = _gerador(exp, a.braco, a.workers, a.dedup)
        falhas = g.run()
        if falhas:
            print(f"[{a.braco}] {falhas} unidades falharam (isoladas; as demais foram salvas). Repita o mesmo comando "
                  "para tentar só elas.")
            return 2
        print(f"[{a.braco}] geração concluída: {C.relativo(exp / 'bracos' / a.braco / 'RELATORIO.md')}")
        return 0
    if a.comando == "v22":
        from .v22 import GeracaoV22
        info = info_braco(a.braco)
        if info["derivado"]:
            raise SystemExit("Informe o braço de origem (A, B, C ou D); o v22 cria <braço>_v22")
        if info["unidade"] != "janela":
            raise SystemExit("O v22 usa a janela de 3 blocos (braços A ou B)")
        origem, nome = exp / "bracos" / a.braco, a.braco + "_v22"
        faltam = [i for i in C.ITENS if not (origem / "topicos" / i / "combinacoes.json").exists()]
        if faltam:
            raise SystemExit(f"O v22 reaproveita o inventário de {a.braco}, incompleto para {faltam}")
        g = GeracaoV22(exp / "bracos" / nome, C.ITENS, docs=C.docs_do_braco(exp, a.braco), braco=nome, reusar=[origem],
                       calibracao=_calibracao(exp), saturacao=sat, onda=a.onda, workers=a.workers)
        falhas = g.run()
        if falhas:
            print(f"[{nome}] {falhas} unidades falharam (isoladas; o resto está salvo). Repita o mesmo comando.")
            return 2
        print(f"[{nome}] geração concluída: {C.relativo(exp / 'bracos' / nome / 'RELATORIO.md')}")
        return 0
    if a.comando in ("sustentacao", "saturar"):
        sufixo = "_sust" if a.comando == "sustentacao" else "_sat"
        origem, nome = exp / "bracos" / a.braco, a.braco + sufixo
        destino = exp / "bracos" / nome
        info_braco(nome)
        # sustentação refaz as decisões de deduplicação (o gate remove questões antes dela); saturação as mantém,
        # porque as rodadas novas são comparadas com o banco da 1ª rodada
        _copiar_braco(origem, destino, manter_dedup=a.comando == "saturar")
        g = _gerador(exp, nome, a.workers, a.dedup, saturacao=sat)
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
        destino = exp / "avaliacao" / a.braco
        origem = exp / "avaliacao" / a.braco.rsplit("_", 1)[0]
        if info_braco(a.braco)["derivado"] and not destino.exists() and (origem / ".local").exists():
            # braço derivado: reaproveita o cache de chamadas da avaliação de origem (mesma pergunta e mesmo contexto
            # = mesma chamada; respostas e auditorias das questões em comum não são pagas de novo)
            shutil.copytree(origem / ".local", destino / ".local")
        st = executar(exp / "bracos" / a.braco, exp / "avaliacao" / a.braco, workers=a.workers,
                      judge_workers=a.judge_workers, mini=a.mini_deployment)
        print(f"[{a.braco}] avaliação {'concluída' if st == 0 else 'incompleta; repita o mesmo comando'}")
        return st
    return 1


if __name__ == "__main__":
    sys.exit(main())
