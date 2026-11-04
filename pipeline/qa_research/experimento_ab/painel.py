"""Painel de dificuldade empírica: as mesmas questões, sem contexto, respondidas por modelos mais fortes que o GPT-4.1.

Usa o mesmo motor, respondente (até 100 palavras) e juiz do benchmark_gap, só na condição sem contexto. Junta os
vereditos do painel aos do GPT-4.1 Nano, Mini e 4.1 já avaliados na pasta de origem e classifica cada questão:
  facil         todos os modelos acertam
  media         o GPT-5.4 acerta, mas algum outro erra
  dificil       o GPT-5 não acerta (parcial ou incorreta)
  muito_dificil nenhum modelo independente acerta (o GPT-5.4, que gerou as questões, fica fora dos estratos)
A dificuldade é empírica (acerto de modelos), não um rótulo do gerador. Funciona para qualquer pasta de avaliação
com questoes.jsonl e pares.csv (braços do experimento A/B ou benchmark_gap do banco antigo).
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research import benchmark_gap as G

from . import comum as C

# GPT-5.4 gera, audita e julga as questões: entra no painel só como referência (tende a acertar o que ele mesmo
# escreveu). Os estratos usam o GPT-5, modelo forte que não participou da construção do dataset.
PAINEL = {"gpt-5-nano": "gpt-5-nano-petrobras:low", "gpt-5-mini": "gpt-5-mini-petrobras:low",
          "gpt-5": "gpt-5-petrobras:low", "gpt-5-4": "gpt-5-4-petrobras:low"}
BASE = ("gpt-4-1-nano", "gpt-4-1-mini", "gpt-4-1")
FORTE = "gpt-5"
NAO_INDEPENDENTES = ("gpt-5-4",)
ESTRATOS = ("facil", "media", "dificil", "muito_dificil")


def estrato(vs: dict) -> str:
    vs = {m: v for m, v in vs.items() if m not in NAO_INDEPENDENTES}
    if all(v != "correta" for v in vs.values()):
        return "muito_dificil"
    if vs.get(FORTE) != "correta":
        return "dificil"
    return "facil" if all(v == "correta" for v in vs.values()) else "media"


def _base(aval: Path) -> dict:
    """uid original -> {modelo: veredito sem contexto} da avaliação de origem."""
    out: dict = {}
    with (aval / "pares.csv").open(encoding="utf-8-sig") as f:
        for r in csv.DictReader(C.sem_nul(f)):
            out.setdefault(r["uid"], {})[r["modelo"]] = r["veredito_closed_book"]
    return out


def executar(aval: Path, modelos: dict | None = None, workers: int = 8, judge_workers: int = 2, clientes=None,
             progress=print) -> int:
    aval = Path(aval)
    if not (aval / "rodada_concluida.json").exists():
        raise ValueError(f"{aval}: avaliação principal ainda não concluída")
    modelos = modelos or PAINEL
    saida = aval / "painel"
    rows = [q for q in C.linhas(aval / "questoes.jsonl") if q["condicao"] == "closed_book"]
    cfg = {"schema": "experimento-ab-painel-v1", "origem": C.relativo(aval), "modelos": modelos, "juiz": G.Q.JUIZ,
           "condicao": "closed_book", "limite_palavras": 100, "questoes_sha256": C.sha(rows),
           "prompts": {n: C.sha(G.prompt(n)) for n in ("respondente", "juiz")}}
    with output_lock(saida):
        old = read_json(saida / "config.json")
        if old is not None and {k: v for k, v in old.items() if k != "modelos"} == \
                {k: v for k, v in cfg.items() if k != "modelos"} and old["modelos"].items() <= cfg["modelos"].items():
            old = cfg      # painel ampliado com modelos novos: as respostas já salvas são mantidas
        if old is not None and old != cfg:
            raise ValueError("Painel com protocolo ou questões diferentes nesta pasta; apague painel/ ou use outra")
        atomic_json(saida / "config.json", cfg)
        G.Q.C.GeracaoSemConteudo.jsonl(saida / "questoes.jsonl", rows)
        d = saida / "avaliacao"
        for m in modelos:
            for sub in ("respostas", "juiz"):
                (d / sub / m).mkdir(parents=True, exist_ok=True)
        (d / "falhas").mkdir(exist_ok=True)
        e = G.AvaliacaoGap(saida, respondentes=modelos, juiz=G.Q.JUIZ, grupos=[tuple(modelos)], workers=workers,
                           judge_workers=judge_workers, lote_juiz=8, clientes=clientes, progress=progress)
        try:
            e.run()
        finally:
            for c in e.clientes.values():
                if hasattr(c, "close"):
                    c.close()
        completo = all(len(e.vereditos[m]) == len(rows) for m in modelos)
        base = _base(aval)
        linhas = []
        for q in rows:
            u = q["uid"].split(":", 1)[1]
            vs = {m: base.get(u, {}).get(m) for m in BASE} | {m: e.vereditos[m].get(q["uid"]) for m in modelos}
            if any(v is None for v in vs.values()):
                continue
            p = sum(1 if v == "correta" else .5 if v == "parcial" else 0 for v in vs.values()) / len(vs)
            linhas.append({"uid": u, "item": q["item"], "tipo": q["tipo"], **{f"v_{m}": v for m, v in vs.items()},
                           "p_acerto": round(p, 3), "estrato": estrato(vs)})
        if linhas:
            with (saida / "dificuldade.csv").open("w", encoding="utf-8-sig", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(linhas[0]))
                w.writeheader()
                w.writerows(linhas)
        resumo = resumir(linhas, (*BASE, *modelos))
        atomic_json(saida / "resumo.json", {**resumo, "completo": completo})
        progress(f"[painel] {C.relativo(saida)}: {resumo['estratos']} | acurácia sem contexto {resumo['acuracia']}",
                 flush=True)
        if completo:
            atomic_json(saida / "painel_concluido.json", {"questoes": len(rows)})
        return 0 if completo else 2


def resumir(linhas: list, modelos) -> dict:
    n = len(linhas)
    acc = {m: round(100 * sum(r[f"v_{m}"] == "correta" for r in linhas) / n, 1) if n else None for m in modelos}
    est = Counter(r["estrato"] for r in linhas)
    por_tipo = {}
    for t in sorted({r["tipo"] for r in linhas}):
        rs = [r for r in linhas if r["tipo"] == t]
        por_tipo[t] = {"n": len(rs), "dificil_ou_mais": round(100 * sum(r["estrato"] in ("dificil", "muito_dificil")
                                                                        for r in rs) / len(rs), 1)}
    return {"n": n, "acuracia": acc, "estratos": {e: est.get(e, 0) for e in ESTRATOS},
            "estratos_pct": {e: round(100 * est.get(e, 0) / n, 1) if n else None for e in ESTRATOS}, "por_tipo": por_tipo}
