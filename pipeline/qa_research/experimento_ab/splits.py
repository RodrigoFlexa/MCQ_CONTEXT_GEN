"""Divisão do banco final em treino, validação e teste (70/10/20), estratificada e sem vazamento.

Unidade de divisão: o GRUPO, não a questão. Questões do mesmo foco de janela (mesmo documento, mesmos blocos) ficam no
mesmo conjunto, e grupos com questões muito parecidas no mesmo tópico (TF-IDF >= LIMIAR_SIMILAR) são unidos; assim
o teste não traz um conhecimento que o treino já ensina com outras palavras.
Estratificação: cada grupo vai para o conjunto com maior déficit em relação à meta, somando tópico, tipo, estrato de
dificuldade empírica e fonte. Determinística (semente fixa).
Saída em <banco>/splits/: treino.jsonl, validacao.jsonl, teste.jsonl, divisao.json e SPLITS.md.
"""
from __future__ import annotations

import random

from collections import Counter, defaultdict
from pathlib import Path

from pipeline.inventario.textutil import atomic_json

from . import comum as C

PROPORCOES = {"treino": 0.7, "validacao": 0.1, "teste": 0.2}
SEMENTE = 20261107
LIMIAR_SIMILAR = 0.45
DOCS_REFINADOS = ("v23", "v22")          # fontes geradas sobre os documentos refinados (numeração de blocos própria)
DIMENSOES = ("item", "tipo", "estrato", "fonte")


def grupo_base(uid: str) -> str:
    fonte, item, origem, *resto = uid.split(":")
    if origem == "j":                     # fonte:item:j:rR:FOCO:K -> mesmo foco de janela
        docs = "refinado" if fonte in DOCS_REFINADOS else "base"
        return f"{docs}:{item}:j:{int(resto[1])}"
    return uid                            # composta: grupo próprio


def _uniao_similares(qs: list, grupo: dict) -> dict:
    from sklearn.feature_extraction.text import TfidfVectorizer
    pai = {g: g for g in set(grupo.values())}

    def raiz(g):
        while pai[g] != g:
            pai[g] = pai[pai[g]]
            g = pai[g]
        return g

    por_item = defaultdict(list)
    for q in qs:
        por_item[q["item"]].append(q)
    for lst in por_item.values():
        if len(lst) < 2:
            continue
        V = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True).fit_transform(
            [q["pergunta"] + " " + q["resposta"] for q in lst])
        S = (V @ V.T).tocoo()
        for i, j, s in zip(S.row, S.col, S.data):
            if i < j and s >= LIMIAR_SIMILAR:
                a, b = raiz(grupo[lst[i]["uid"]]), raiz(grupo[lst[j]["uid"]])
                if a != b:
                    pai[b] = a
    return {u: raiz(g) for u, g in grupo.items()}


def dividir(banco: Path, proporcoes: dict = PROPORCOES, semente: int = SEMENTE) -> dict:
    banco = Path(banco)
    qs = C.linhas(banco / "banco.jsonl")
    for q in qs:
        q["estrato"] = q["dificuldade"]["estrato"]
    grupo = _uniao_similares(qs, {q["uid"]: grupo_base(q["uid"]) for q in qs})
    membros = defaultdict(list)
    for q in qs:
        membros[grupo[q["uid"]]].append(q)
    total = {d: Counter(q[d] for q in qs) for d in DIMENSOES}
    n = len(qs)
    atual = {s: {d: Counter() for d in DIMENSOES} for s in proporcoes}
    tam = Counter()
    rng = random.Random(semente)
    ordem = sorted(membros)
    rng.shuffle(ordem)
    ordem.sort(key=lambda g: -len(membros[g]))            # grupos grandes primeiro; empates em ordem aleatória
    destino = {}
    for g in ordem:
        def deficit(s):
            p = proporcoes[s]
            d = sum((p * total[dim][q[dim]] - atual[s][dim][q[dim]]) / max(1.0, p * total[dim][q[dim]])
                    for q in membros[g] for dim in DIMENSOES)
            return d + 4 * len(membros[g]) * (p * n - tam[s]) / (p * n)
        s = max(proporcoes, key=lambda s: (deficit(s), proporcoes[s]))
        destino[g] = s
        for q in membros[g]:
            tam[s] += 1
            for dim in DIMENSOES:
                atual[s][dim][q[dim]] += 1
    saida = banco / "splits"
    saida.mkdir(exist_ok=True)
    conj = {s: [] for s in proporcoes}
    for q in sorted(qs, key=lambda q: q["id"]):
        q.pop("estrato")
        conj[destino[grupo[q["uid"]]]].append({**q, "split": destino[grupo[q["uid"]]]})
    for s, lst in conj.items():
        C.gravar_jsonl(saida / f"{s}.jsonl", lst)
    res = {"semente": semente, "proporcoes": proporcoes, "limiar_similar": LIMIAR_SIMILAR,
           "grupos": len(membros), "maior_grupo": max(len(v) for v in membros.values()),
           "tamanho": {s: len(v) for s, v in conj.items()},
           "pct": {s: round(100 * len(v) / n, 1) for s, v in conj.items()},
           **{f"por_{d}": {s: dict(sorted(Counter(q[d] if d != "estrato" else q["dificuldade"]["estrato"]
                                                  for q in v).items())) for s, v in conj.items()}
              for d in DIMENSOES},
           "ids": {s: [q["id"] for q in v] for s, v in conj.items()}}
    atomic_json(saida / "divisao.json", res)
    (saida / "SPLITS.md").write_text(_markdown(res), encoding="utf-8")
    return res


def _markdown(r: dict) -> str:
    sets = list(r["tamanho"])
    out = ["# Divisão do banco PetroQuest v1", "",
           f"Treino, validação e teste em {', '.join(f'{int(100 * p)}%' for p in r['proporcoes'].values())}, por grupo "
           f"({r['grupos']} grupos: mesmo foco de janela ou questões parecidas no mesmo tópico, TF-IDF >= "
           f"{r['limiar_similar']}), estratificada por tópico, tipo, estrato de dificuldade e fonte. Semente {r['semente']}.",
           "", "| | " + " | ".join(sets) + " |", "|---|" + "---|" * len(sets),
           "| Questões | " + " | ".join(f"{r['tamanho'][s]} ({r['pct'][s]}%)" for s in sets) + " |"]
    for dim, nome in (("tipo", "Tipo"), ("estrato", "Estrato")):
        chaves = sorted({k for s in sets for k in r[f"por_{dim}"][s]})
        for k in chaves:
            out.append(f"| {nome}: {k} | " + " | ".join(
                f"{100 * r[f'por_{dim}'][s].get(k, 0) / r['tamanho'][s]:.1f}%" for s in sets) + " |")
    mins = {s: min(r["por_item"][s].values()) for s in sets}
    out += ["", f"Tópicos presentes em cada conjunto: " + ", ".join(f"{s} {len(r['por_item'][s])}" for s in sets)
            + "; mínimo de questões por tópico: " + ", ".join(f"{s} {mins[s]}" for s in sets) + "."]
    return "\n".join(out) + "\n"



