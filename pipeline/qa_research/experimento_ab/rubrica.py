"""Dificuldade pela rubrica do especialista: uma classificação alternativa à dificuldade empírica (painel de modelos).

Cada questão do dataset final é classificada (fácil, média ou difícil) por um LLM com a rubrica que um especialista
do setor definiu (prompts/rubrica_dificuldade.md, itens F1-F9, M1-M9 e D1-D12), vendo pergunta, gabarito, explicação
e a resposta errada mais provável, sem o documento. Uma chamada por questão, retomável, com cache.

Saída em <dataset>/rubrica/: classificacoes/<uid>.json, rubrica.jsonl, resumo.json e RUBRICA.md, com a distribuição
por nível, tipo e fonte, a frequência de cada critério e, quando a avaliação existe, a comparação com a dificuldade
empírica (estratos e acurácia sem contexto de cada modelo por nível). As duas medidas não precisam concordar: a
rubrica mede exigência cognitiva; o painel mede o que os modelos já sabem (Kordi et al., 2025).
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.geracao_tipos.rodadas import _filtrado, _nome_arq

from . import comum as C
from .completo import SAIDA as FINAL_V2
from .painel import NAO_INDEPENDENTES, estrato

MODELO = "gpt-5-4-petrobras:low"
NIVEIS = ("facil", "media", "dificil")
CRITERIOS = tuple([f"F{i}" for i in range(1, 10)] + [f"M{i}" for i in range(1, 10)] + [f"D{i}" for i in range(1, 13)])
NOMES = {
    "F1": "conceito fundamental", "F2": "função básica de equipamento", "F3": "objetivo de sistema",
    "F4": "causa e efeito simples", "F5": "terminologia essencial", "F6": "condição operacional básica",
    "F7": "ação mais evidente", "F8": "poucos dados no enunciado", "F9": "candidatas bem distintas",
    "M1": "conceito aplicado a cenário", "M2": "interpretar condições operacionais", "M3": "causa, consequência e ação",
    "M4": "comparar duas soluções", "M5": "interface entre equipamentos", "M6": "diagnóstico conhecido",
    "M7": "ação mais adequada", "M8": "distinguir respostas razoáveis", "M9": "erro profissional comum",
    "D1": "múltiplas variáveis", "D2": "causa primária x efeitos", "D3": "integração entre sistemas",
    "D4": "operação, segurança, manutenção, integridade e controle", "D5": "falha com múltiplas hipóteses",
    "D6": "alternativas com vantagens e limitações", "D7": "avaliação de consequências", "D8": "priorização de ações",
    "D9": "dados incompletos", "D10": "princípios de engenharia e boas práticas", "D11": "solução mais adequada",
    "D12": "resposta verdadeira em outra condição"}


def validar(d: dict) -> None:
    if not isinstance(d, dict) or set(d) != {"criterios", "nivel", "justificativa"}:
        raise ValueError("use exatamente as chaves criterios, nivel e justificativa")
    if d["nivel"] not in NIVEIS:
        raise ValueError(f"nivel deve ser um de {NIVEIS}")
    if not isinstance(d["criterios"], list) or any(c not in CRITERIOS for c in d["criterios"]):
        raise ValueError("criterios deve ser uma lista de códigos da rubrica (F1-F9, M1-M9, D1-D12)")
    if not isinstance(d["justificativa"], str) or not d["justificativa"].strip():
        raise ValueError("justificativa deve ser um texto")


def entrada(q: dict) -> str:
    campos = ("tipo", "pergunta", "resposta", "explicacao", "resposta_padrao", "por_que_nao")
    return json.dumps({k: q[k] for k in campos if q.get(k)}, ensure_ascii=False)


def nivel_regra(criterios: list) -> str:
    """Leitura literal da rubrica, para conferir a classificação do modelo."""
    d = sum(c.startswith("D") for c in criterios)
    m = sum(c.startswith("M") for c in criterios)
    return "dificil" if d >= 2 else "media" if d == 1 or m >= 1 else "facil"


def _spearman(x, y) -> float | None:
    if len(x) < 3:
        return None
    rx, ry = (np.argsort(np.argsort(v, kind="stable"), kind="stable").astype(float) for v in (x, y))
    # postos médios para empates
    for v, r in ((np.asarray(x), rx), (np.asarray(y), ry)):
        for val in np.unique(v):
            idx = v == val
            r[idx] = r[idx].mean()
    if rx.std() == 0 or ry.std() == 0:
        return None
    return float(np.corrcoef(rx, ry)[0, 1])


class Rubrica:
    def __init__(self, dataset: Path = FINAL_V2, *, modelo: str = MODELO, workers: int = 8, cliente=None,
                 progress=print):
        self.dataset = Path(dataset)
        self.saida = self.dataset / "rubrica"
        self.modelo, self.workers, self.progress = modelo, max(1, int(workers)), progress
        self._cliente = cliente

    def cliente(self):
        if self._cliente is None:
            self._cliente = C.cliente_llm(self.modelo, self.saida, "rubrica")
        return self._cliente

    def _arq(self, uid: str) -> Path:
        return self.saida / "classificacoes" / f"{_nome_arq(uid)}.json"

    def classificar(self) -> int:
        qs = C.linhas(self.dataset / "dataset.jsonl")
        cfg = {"schema": "petroquest-rubrica-v1", "modelo": self.modelo,
               "prompt_sha256": C.sha(C.prompt("rubrica_dificuldade"))}
        with output_lock(self.saida):
            old = read_json(self.saida / "config.json")
            if old is not None and old != cfg:
                raise ValueError(f"Rubrica com outro modelo ou prompt em {C.relativo(self.saida)}; apague a pasta")
            atomic_json(self.saida / "config.json", cfg)
            (self.saida / "classificacoes").mkdir(parents=True, exist_ok=True)
            (self.saida / "falhas").mkdir(exist_ok=True)
            faltam = [q for q in qs if not self._arq(q["uid"]).exists()]
            self.progress(f"[rubrica] {len(qs) - len(faltam)}/{len(qs)} já classificadas; {len(faltam)} a classificar",
                          flush=True)
            sistema = C.prompt("rubrica_dificuldade")

            def um(q) -> bool:
                try:
                    d = self.cliente().json(sistema, entrada(q), tag="rubrica", max_tokens=4000, item=q["item"],
                                            validate=validar)
                    rec = {"uid": q["uid"], **d, "criterios": sorted(set(d["criterios"]), key=CRITERIOS.index),
                           "status": "classificada"}
                except Exception as exc:  # noqa: BLE001 - uma questão não para as outras
                    if _filtrado(exc):
                        rec = {"uid": q["uid"], "criterios": [], "nivel": None, "justificativa": "",
                               "status": "bloqueio_provedor"}
                    else:
                        atomic_json(self.saida / "falhas" / self._arq(q["uid"]).name,
                                    {"uid": q["uid"], "erro": f"{type(exc).__name__}: {exc}"[:1500]})
                        return False
                atomic_json(self._arq(q["uid"]), rec)
                return True

            feitos = 0
            with ThreadPoolExecutor(max_workers=self.workers) as pool:
                for ok in pool.map(um, faltam):
                    feitos += ok
                    if feitos and feitos % 200 == 0:
                        self.progress(f"[rubrica] {feitos}/{len(faltam)}", flush=True)
            falhas = len(faltam) - feitos
            if falhas:
                self.progress(f"[rubrica] {falhas} falhas registradas em {C.relativo(self.saida / 'falhas')}; "
                              "repita o comando", flush=True)
            return falhas

    def relatorio(self) -> dict:
        qs = {q["uid"]: q for q in C.linhas(self.dataset / "dataset.jsonl")}
        rs = [r for u in qs if (p := self._arq(u)).exists() for r in [read_json(p)] if r.get("nivel")]
        C.gravar_jsonl(self.saida / "rubrica.jsonl", [{**r, "tipo": qs[r["uid"]]["tipo"], "fonte": qs[r["uid"]]["fonte"],
                                                         "nivel_regra": nivel_regra(r["criterios"])} for r in rs])
        n = len(rs)
        pct = lambda c, t: round(100 * c / t, 1) if t else None  # noqa: E731
        niv = {r["uid"]: r["nivel"] for r in rs}
        res: dict = {"n": n, "de": len(qs), "modelo": self.modelo,
                     "niveis": {k: pct(v, n) for k, v in Counter(niv.values()).items()},
                     "concorda_regra": pct(sum(r["nivel"] == nivel_regra(r["criterios"]) for r in rs), n),
                     "criterios": {c: pct(v, n) for c, v in Counter(c for r in rs for c in r["criterios"]).most_common()}}
        for chave in ("tipo", "fonte"):
            grupos: dict = {}
            for r in rs:
                grupos.setdefault(qs[r["uid"]][chave], []).append(r["nivel"])
            res[f"por_{chave}"] = {g: {"n": len(v), **{k: pct(v.count(k), len(v)) for k in NIVEIS}}
                                   for g, v in sorted(grupos.items())}
        # comparação com a dificuldade empírica (sem contexto)
        vs: dict = {}
        if (self.dataset / "pares.csv").exists():
            with (self.dataset / "pares.csv").open(encoding="utf-8-sig") as f:
                for r in csv.DictReader(C.sem_nul(f)):
                    if r["uid"] in niv:
                        vs.setdefault(r["uid"], {})[r["modelo"]] = r["veredito_closed_book"]
        if vs:
            modelos = sorted({m for v in vs.values() for m in v})
            res["acuracia_por_nivel"] = {m: {k: pct(sum(vs[u].get(m) == "correta" for u in us), len(us))
                                             for k in NIVEIS for us in [[u for u in vs if niv[u] == k]]}
                                         for m in modelos}
            cruz = Counter((niv[u], estrato(v)) for u, v in vs.items())
            res["cruzamento_estratos"] = {k: {e: cruz.get((k, e), 0) for e in ("facil", "media", "dificil", "muito_dificil")}
                                          for k in NIVEIS}
            ind = [m for m in modelos if m not in NAO_INDEPENDENTES]
            us = list(vs)
            p = [np.mean([{"correta": 1, "parcial": .5}.get(vs[u].get(m), 0) for m in ind]) for u in us]
            res["spearman_nivel_x_acerto"] = _spearman([NIVEIS.index(niv[u]) for u in us], p)
        atomic_json(self.saida / "resumo.json", res)
        (self.saida / "RUBRICA.md").write_text(_markdown(res), encoding="utf-8")
        return res


NOME_MODELO = {"gpt-4-1-nano": "GPT-4.1 Nano", "gpt-4-1-mini": "GPT-4.1 Mini", "gpt-4-1": "GPT-4.1",
               "gpt-5-nano": "GPT-5 nano", "gpt-5-mini": "GPT-5 mini", "gpt-5": "GPT-5", "gpt-5-4": "GPT-5.4 (ref.)"}
ROTULO = {"facil": "Fácil", "media": "Média", "dificil": "Difícil"}


def _markdown(r: dict) -> str:
    f = lambda v: "-" if v is None else f"{v:.1f}%"  # noqa: E731
    out = ["# Dificuldade pela rubrica do especialista", "",
           f"{r['n']} de {r['de']} questões classificadas por {r['modelo']} (pergunta, gabarito, explicação e resposta "
           "errada mais provável, sem o documento).", "",
           "| Nível | Questões |", "|---|---|"]
    out += [f"| {ROTULO[k]} | {f(r['niveis'].get(k, 0))} |" for k in NIVEIS]
    out += ["", f"Classificação do modelo igual à leitura literal da rubrica (2+ itens de Difícil = difícil; "
            f"1 de Difícil ou algum de Média = média): {f(r['concorda_regra'])}.", "",
            "## Por tipo", "", "| Tipo | n | Fácil | Média | Difícil |", "|---|---|---|---|---|"]
    out += [f"| {t} | {v['n']} | {f(v['facil'])} | {f(v['media'])} | {f(v['dificil'])} |" for t, v in r["por_tipo"].items()]
    out += ["", "## Por fonte", "", "| Fonte | n | Fácil | Média | Difícil |", "|---|---|---|---|---|"]
    out += [f"| {t} | {v['n']} | {f(v['facil'])} | {f(v['media'])} | {f(v['dificil'])} |" for t, v in r["por_fonte"].items()]
    if r.get("acuracia_por_nivel"):
        out += ["", "## Rubrica x acerto dos modelos (sem contexto)", "",
                "| Modelo | Fácil | Média | Difícil |", "|---|---|---|---|"]
        ordem = [m for m in NOME_MODELO if m in r["acuracia_por_nivel"]]
        out += [f"| {NOME_MODELO[m]} | " + " | ".join(f(r["acuracia_por_nivel"][m][k]) for k in NIVEIS) + " |"
                for m in ordem]
        out += ["", "| Rubrica \\ empírico | fácil | média | difícil | muito difícil |", "|---|---|---|---|---|"]
        out += [f"| {ROTULO[k]} | " + " | ".join(str(v) for v in r["cruzamento_estratos"][k].values()) + " |"
                for k in NIVEIS]
        sp = r.get("spearman_nivel_x_acerto")
        out += ["", f"Correlação de Spearman entre o nível da rubrica e o acerto médio dos modelos independentes: "
                f"{'-' if sp is None else f'{sp:.2f}'} (negativa = a rubrica acompanha a dificuldade empírica)."]
    out += ["", "## Critérios mais exigidos", "", "| Critério | Questões |", "|---|---|"]
    out += [f"| {c} {NOMES[c]} | {f(v)} |" for c, v in r["criterios"].items()]
    out += ["", "A rubrica mede exigência cognitiva; o painel mede o que os modelos já sabem. Divergência entre as duas "
            "é esperada e informativa (Kordi et al., 2025)."]
    return "\n".join(out) + "\n"


def executar(dataset: Path = FINAL_V2, workers: int = 8, modelo: str = MODELO, progress=print) -> int:
    r = Rubrica(dataset, modelo=modelo, workers=workers, progress=progress)
    falhas = r.classificar()
    r.relatorio()
    return 2 if falhas else 0
