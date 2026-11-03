"""Etapa 0: calibração da deduplicação com as 2.818 questões já existentes (nenhuma geração nova).

  1. embeddings de pergunta + resposta com text-embedding-3-small e 3-large (E5 antigo, só da pergunta, entra como
     base de comparação);
  2. cosseno centrado (vetor médio do banco) entre pares do mesmo documento;
  3. sorteio estratificado de pares por faixa de cosseno (por modelo) + pares que a deduplicação antiga já marcou
     como redundantes (positivos conhecidos);
  4. rótulo de referência (gpt-5.4 high, um par por chamada) e rótulo dos juízes candidatos (nano, mini) nos mesmos pares;
  5. AUC por modelo de embedding, limiares (descarte automático com precisão 100% na amostra; faixa do juiz com
     recall >= 95% dos redundantes) e escolha do juiz mais barato que concorda com a referência.

`rotulos_humanos.csv` (opcional, colunas par_id e rotulo_humano = sim/nao) substitui o rótulo de referência no
recálculo (`calibrar --recalcular`), sem novas chamadas.
"""
from __future__ import annotations

import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from pipeline.qa_research.piloto_janela.core import atomic_json, read_json

from . import comum as C
from .dedup import centrar, julgar

FAIXAS = (0.50, 0.90, 0.97, 0.99, 0.995, 0.998, 0.999, 1.0)   # quantis do cosseno centrado entre pares do mesmo doc
RECALL_ALVO = 0.95
MIN_AUTO = 3            # pares redundantes consecutivos no topo para habilitar descarte automático
CONCORDANCIA_MIN = 0.90


def _h(*p) -> int:
    return int(C.sha("|".join(map(str, p)))[:12], 16)


def carregar_banco(fonte: Path = C.GERACAO_FINAL):
    """Aprovadas (base do vetor médio e dos pares) e pares (removida, mantida) da deduplicação antiga."""
    aprov = C.linhas(Path(fonte) / "aprovadas.jsonl")
    positivos, extras = [], {}
    todas = Path(fonte) / "questoes.jsonl"
    if todas.exists():
        por_uid = {q["uid"]: q for q in aprov}
        for q in C.linhas(todas):
            if q.get("redundante") and q["redundante"] in por_uid and q["uid"] not in por_uid:
                extras[q["uid"]] = q
                positivos.append((q["uid"], q["redundante"]))
    return aprov, list(extras.values()), positivos


def pares_por_faixa(uids, itens, sim, por_faixa, semente):
    """Sorteio determinístico de pares do mesmo documento em cada faixa de quantil do cosseno centrado."""
    itens = np.asarray(itens)
    ii, jj = np.triu_indices(len(uids), 1)
    mesmo = itens[ii] == itens[jj]
    ii, jj = ii[mesmo], jj[mesmo]
    s = sim[ii, jj]
    bordas = np.quantile(s, FAIXAS)
    out = []
    for f in range(len(FAIXAS) - 1):
        lo, hi = bordas[f], bordas[f + 1]
        sel = np.where((s >= lo) & ((s < hi) if f < len(FAIXAS) - 2 else (s <= hi)))[0]
        sel = sorted(sel, key=lambda k: _h(semente, uids[ii[k]], uids[jj[k]]))[:por_faixa]
        out += [(uids[ii[k]], uids[jj[k]], f"{semente}:q{FAIXAS[f]}-{FAIXAS[f + 1]}") for k in sel]
    return out, {f"q{FAIXAS[f]}": float(bordas[f]) for f in range(len(FAIXAS))}


def auc(scores, y) -> float | None:
    """AUC por postos (Mann-Whitney), com empates divididos."""
    s, y = np.asarray(scores, float), np.asarray(y, int)
    ok = np.isfinite(s)
    s, y = s[ok], y[ok]
    n1, n0 = int(y.sum()), int((1 - y).sum())
    if not n1 or not n0:
        return None
    ordem = np.argsort(s)
    postos = np.empty(len(s))
    vals = s[ordem]
    k = 0
    while k < len(s):
        m = k
        while m + 1 < len(s) and vals[m + 1] == vals[k]:
            m += 1
        postos[ordem[k:m + 1]] = (k + m) / 2 + 1
        k = m + 1
    return float((postos[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def limiares(scores, y) -> dict:
    s, y = np.asarray(scores, float), np.asarray(y, int)
    ok = np.isfinite(s)
    s, y = s[ok], y[ok]
    ordem = np.argsort(-s)
    run = 0
    for k in ordem:
        if y[k] != 1:
            break
        run += 1
    auto = float(s[ordem[run - 1]]) if run >= MIN_AUTO else None   # None: nunca descarta sem juiz
    pos = np.sort(s[y == 1])
    if len(pos):
        juiz = float(pos[int(np.floor((1 - RECALL_ALVO) * len(pos)))])
    else:
        juiz = auto
    if auto is not None and juiz is not None and juiz > auto:
        juiz = auto
    acima = s >= juiz if juiz is not None else np.zeros(len(s), bool)
    return {"limiar_auto": auto, "limiar_juiz": juiz, "pares": int(len(s)), "redundantes": int(y.sum()),
            "redundantes_auto": int(run) if auto is not None else 0,
            "recall_juiz": float((acima & (y == 1)).sum() / max(1, y.sum())),
            "pares_para_juiz": int((acima & (s < auto if auto is not None else True)).sum())}


class Calibracao:
    def __init__(self, saida: Path, fonte: Path = C.GERACAO_FINAL, embeddings=tuple(C.EMBEDDINGS), referencia=C.REFERENCIA,
                 juizes: dict | None = None, por_faixa: int = 8, max_positivos: int = 40, workers: int = 8,
                 clientes: dict | None = None, embedders: dict | None = None, progress=print):
        self.saida, self.fonte = Path(saida), Path(fonte)
        self.embeddings, self.referencia = list(embeddings), referencia
        self.juizes = dict(juizes or C.JUIZES)
        self.por_faixa, self.max_positivos, self.workers = por_faixa, max_positivos, workers
        self.clientes, self.embedders, self.progress = dict(clientes or {}), dict(embedders or {}), progress

    def cliente(self, papel: str, modelo: str):
        if papel not in self.clientes:
            self.clientes[papel] = C.cliente_llm(modelo, self.saida, papel)
        return self.clientes[papel]

    def embedder(self, nome: str):
        if nome not in self.embedders:
            self.embedders[nome] = C.embedder(nome, self.saida)
        return self.embedders[nome]

    # -------------------------------------------------------------- 1-3. vetores e pares
    def vetores(self):
        aprov, extras, positivos = carregar_banco(self.fonte)
        todas = aprov + extras
        uids = [q["uid"] for q in todas]
        sims, medias = {}, {}
        for nome in self.embeddings:
            self.progress(f"[calibração] embeddings {nome}: {len(todas)} questões (cache por conteúdo)", flush=True)
            V = np.asarray(self.embedder(nome).encode([C.texto_questao(q) for q in todas]), dtype=np.float64)
            media = V[: len(aprov)].mean(axis=0)
            atomic_json(self.saida / f"media_{nome}.json", [float(x) for x in media])   # *.npy é ignorado pelo Git
            Vc = centrar(V, media)
            sims[nome] = Vc @ Vc.T
            medias[nome] = media
        if C.E5_CACHE.exists():   # base antiga: só a pergunta, só as aprovadas, mesma ordem do arquivo
            e5 = np.load(C.E5_CACHE)
            E = np.asarray(e5["vectors"], dtype=np.float64)
            if len(E) == len(aprov):
                Ec = centrar(E, E.mean(axis=0))
                full = np.full((len(todas), len(todas)), np.nan)
                full[: len(aprov), : len(aprov)] = Ec @ Ec.T
                sims["e5-small (pergunta)"] = full
        return todas, uids, sims, positivos, len(aprov)

    def pares(self, todas, uids, sims, positivos, n_aprov):
        arq = self.saida / "pares.json"
        if arq.exists():
            return read_json(arq)
        itens = [q["item"] for q in todas[:n_aprov]]
        pares, bordas = {}, {}
        for nome, S in sims.items():
            sel, bordas[nome] = pares_por_faixa(uids[:n_aprov], itens, S[:n_aprov, :n_aprov], self.por_faixa, nome)
            for a, b, estrato in sel:
                pares.setdefault(tuple(sorted((a, b))), estrato)
        for a, b in sorted(positivos, key=lambda p: _h("pos", *p))[: self.max_positivos]:
            pares.setdefault(tuple(sorted((a, b))), "dedup_antiga")
        lista = [{"par_id": f"P{k:04d}", "a": a, "b": b, "estrato": e} for k, ((a, b), e) in enumerate(sorted(pares.items()), 1)]
        atomic_json(arq, {"bordas_quantis": bordas, "pares": lista, "criado_em": datetime.now(timezone.utc).isoformat()})
        return read_json(arq)

    # -------------------------------------------------------------- 4. rótulos
    def rotular(self, pares, por_uid) -> int:
        tarefas = [(papel, modelo, p) for papel, modelo in [("referencia", self.referencia), *self.juizes.items()]
                   for p in pares if not (self.saida / "rotulos" / papel / f"{p['par_id']}.json").exists()]
        self.progress(f"[calibração] rótulos pendentes: {len(tarefas)} (referência + {len(self.juizes)} juízes)", flush=True)

        def um(t):
            papel, modelo, p = t
            a, b = por_uid[p["a"]], por_uid[p["b"]]
            try:
                d = julgar(self.cliente(papel, modelo), a, [b], tag=f"calibracao_{papel}", item=a["item"])
            except Exception as exc:  # noqa: BLE001 - par isolado
                atomic_json(self.saida / "falhas" / f"{papel}_{p['par_id']}.json",
                            {"erro": type(exc).__name__, "mensagem": str(exc)[:1500]})
                return False
            atomic_json(self.saida / "rotulos" / papel / f"{p['par_id']}.json",
                        {"par_id": p["par_id"], "modelo": modelo, "redundante": d["redundante"], "motivo": d["motivo"]})
            f = self.saida / "falhas" / f"{papel}_{p['par_id']}.json"
            if f.exists():
                f.unlink()
            return True

        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            return sum(not ok for ok in pool.map(um, tarefas))

    # -------------------------------------------------------------- 5. análise
    def analisar(self, todas, uids, sims, pares) -> dict:
        idx = {u: k for k, u in enumerate(uids)}
        por_uid = {q["uid"]: q for q in todas}
        rot = {papel: {p.stem: read_json(p)["redundante"] for p in (self.saida / "rotulos" / papel).glob("*.json")}
               for papel in ["referencia", *self.juizes]}
        humanos = {}
        arq_h = self.saida / "rotulos_humanos.csv"
        if arq_h.exists():
            with arq_h.open(encoding="utf-8-sig") as f:
                for r in csv.DictReader(f):
                    v = (r.get("rotulo_humano") or "").strip().lower()
                    if v in ("sim", "nao", "não"):
                        humanos[r["par_id"]] = v == "sim"
        verdade = {p["par_id"]: humanos.get(p["par_id"], rot["referencia"].get(p["par_id"])) for p in pares}
        verdade = {k: v for k, v in verdade.items() if v is not None}
        res = {"fonte_rotulo": "humano onde preenchido; demais: " + self.referencia, "rotulos_humanos": len(humanos),
               "pares": len(pares), "pares_com_rotulo": len(verdade),
               "redundantes": sum(verdade.values()), "modelos": {}, "juizes": {}}
        linhas = []
        for p in pares:
            if p["par_id"] not in verdade:
                continue
            row = {"par_id": p["par_id"], "estrato": p["estrato"], "item": por_uid[p["a"]]["item"],
                   "pergunta_a": por_uid[p["a"]]["pergunta"], "resposta_a": por_uid[p["a"]]["resposta"],
                   "pergunta_b": por_uid[p["b"]]["pergunta"], "resposta_b": por_uid[p["b"]]["resposta"],
                   "rotulo_referencia": {True: "sim", False: "nao"}.get(rot["referencia"].get(p["par_id"]), ""),
                   **{f"juiz_{j}": {True: "sim", False: "nao"}.get(rot[j].get(p["par_id"]), "") for j in self.juizes},
                   **{f"cos_{n}": round(float(S[idx[p["a"]], idx[p["b"]]]), 4) for n, S in sims.items()},
                   "rotulo_humano": {True: "sim", False: "nao"}.get(humanos.get(p["par_id"]), "")}
            linhas.append(row)
        y = [verdade[r["par_id"]] for r in linhas]
        par = {p["par_id"]: p for p in pares}
        for nome, S in sims.items():
            sc = [S[idx[par[r["par_id"]]["a"]], idx[par[r["par_id"]]["b"]]] for r in linhas]
            res["modelos"][nome] = {"auc": auc(sc, y), **limiares(sc, y),
                                    "observacao": "só pergunta; vetor antigo" if nome.startswith("e5") else "pergunta + resposta"}
        for j, modelo in self.juizes.items():
            pares_j = [(rot[j][r["par_id"]], verdade[r["par_id"]]) for r in linhas if r["par_id"] in rot[j]]
            tp = sum(a and b for a, b in pares_j)
            res["juizes"][j] = {"modelo": modelo, "n": len(pares_j),
                                "concordancia": sum(a == b for a, b in pares_j) / max(1, len(pares_j)),
                                "recall_redundantes": tp / max(1, sum(b for _, b in pares_j)),
                                "precisao_redundantes": tp / max(1, sum(a for a, _ in pares_j))}
        azure = {n: m for n, m in res["modelos"].items() if n in self.embeddings and m["auc"] is not None}
        if not azure:
            raise ValueError("Sem pares rotulados com redundantes e não redundantes: aumente --por-faixa")
        escolhido = max(azure, key=lambda n: azure[n]["auc"])
        juiz = next((j for j, m in res["juizes"].items()
                     if m["n"] and m["concordancia"] >= CONCORDANCIA_MIN and m["recall_redundantes"] >= CONCORDANCIA_MIN),
                    None)
        cfg = {"embedding": escolhido, **C.EMBEDDINGS[escolhido], "media": f"media_{escolhido}.json",
               "limiar_auto": azure[escolhido]["limiar_auto"] if azure[escolhido]["limiar_auto"] is not None else 2.0,
               "limiar_juiz": azure[escolhido]["limiar_juiz"] if azure[escolhido]["limiar_juiz"] is not None else 2.0,
               "juiz": self.juizes[juiz] if juiz else self.referencia, "juiz_nome": juiz or "referencia",
               "criterio": {"embedding": "maior AUC (cosseno centrado, pergunta + resposta)",
                            "limiar_auto": f"topo da amostra com >= {MIN_AUTO} redundantes consecutivos (precisão 100%); "
                                           "2.0 = nunca descarta sem juiz",
                            "limiar_juiz": f"recall >= {RECALL_ALVO:.0%} dos redundantes rotulados",
                            "juiz": f"mais barato com concordância e recall >= {CONCORDANCIA_MIN:.0%}; senão a referência"},
               "analise": res, "em": datetime.now(timezone.utc).isoformat()}
        atomic_json(self.saida / "calibracao.json", cfg)
        campos = list(linhas[0]) if linhas else ["par_id"]
        with (self.saida / "pares_rotulados.csv").open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=campos, quoting=csv.QUOTE_ALL)
            w.writeheader()
            w.writerows(linhas)
        self._markdown(cfg)
        return cfg

    def _markdown(self, cfg):
        a = cfg["analise"]
        l = ["# Calibração da deduplicação incremental", "",
             f"Pares rotulados: {a['pares_com_rotulo']} ({a['redundantes']} redundantes). Rótulo: {a['fonte_rotulo']}.", "",
             "| Embedding | AUC | limiar automático | limiar do juiz | recall na faixa do juiz | pares que iriam ao juiz |",
             "|---|---|---|---|---|---|"]
        for n, m in a["modelos"].items():
            f = lambda v: "-" if v is None else f"{v:.3f}"
            l.append(f"| {n} | {f(m['auc'])} | {f(m['limiar_auto'])} | {f(m['limiar_juiz'])} | {m['recall_juiz']:.0%} | "
                     f"{m['pares_para_juiz']} |")
        l += ["", "| Juiz | concordância | recall dos redundantes | precisão dos redundantes | n |", "|---|---|---|---|---|"]
        for j, m in a["juizes"].items():
            l.append(f"| {j} ({m['modelo']}) | {m['concordancia']:.0%} | {m['recall_redundantes']:.0%} | "
                     f"{m['precisao_redundantes']:.0%} | {m['n']} |")
        l += ["", f"**Escolhas:** embedding `{cfg['embedding']}`, limiar automático {cfg['limiar_auto']:.3f}, "
                  f"limiar do juiz {cfg['limiar_juiz']:.3f}, juiz `{cfg['juiz']}`.", "",
              "Cosseno centrado: subtrai o vetor médio do banco antes do cosseno. A amostra é estratificada por faixa, "
              "então recall e AUC valem para a amostra, não para a população de pares.",
              "Para revisar rótulos: preencha `rotulo_humano` (sim/nao) em `pares_rotulados.csv`, salve como "
              "`rotulos_humanos.csv` e rode a calibração com `--recalcular` (sem chamadas novas)."]
        (self.saida / "CALIBRACAO.md").write_text("\n".join(l) + "\n", encoding="utf-8")

    def run(self, recalcular: bool = False) -> int:
        self.saida.mkdir(parents=True, exist_ok=True)
        todas, uids, sims, positivos, n_aprov = self.vetores()
        pares = self.pares(todas, uids, sims, positivos, n_aprov)["pares"]
        falhas = 0 if recalcular else self.rotular(pares, {q["uid"]: q for q in todas})
        cfg = self.analisar(todas, uids, sims, pares)
        self.progress(f"[calibração] embedding {cfg['embedding']} | auto {cfg['limiar_auto']:.3f} | juiz "
                      f"{cfg['limiar_juiz']:.3f} ({cfg['juiz']}) | falhas pendentes {falhas}", flush=True)
        return falhas
