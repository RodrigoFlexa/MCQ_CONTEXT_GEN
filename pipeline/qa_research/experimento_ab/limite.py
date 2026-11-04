"""Experimento do limite de palavras na resposta dos modelos avaliados (subconjunto do dataset final).

Pergunta: limitar a resposta (por instrução, não por corte de tokens) muda a acurácia, as parciais e a concordância
entre o juiz e as métricas lexicais (F1, BLEU, ROUGE-L)? Desenho pareado:
  - controle: as respostas de até 100 palavras já avaliadas no dataset final (pares.csv e painel);
  - tratamento: as mesmas questões, os mesmos modelos e o mesmo juiz, com resposta de até N palavras;
  - só sem contexto (a condição principal do benchmark);
  - amostra estratificada por tipo de questão e estrato de dificuldade (painel), com semente fixa.
Saída em petroquest_final_v1/limite_<N>/: respostas, vereditos, comparacao.json e LIMITE.md.
"""
from __future__ import annotations

import csv
import json
import math
import random
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json
from pipeline.inventario.textutil import read_json as ler
from pipeline.qa_research import benchmark_gap as G
from pipeline.qa_research.geracao_tipos.rodadas import _filtrado, _nome_arq

from . import comum as C
from .final import SAIDA

MODELOS = {"gpt-4-1-nano": "gpt-4-1-nano-petrobras", "gpt-4-1-mini": "gpt-4-1-mini-petrobras",
           "gpt-4-1": "gpt-4-1-petrobras", "gpt-5-nano": "gpt-5-nano-petrobras:low",
           "gpt-5-mini": "gpt-5-mini-petrobras:low", "gpt-5": "gpt-5-petrobras:low", "gpt-5-4": "gpt-5-4-petrobras:low"}
PAINEL = ("gpt-5-nano", "gpt-5-mini", "gpt-5", "gpt-5-4")
STOP = set("a o as os um uma uns umas de do da dos das em no na nos nas por pelo pela pelos pelas para com e ou que "
           "se ao aos à às é".split())


def prompt_curta(limite: int) -> str:
    return C.prompt("respondente_curta").format(limite=limite)


# ------------------------------------------------------------------ métricas lexicais
def norm(t: str) -> list[str]:
    t = re.sub(r"[^\w\s]", " ", unicodedata.normalize("NFC", (t or "").lower()))
    return [w for w in t.split() if w not in STOP]


def f1(pred: str, ref: str) -> tuple[float, float, float]:
    """F1, precisão e revocação por tokens (normalização do SQuAD, sem stopwords)."""
    p, r = norm(pred), norm(ref)
    comum = sum((Counter(p) & Counter(r)).values())
    if not p or not r or not comum:
        return 0.0, 0.0, 0.0
    P, R = comum / len(p), comum / len(r)
    return 2 * P * R / (P + R), P, R


def rouge_l(pred: str, ref: str) -> float:
    a, b = norm(pred), norm(ref)
    m = [0] * (len(b) + 1)
    for x in a:
        ant = 0
        for j, y in enumerate(b, 1):
            m[j], ant = (ant + 1 if x == y else max(m[j], m[j - 1])), m[j]
    lcs = m[-1]
    if not lcs:
        return 0.0
    P, R = lcs / len(a), lcs / len(b)
    return 2 * P * R / (P + R)


def bleu(preds: list[str], refs: list[str]) -> float:
    """BLEU-4 de corpus (precisões recortadas, média geométrica, penalidade de brevidade), 0 a 100."""
    num, den = [0] * 4, [0] * 4
    tam_p = tam_r = 0
    for p, r in zip(preds, refs):
        a, b = (p or "").lower().split(), (r or "").lower().split()
        tam_p, tam_r = tam_p + len(a), tam_r + len(b)
        for n in range(1, 5):
            ga = Counter(tuple(a[i:i + n]) for i in range(len(a) - n + 1))
            gb = Counter(tuple(b[i:i + n]) for i in range(len(b) - n + 1))
            num[n - 1] += sum((ga & gb).values())
            den[n - 1] += max(0, len(a) - n + 1)
    if not tam_p or any(d == 0 for d in den):
        return 0.0
    logp = sum(math.log((x + 1) / (d + 1)) for x, d in zip(num, den)) / 4   # suavização add-one
    bp = 1.0 if tam_p > tam_r else math.exp(1 - tam_r / tam_p)
    return 100 * bp * math.exp(logp)


def auc(pos: list[float], neg: list[float]) -> float | None:
    """Probabilidade de uma resposta correta ter F1 maior que uma incorreta (concordância lexical x juiz)."""
    if not pos or not neg:
        return None
    s = sum((p > n) + .5 * (p == n) for p in pos for n in neg)
    return s / (len(pos) * len(neg))


# ------------------------------------------------------------------ amostra
def amostrar(final: Path, n: int, semente: int = 20261103) -> list[dict]:
    """Estratificada por tipo x estrato de dificuldade (fácil / média / difícil ou mais), alocação proporcional."""
    ds = {q["uid"]: q for q in C.linhas(final / "dataset.jsonl")}
    est = {}
    with (final / "painel" / "dificuldade.csv").open(encoding="utf-8-sig") as f:
        for r in csv.DictReader(C.sem_nul(f)):
            est[r["uid"]] = "dificil" if r["estrato"] in ("dificil", "muito_dificil") else r["estrato"]
    grupos = defaultdict(list)
    for u in sorted(ds):
        if u in est:
            grupos[(ds[u]["tipo"], est[u])].append(u)
    total = sum(len(g) for g in grupos.values())
    rng = random.Random(semente)
    escolhidas = []
    for k in sorted(grupos):
        g = grupos[k]
        cota = min(len(g), max(1, round(n * len(g) / total)))
        escolhidas += rng.sample(g, cota)
    return [{**ds[u], "estrato": est[u]} for u in sorted(escolhidas)]


# ------------------------------------------------------------------ avaliação com resposta curta
class AvaliacaoCurta(G.AvaliacaoGap):
    """Mesmo motor do benchmark_gap com resposta de até `limite` palavras, com ou sem contexto."""
    limite = 20

    def responder_um(self, m, q):
        nome = "resposta_" + m + "_" + _nome_arq(q["uid"])
        try:
            d = self.cliente("resp_" + m, self.respondentes[m]).json(
                prompt_curta(self.limite), json.dumps({"pergunta": q["pergunta"], "contexto": q.get("contexto_tecnico")},
                                                 ensure_ascii=False),
                tag="resposta_curta_" + m, max_tokens=8000, item=q["item"], validate=G.Q.base.validar_resposta)
            pal = len(d["resposta"].split())
            rec = {"uid": q["uid"], "modelo": m, "resposta": d["resposta"], "status_avaliacao": "respondida",
                   "palavras": pal, "acima_limite_solicitado": pal > self.limite}
        except Exception as exc:  # noqa: BLE001
            if not _filtrado(exc):
                self._falha(nome, exc)
                return False
            rec = {"uid": q["uid"], "modelo": m, "resposta": None, "status_avaliacao": "bloqueio_respondente",
                   "erro": "ContentFiltered"}
        atomic_json(self._arq_resposta(m, q["uid"]), rec)
        self._ok(nome)
        with self.lock:
            self.respondidas[m].add(q["uid"])
        return True

    def checar_modelos(self):   # a sondagem de disponibilidade também usa a resposta curta
        if all(all(self._arq_resposta(m, u).exists() for u in self.carregar_questoes()) for m in self.respondentes):
            return
        for m, alias in self.respondentes.items():
            self.cliente("resp_" + m, alias).json(prompt_curta(self.limite), json.dumps(
                {"pergunta": "Qual a função de um separador trifásico?", "contexto": None}, ensure_ascii=False),
                tag="teste_curta_" + m, max_tokens=8000, validate=G.Q.base.validar_resposta)


def controle(final: Path) -> dict:
    """(modelo, uid) -> (resposta, veredito) com até 100 palavras, já avaliadas no dataset final."""
    out = {}
    with (final / "pares.csv").open(encoding="utf-8-sig") as f:
        for r in csv.DictReader(C.sem_nul(f)):
            out[(r["modelo"], r["uid"])] = (r["resposta_closed_book"], r["veredito_closed_book"])
    with (final / "painel" / "dificuldade.csv").open(encoding="utf-8-sig") as f:
        for r in csv.DictReader(C.sem_nul(f)):
            for m in PAINEL:
                arq = final / "painel" / "avaliacao" / "respostas" / m / f"{_nome_arq('closed_book:' + r['uid'])}.json"
                if r.get(f"v_{m}") and arq.exists():
                    out[(m, r["uid"])] = ((ler(arq) or {}).get("resposta") or "", r[f"v_{m}"])
    return out


def executar(final: Path = SAIDA, limite: int = 20, n: int = 300, modelos: dict | None = None, workers: int = 8,
             judge_workers: int = 2, clientes=None, progress=print) -> int:
    final = Path(final)
    if not (final / "painel" / "painel_concluido.json").exists():
        raise ValueError("O dataset final precisa estar avaliado (com painel) antes do experimento de limite")
    modelos = modelos or MODELOS
    saida = final / f"limite_{limite}"
    amostra = amostrar(final, n)
    rows = [{**q, "uid_original": q["uid"], "uid": "closed_book:" + q["uid"], "condicao": "closed_book",
             "contexto_tecnico": None} for q in amostra]
    cfg = {"schema": "petroquest-limite-v1", "limite_palavras": limite, "n": len(rows), "modelos": modelos,
           "juiz": G.Q.JUIZ, "questoes_sha256": C.sha(rows), "prompt_sha256": C.sha(prompt_curta(limite)),
           "juiz_prompt_sha256": C.sha(G.prompt("juiz"))}
    with output_lock(saida):
        old = ler(saida / "config.json")
        if old is not None and old != cfg:
            raise ValueError(f"{C.relativo(saida)} tem outro protocolo ou outra amostra; apague a pasta para refazer")
        atomic_json(saida / "config.json", cfg)
        G.Q.C.GeracaoSemConteudo.jsonl(saida / "questoes.jsonl", rows)
        d = saida / "avaliacao"
        for m in modelos:
            for sub in ("respostas", "juiz"):
                (d / sub / m).mkdir(parents=True, exist_ok=True)
        (d / "falhas").mkdir(exist_ok=True)
        AvaliacaoCurta.limite = limite
        e = AvaliacaoCurta(saida, respondentes=modelos, juiz=G.Q.JUIZ, grupos=[tuple(modelos)], workers=workers,
                           judge_workers=judge_workers, lote_juiz=8, clientes=clientes, progress=progress)
        try:
            e.run()
        finally:
            for c in e.clientes.values():
                if hasattr(c, "close"):
                    c.close()
        completo = all(len(e.vereditos[m]) == len(rows) for m in modelos)
        comparar(final, saida, amostra, list(modelos), limite, e)
        progress(f"[limite] {C.relativo(saida / 'LIMITE.md')}", flush=True)
        return 0 if completo else 2


def comparar(final: Path, saida: Path, amostra: list, modelos: list, limite: int, e) -> dict:
    ctl = controle(final)
    refs = {q["uid"]: q["resposta"] for q in amostra}
    res, rng = {}, np.random.default_rng(7)
    for m in modelos:
        linhas = {}
        for cond in ("100", str(limite)):
            pares = []
            for u in refs:
                if cond == "100":
                    r, v = ctl.get((m, u), (None, None))
                else:
                    rec = ler(e._arq_resposta(m, "closed_book:" + u)) or {}
                    r, v = rec.get("resposta"), e.vereditos[m].get("closed_book:" + u)
                if r and v in ("correta", "parcial", "incorreta"):
                    pares.append((u, r, v))
            if not pares:
                continue
            fs = [f1(r, refs[u]) for u, r, _ in pares]
            pos = [f[0] for f, (_, _, v) in zip(fs, pares) if v == "correta"]
            neg = [f[0] for f, (_, _, v) in zip(fs, pares) if v == "incorreta"]
            linhas[cond] = {
                "n": len(pares), "acuracia": 100 * np.mean([v == "correta" for _, _, v in pares]),
                "com_parcial": 100 * np.mean([{"correta": 1, "parcial": .5}.get(v, 0) for _, _, v in pares]),
                "parciais": 100 * np.mean([v == "parcial" for _, _, v in pares]),
                "palavras": float(np.mean([len(r.split()) for _, r, _ in pares])),
                "acima_do_limite": 100 * np.mean([len(r.split()) > limite for _, r, _ in pares]),
                "f1": 100 * np.mean([f[0] for f in fs]), "precisao": 100 * np.mean([f[1] for f in fs]),
                "revocacao": 100 * np.mean([f[2] for f in fs]),
                "exact_match": 100 * np.mean([norm(r) == norm(refs[u]) for u, r, _ in pares]),
                "bleu": bleu([r for _, r, _ in pares], [refs[u] for u, _, _ in pares]),
                "rouge_l": 100 * np.mean([rouge_l(r, refs[u]) for u, r, _ in pares]),
                "auc_f1_juiz": auc(pos, neg),
                "_acertos": {u: float(v == "correta") for u, _, v in pares}}
        if len(linhas) == 2:   # diferença pareada da acurácia (mesmas questões nas duas condições), IC por bootstrap
            a, b = linhas[str(limite)]["_acertos"], linhas["100"]["_acertos"]
            comuns = sorted(set(a) & set(b))
            dif = np.array([a[u] - b[u] for u in comuns])
            boots = [rng.choice(dif, len(dif)).mean() for _ in range(2000)]
            linhas["diferenca_acuracia"] = {"pontos": 100 * dif.mean(), "ic95": [100 * np.quantile(boots, .025),
                                                                                 100 * np.quantile(boots, .975)],
                                            "n_pareado": len(comuns)}
        for c in linhas.values():
            c.pop("_acertos", None)
        res[m] = linhas
    out = {"limite": limite, "n_amostra": len(amostra),
           "amostra_por_tipo": dict(Counter(q["tipo"] for q in amostra)),
           "amostra_por_estrato": dict(Counter(q["estrato"] for q in amostra)), "modelos": res}
    atomic_json(saida / "comparacao.json", out)
    (saida / "LIMITE.md").write_text(_markdown(out), encoding="utf-8")
    return out


def _markdown(o: dict) -> str:
    L = o["limite"]
    f = lambda v, c=1: "-" if v is None else f"{v:.{c}f}"  # noqa: E731
    l = [f"# Limite de palavras na resposta: 100 x {L}", "",
         f"Amostra estratificada de {o['n_amostra']} questões do dataset final, sem contexto. Por tipo: "
         f"{o['amostra_por_tipo']}. Por estrato: {o['amostra_por_estrato']}.", "",
         "| Modelo | Limite | Acurácia | Com parcial | Parciais | Palavras | Acima do limite | Revocação | F1 | EM | BLEU | ROUGE-L | AUC F1 x juiz |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for m, c in o["modelos"].items():
        for cond in ("100", str(L)):
            if cond in c:
                x = c[cond]
                l.append(f"| {m} | {cond} | {f(x['acuracia'])}% | {f(x['com_parcial'])}% | {f(x['parciais'])}% | "
                         f"{f(x['palavras'], 0)} | {f(x['acima_do_limite'])}% | {f(x['revocacao'])} | {f(x['f1'])} | "
                         f"{f(x['exact_match'])} | {f(x['bleu'])} | {f(x['rouge_l'])} | {f(x['auc_f1_juiz'], 2)} |")
    l += ["", "## Diferença pareada da acurácia (limite curto − 100 palavras)", "", "| Modelo | Pontos | IC 95% |", "|---|---|---|"]
    for m, c in o["modelos"].items():
        d = c.get("diferenca_acuracia")
        if d:
            l.append(f"| {m} | {d['pontos']:+.1f} | [{d['ic95'][0]:+.1f}; {d['ic95'][1]:+.1f}] |")
    l += ["", "AUC F1 x juiz: probabilidade de uma resposta julgada correta ter F1 maior que uma julgada incorreta "
          "(0,5 = métrica lexical não distingue; 1 = concorda sempre com o juiz). O GPT-5.4 gerou as questões e "
          "entra só como referência."]
    return "\n".join(l) + "\n"
