"""Calibração do "atalho" do auditor (relatorios/calibracao_atalho_v3).

O atalho (a resposta sai do enunciado) é a principal causa de reprovação da geração final v3: 5.204 das 12.454 questões
foram reprovadas só por ele, com tudo o mais aprovado. É um julgamento do GPT-5.4, e o mesmo conhecimento com redação
quase igual recebeu vereditos opostos. Este experimento mede o atalho pelo que importa para um benchmark: se a resposta
sai do enunciado, modelos menores acertam sem contexto.

Amostra estratificada por tipo (N_POR_GRUPO por grupo, semente fixa) de dois grupos da geração principal:
  atalho   reprovadas só por atalho, com gabarito curto;
  validas  válidas (controle).
Cada questão é respondida sem contexto, com resposta de até 20 palavras, por GPT-4.1 Mini e GPT-5 mini (os modelos
independentes mais fracos do painel), e julgada pelo juiz padrão. Se o atalho for real, as reprovadas por atalho têm
acerto bem maior que as válidas; se a diferença for pequena, o veredito de atalho é ruído em boa parte e as reprovadas
por ele merecem conserto ou reavaliação, não descarte.

python -m pipeline.qa_research.experimento_ab atalho-v3 [--amostra 300]
"""
from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research import benchmark_gap as G

from . import comum as C
from . import limite as LI
from .final_v3 import CONFIG, SAIDA as ORIGEM

SAIDA = C.QA / "relatorios" / "calibracao_atalho_v3"
N_POR_GRUPO = 300
MODELOS = {m: LI.MODELOS[m] for m in ("gpt-4-1-mini", "gpt-5-mini")}
SEMENTE = 20261122
LIMITE = 20


def amostrar(qs: list[dict], n: int, rng: random.Random) -> list[dict]:
    """n questões com os tipos na proporção do grupo (ao menos uma de cada tipo presente)."""
    por_tipo = defaultdict(list)
    for q in sorted(qs, key=lambda q: q["uid"]):
        por_tipo[q["tipo"] or "?"].append(q)
    total = len(qs)
    cotas = {t: max(1, round(n * len(v) / total)) for t, v in por_tipo.items()} if total else {}
    out = []
    for t, v in sorted(por_tipo.items()):
        out += rng.sample(v, min(cotas[t], len(v)))
    rng.shuffle(out)
    return out[:n]


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if not n:
        return (float("nan"), float("nan"))
    p = k / n
    c = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    m = (p + z * z / (2 * n)) / (1 + z * z / n)
    return (100 * (m - c), 100 * (m + c))


def executar(origem: Path = ORIGEM, saida: Path = SAIDA, *, n: int = N_POR_GRUPO, workers: int = 8,
             judge_workers: int = 2, clientes=None, leitor=None, exp: Path = C.EXPERIMENTO, progress=print) -> int:
    from .banco_v3 import Leitor
    saida = Path(saida)
    lt = leitor or Leitor(Path(origem), exp=exp, progress=progress)
    qs = lt.finais(CONFIG)
    grupos = {"atalho": [q for q in qs if not q["aprovada_auditor"] and q["resposta_curta"]
                         and set(q["auditoria"].get("falhas", [])) == {"atalho"}],
              "validas": [q for q in qs if q["valida"]]}
    rng = random.Random(SEMENTE)
    amostra = {g: amostrar(v, n, rng) for g, v in grupos.items()}
    rows = [{"uid": f"closed_book:{q['uid']}", "uid_original": q["uid"], "condicao": "closed_book", "grupo": g,
             "item": q["item"], "tipo": q["tipo"], "composicao": "simples", "pergunta": q["pergunta"],
             "resposta": q["resposta"], "contexto_tecnico": None}
            for g, lst in amostra.items() for q in lst]
    cfg = {"schema": "calibracao-atalho-v3", "origem": C.relativo(Path(origem)), "n_por_grupo": n, "semente": SEMENTE,
           "modelos": MODELOS, "juiz": G.Q.JUIZ, "limite_palavras": LIMITE, "questoes_sha256": C.sha(rows),
           "prompts": {"respondente": C.sha(LI.prompt_curta(LIMITE)), "juiz": C.sha(G.prompt("juiz"))}}
    saida.mkdir(parents=True, exist_ok=True)
    (saida / ".gitignore").write_text(".local/\nchamadas/\navaliacao/\n", encoding="utf-8")
    with output_lock(saida):
        old = read_json(saida / "config.json")
        if old is not None and old != cfg:
            raise ValueError(f"Calibração com outra amostra ou protocolo em {C.relativo(saida)}; apague a pasta")
        atomic_json(saida / "config.json", cfg)
        G.Q.C.GeracaoSemConteudo.jsonl(saida / "questoes.jsonl", rows)
        d = saida / "avaliacao"
        for m in MODELOS:
            for sub in ("respostas", "juiz"):
                (d / sub / m).mkdir(parents=True, exist_ok=True)
        (d / "falhas").mkdir(exist_ok=True)
        LI.AvaliacaoCurta.limite = LIMITE
        e = LI.AvaliacaoCurta(saida, respondentes=MODELOS, juiz=G.Q.JUIZ, grupos=[tuple(MODELOS)], workers=workers,
                              judge_workers=judge_workers, lote_juiz=8, clientes=clientes, progress=progress)
        try:
            e.run()
        finally:
            for c in e.clientes.values():
                if hasattr(c, "close"):
                    c.close()
        completo = all(r["uid"] in e.vereditos[m] for m in MODELOS for r in rows)
        res = resumir(rows, e.vereditos, {g: len(v) for g, v in grupos.items()})
        res["completo"] = completo
        atomic_json(saida / "resumo.json", res)
        (saida / "ATALHO.md").write_text(markdown(res), encoding="utf-8")
        progress(f"[atalho] {C.relativo(saida / 'ATALHO.md')}: " + "; ".join(
            f"{m} atalho {res['acuracia'][m]['atalho']['pct']:.0f}% x válidas {res['acuracia'][m]['validas']['pct']:.0f}%"
            for m in MODELOS), flush=True)
        return 0 if completo else 2


def resumir(rows: list[dict], vereditos: dict, populacao: dict) -> dict:
    acc, por_tipo = {}, {}
    for m in MODELOS:
        acc[m], por_tipo[m] = {}, {}
        for g in ("atalho", "validas"):
            rs = [r for r in rows if r["grupo"] == g and vereditos[m].get(r["uid"]) in ("correta", "parcial", "incorreta")]
            k = sum(vereditos[m][r["uid"]] == "correta" for r in rs)
            lo, hi = wilson(k, len(rs))
            acc[m][g] = {"n": len(rs), "corretas": k, "pct": 100 * k / len(rs) if rs else float("nan"), "ic95": [lo, hi]}
            por_tipo[m][g] = {t: round(100 * sum(vereditos[m][r["uid"]] == "correta" for r in rt) / len(rt), 1)
                              for t in sorted({r["tipo"] for r in rs})
                              for rt in [[r for r in rs if r["tipo"] == t]]}
    dif = {m: acc[m]["atalho"]["pct"] - acc[m]["validas"]["pct"] for m in MODELOS}
    leitura = ("O atalho apontado pelo auditor é real: as reprovadas por ele são bem mais fáceis para os modelos menores; "
               "o conserto deve tirar do enunciado o que entrega a resposta." if min(dif.values()) >= 15 else
               "O atalho apontado pelo auditor separa pouco: as reprovadas por ele não são muito mais fáceis que as válidas "
               "para os modelos menores; boa parte é ruído de julgamento e merece conserto ou reavaliação, não descarte.")
    return {"populacao": populacao, "amostra": dict(Counter(r["grupo"] for r in rows)), "acuracia": acc,
            "por_tipo": por_tipo, "diferenca_pp": dif, "leitura": leitura}


def markdown(r: dict) -> str:
    f = lambda v: "-" if v != v else f"{v:.1f}"  # noqa: E731
    out = ["# Calibração do atalho do auditor", "",
           f"Amostra estratificada por tipo: {r['amostra'].get('atalho', 0)} reprovadas só por atalho (de "
           f"{r['populacao']['atalho']}) e {r['amostra'].get('validas', 0)} válidas (de {r['populacao']['validas']}), "
           "respondidas sem contexto, resposta de até 20 palavras, juiz padrão.", "",
           "| Modelo | Acerto nas reprovadas por atalho | Acerto nas válidas | Diferença (pontos) |", "|---|---|---|---|"]
    for m, a in r["acuracia"].items():
        out.append(f"| {m} | {f(a['atalho']['pct'])}% (IC {f(a['atalho']['ic95'][0])} a {f(a['atalho']['ic95'][1])}) | "
                   f"{f(a['validas']['pct'])}% (IC {f(a['validas']['ic95'][0])} a {f(a['validas']['ic95'][1])}) | "
                   f"{f(r['diferenca_pp'][m])} |")
    out += ["", f"Leitura: {r['leitura']}", "", "## Por tipo (acerto, %)", ""]
    for m, g in r["por_tipo"].items():
        out.append(f"- {m}: atalho {g['atalho']}; válidas {g['validas']}")
    return "\n".join(out) + "\n"
