"""Dificuldade cognitiva v3: quatro dimensões graduadas (0 a 2) e o nível dado por um profissional experiente de FPSO.

Substitui, como teste, a rubrica de 30 critérios (rubrica.py). Cada questão do banco final recebe, numa chamada:
conhecimento, inferencia, sistemas e generalista (0 a 2 cada) e um nivel_profissional (facil, media, dificil).
O nível pelas dimensões vem da soma: 0 a 2 fácil, 3 a 5 média, 6 a 8 difícil.

Uso (na raiz do repositório):
    python -m pipeline.qa_research.experimento_ab.dificuldade_v3 [--amostra N] [--workers N] [--modelo M]

Saída em relatorios/petroquest_banco_v1/dificuldade_<VERSAO>/ (ou dificuldade_<VERSAO>_amostraN/): classificacoes/<id>.json,
dificuldade_v3.jsonl, resumo.json e DIFICULDADE_V3.md. Retomável: repetir o comando só classifica o que falta.
O relatório compara os dois níveis entre si, com a rubrica antiga e com a dificuldade empírica (painel de quatro
modelos sem contexto: critério atual ancorado no GPT-5 e critério de proporção).
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json

from . import comum as C
from .banco import SAIDA as BANCO

MODELO = "gpt-5-4-petrobras:low"
PROMPT = "dificuldade_v3"
VERSAO = "v3_1"   # muda a cada ajuste do prompt; cada versão grava na própria pasta
NIVEIS = ("facil", "media", "dificil")
DIMENSOES = ("conhecimento", "inferencia", "sistemas", "generalista")
PAINEL = ("gpt-4-1-mini", "gpt-4-1", "gpt-5-mini", "gpt-5")   # independentes; o GPT-5.4 gerou as questões
ROTULO = {"facil": "Fácil", "media": "Média", "dificil": "Difícil"}


def _filtrado(exc: Exception) -> bool:
    """Bloqueio do filtro de conteúdo do Azure: tentar de novo não adianta."""
    return type(exc).__name__ == "ContentFiltered"


def nivel_soma(soma: int) -> str:
    return "facil" if soma <= 2 else "media" if soma <= 5 else "dificil"


def validar(d: dict) -> None:
    chaves = set(DIMENSOES) | {"nivel_profissional", "justificativa"}
    if not isinstance(d, dict) or set(d) != chaves:
        raise ValueError(f"use exatamente as chaves {sorted(chaves)}")
    for k in DIMENSOES:
        if d[k] not in (0, 1, 2) or isinstance(d[k], bool):
            raise ValueError(f"{k} deve ser o inteiro 0, 1 ou 2")
    if d["nivel_profissional"] not in NIVEIS:
        raise ValueError(f"nivel_profissional deve ser um de {NIVEIS}")
    if not isinstance(d["justificativa"], str) or not d["justificativa"].strip():
        raise ValueError("justificativa deve ser um texto")


def entrada(q: dict) -> str:
    campos = ("tipo", "pergunta", "resposta", "explicacao", "resposta_padrao", "por_que_nao")
    return json.dumps({k: q[k] for k in campos if q.get(k)}, ensure_ascii=False)


def empirico(q: dict) -> tuple[str, str, float]:
    """(critério atual em 3 níveis, critério de proporção, p) a partir do painel sem contexto."""
    d = q.get("dificuldade") or {}
    e = d.get("estrato")
    atual = "dificil" if e in ("dificil", "muito_dificil") else e
    sc = d.get("sem_contexto") or {}
    p = sum(sc.get(m) == "correta" for m in PAINEL) / len(PAINEL)
    prop = "facil" if p == 1 else "media" if p >= 0.5 else "dificil"
    return atual, prop, p


def _spearman(x, y) -> float | None:
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3:
        return None

    def postos(v):
        r = np.empty(len(v))
        r[np.argsort(v, kind="stable")] = np.arange(len(v), dtype=float)
        for val in np.unique(v):
            r[v == val] = r[v == val].mean()
        return r
    rx, ry = postos(x), postos(y)
    if rx.std() == 0 or ry.std() == 0:
        return None
    return float(np.corrcoef(rx, ry)[0, 1])


class DificuldadeV3:
    def __init__(self, banco: Path = BANCO, *, amostra: int = 0, semente: int = 20261112, modelo: str = MODELO,
                 workers: int = 12, cliente=None, progress=print):
        self.banco = Path(banco)
        self.amostra, self.semente = int(amostra or 0), semente
        nome = f"dificuldade_{VERSAO}" + (f"_amostra{self.amostra}" if self.amostra else "")
        self.saida = self.banco / nome
        self.modelo, self.workers, self.progress = modelo, max(1, int(workers)), progress
        self._cliente = cliente

    def cliente(self):
        if self._cliente is None:
            self._cliente = C.cliente_llm(self.modelo, self.saida, "dificuldade_v3")
        return self._cliente

    def questoes(self) -> list[dict]:
        qs = C.linhas(self.banco / "banco.jsonl")
        if not self.amostra or self.amostra >= len(qs):
            return qs
        # amostra estratificada por tipo, reprodutível
        rng = random.Random(self.semente)
        por_tipo: dict = {}
        for q in qs:
            por_tipo.setdefault(q["tipo"], []).append(q)
        escolha = []
        for t, v in sorted(por_tipo.items()):
            k = max(1, round(self.amostra * len(v) / len(qs)))
            escolha += rng.sample(v, min(k, len(v)))
        return escolha

    def _arq(self, qid: str) -> Path:
        return self.saida / "classificacoes" / f"{qid}.json"

    def classificar(self) -> int:
        qs = self.questoes()
        sistema = C.prompt(PROMPT)
        cfg = {"schema": f"petroquest-dificuldade-{VERSAO}", "modelo": self.modelo, "prompt_sha256": C.sha(sistema),
               "amostra": self.amostra, "semente": self.semente if self.amostra else None}
        with output_lock(self.saida):
            old = read_json(self.saida / "config.json")
            if old is not None and old != cfg:
                raise ValueError(f"Pasta com outro modelo, prompt ou amostra: {C.relativo(self.saida)}; apague-a "
                                 "ou use outra amostra")
            atomic_json(self.saida / "config.json", cfg)
            (self.saida / "classificacoes").mkdir(parents=True, exist_ok=True)
            (self.saida / "falhas").mkdir(exist_ok=True)
            faltam = [q for q in qs if not self._arq(q["id"]).exists()]
            self.progress(f"[dificuldade_v3] {len(qs) - len(faltam)}/{len(qs)} já classificadas; "
                          f"{len(faltam)} a classificar", flush=True)

            def um(q) -> bool:
                try:
                    d = self.cliente().json(sistema, entrada(q), tag="dificuldade_v3", max_tokens=4000,
                                            item=q["item"], validate=validar)
                    soma = sum(d[k] for k in DIMENSOES)
                    rec = {"id": q["id"], **{k: d[k] for k in DIMENSOES}, "soma": soma,
                           "nivel_dimensoes": nivel_soma(soma), "nivel_profissional": d["nivel_profissional"],
                           "justificativa": d["justificativa"], "status": "classificada"}
                except Exception as exc:  # noqa: BLE001 - uma questão não para as outras
                    if _filtrado(exc):
                        rec = {"id": q["id"], "status": "bloqueio_provedor"}
                    else:
                        atomic_json(self.saida / "falhas" / f"{q['id']}.json",
                                    {"id": q["id"], "erro": f"{type(exc).__name__}: {exc}"[:1500]})
                        return False
                atomic_json(self._arq(q["id"]), rec)
                return True

            feitos = 0
            with ThreadPoolExecutor(max_workers=self.workers) as pool:
                for ok in pool.map(um, faltam):
                    feitos += ok
                    if feitos and feitos % 200 == 0:
                        self.progress(f"[dificuldade_v3] {feitos}/{len(faltam)}", flush=True)
            falhas = len(faltam) - feitos
            if falhas:
                self.progress(f"[dificuldade_v3] {falhas} falhas em {C.relativo(self.saida / 'falhas')}; "
                              "repita o comando", flush=True)
            return falhas

    def relatorio(self) -> dict:
        qs = {q["id"]: q for q in self.questoes()}
        rs = [r for i in qs if (p := self._arq(i)).exists() for r in [read_json(p)] if r.get("status") == "classificada"]
        n = len(rs)
        pct = lambda c, t: round(100 * c / t, 1) if t else None  # noqa: E731
        linhas = []
        for r in rs:
            q = qs[r["id"]]
            atual, prop, p = empirico(q)
            linhas.append({**r, "tipo": q["tipo"], "fonte": q.get("fonte"), "item": q["item"],
                           "empirico_atual": atual, "empirico_proporcao": prop, "p_painel": p,
                           "rubrica_antiga": (q.get("dificuldade") or {}).get("rubrica")})
        C.gravar_jsonl(self.saida / "dificuldade_v3.jsonl", linhas)

        def dist(chave):
            c = Counter(x[chave] for x in linhas)
            return {k: pct(c.get(k, 0), n) for k in NIVEIS}

        def cruz(a, b):
            c = Counter((x[a], x[b]) for x in linhas)
            return {k: {j: c.get((k, j), 0) for j in NIVEIS} for k in NIVEIS}

        def p_medio(chave):
            return {k: (round(float(np.mean(v)), 3) if (v := [x["p_painel"] for x in linhas if x[chave] == k])
                        else None) for k in NIVEIS}

        res: dict = {
            "n": n, "de": len(qs), "modelo": self.modelo, "amostra": self.amostra,
            "nivel_dimensoes": dist("nivel_dimensoes"), "nivel_profissional": dist("nivel_profissional"),
            "concordancia_dimensoes_profissional": pct(sum(x["nivel_dimensoes"] == x["nivel_profissional"]
                                                           for x in linhas), n),
            "dimensoes": {k: {str(v): pct(sum(x[k] == v for x in linhas), n) for v in (0, 1, 2)} for k in DIMENSOES},
            "soma": {str(s): pct(sum(x["soma"] == s for x in linhas), n) for s in range(9)},
            "p_medio_por_nivel": {"dimensoes": p_medio("nivel_dimensoes"),
                                  "profissional": p_medio("nivel_profissional")},
            "spearman": {
                "soma_x_p": _spearman([x["soma"] for x in linhas], [x["p_painel"] for x in linhas]),
                "profissional_x_p": _spearman([NIVEIS.index(x["nivel_profissional"]) for x in linhas],
                                              [x["p_painel"] for x in linhas]),
                **{f"{k}_x_p": _spearman([x[k] for x in linhas], [x["p_painel"] for x in linhas]) for k in DIMENSOES},
            },
            "cruzamentos": {
                "dimensoes_x_profissional": cruz("nivel_dimensoes", "nivel_profissional"),
                "dimensoes_x_empirico_atual": cruz("nivel_dimensoes", "empirico_atual"),
                "profissional_x_empirico_atual": cruz("nivel_profissional", "empirico_atual"),
                "profissional_x_empirico_proporcao": cruz("nivel_profissional", "empirico_proporcao"),
                "profissional_x_rubrica_antiga": cruz("nivel_profissional", "rubrica_antiga"),
            },
            "por_tipo": {t: {"n": len(v), **{k: pct(sum(x["nivel_profissional"] == k for x in v), len(v))
                                              for k in NIVEIS}}
                         for t, v in sorted({x["tipo"]: [y for y in linhas if y["tipo"] == x["tipo"]]
                                             for x in linhas}.items())},
        }
        atomic_json(self.saida / "resumo.json", res)
        (self.saida / "DIFICULDADE_V3.md").write_text(_markdown(res), encoding="utf-8")
        return res


def _markdown(r: dict) -> str:
    f = lambda v: "-" if v is None else f"{v:.1f}%"  # noqa: E731
    g = lambda v: "-" if v is None else f"{v:.2f}"  # noqa: E731
    out = ["# Dificuldade cognitiva v3", "",
           f"{r['n']} de {r['de']} questões do banco final classificadas por {r['modelo']}"
           + (f" (amostra estratificada por tipo de {r['amostra']})" if r["amostra"] else "") + ".", "",
           "Nível pelas dimensões: soma de conhecimento, inferência, sistemas e generalista (0 a 8); "
           "0 a 2 fácil, 3 a 5 média, 6 a 8 difícil. Nível profissional: julgamento direto do classificador.", "",
           "| Nível | Pelas dimensões | Profissional |", "|---|---|---|"]
    out += [f"| {ROTULO[k]} | {f(r['nivel_dimensoes'][k])} | {f(r['nivel_profissional'][k])} |" for k in NIVEIS]
    out += ["", f"Concordância entre os dois níveis: {f(r['concordancia_dimensoes_profissional'])}.", "",
            "## Dimensões", "", "| Dimensão | 0 | 1 | 2 | Spearman com p |", "|---|---|---|---|---|"]
    out += [f"| {k} | {f(v['0'])} | {f(v['1'])} | {f(v['2'])} | {g(r['spearman'][k + '_x_p'])} |"
            for k, v in r["dimensoes"].items()]
    out += ["", "| Soma | " + " | ".join(r["soma"]) + " |", "|---" * 10 + "|",
            "| % | " + " | ".join(f(v) for v in r["soma"].values()) + " |", "",
            "## Relação com a dificuldade empírica", "",
            "p = fração do painel independente (GPT-4.1 mini, GPT-4.1, GPT-5 mini, GPT-5) que acerta sem contexto.", "",
            "| Nível | p médio (dimensões) | p médio (profissional) |", "|---|---|---|"]
    out += [f"| {ROTULO[k]} | {g(r['p_medio_por_nivel']['dimensoes'][k])} | "
            f"{g(r['p_medio_por_nivel']['profissional'][k])} |" for k in NIVEIS]
    out += ["", f"Spearman soma x p: {g(r['spearman']['soma_x_p'])}; nível profissional x p: "
            f"{g(r['spearman']['profissional_x_p'])} (negativo = acompanha a dificuldade empírica)."]
    titulos = {"dimensoes_x_profissional": ("Dimensões", "profissional"),
               "dimensoes_x_empirico_atual": ("Dimensões", "empírico atual"),
               "profissional_x_empirico_atual": ("Profissional", "empírico atual"),
               "profissional_x_empirico_proporcao": ("Profissional", "empírico por proporção"),
               "profissional_x_rubrica_antiga": ("Profissional", "rubrica antiga")}
    for chave, (a, b) in titulos.items():
        c = r["cruzamentos"][chave]
        out += ["", f"### {a} (linhas) x {b} (colunas)", "", "| | Fácil | Média | Difícil |", "|---|---|---|---|"]
        out += [f"| {ROTULO[k]} | " + " | ".join(str(c[k][j]) for j in NIVEIS) + " |" for k in NIVEIS]
    out += ["", "## Nível profissional por tipo", "", "| Tipo | n | Fácil | Média | Difícil |", "|---|---|---|---|---|"]
    out += [f"| {t} | {v['n']} | {f(v['facil'])} | {f(v['media'])} | {f(v['dificil'])} |"
            for t, v in r["por_tipo"].items()]
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--amostra", type=int, default=0, help="amostra estratificada por tipo (0 = banco inteiro)")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--modelo", default=MODELO)
    ap.add_argument("--so-relatorio", action="store_true", help="refaz só o relatório, sem chamadas")
    a = ap.parse_args(argv)
    d = DificuldadeV3(amostra=a.amostra, modelo=a.modelo, workers=a.workers)
    falhas = 0 if a.so_relatorio else d.classificar()
    r = d.relatorio()
    print(f"[dificuldade_v3] {r['n']}/{r['de']} classificadas. Relatório: {C.relativo(d.saida / 'DIFICULDADE_V3.md')}",
          flush=True)
    return 2 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
