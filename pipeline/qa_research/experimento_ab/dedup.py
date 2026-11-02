"""Deduplicação incremental: cada questão é comparada com o banco já aceito do mesmo documento.

  1. embedding de pergunta + resposta (modelo escolhido na calibração);
  2. cosseno CENTRADO (subtrai o vetor médio do domínio, calculado na calibração): o cosseno bruto dos embeddings
     fica concentrado numa faixa alta e não separa questões diferentes;
  3. vizinho >= limiar_auto: redundante sem chamada; vizinhos entre limiar_juiz e limiar_auto: um juiz decide
     (com até k vizinhos, uma chamada por questão) e escolhe qual das duas fica; abaixo de limiar_juiz: nova.

Cada decisão é um arquivo por questão (retomável e auditável). Falha numa questão não afeta as outras.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from pipeline.qa_research.piloto_janela.core import atomic_json, read_json

from .comum import prompt, texto_questao


def centrar(vetores: np.ndarray, media: np.ndarray) -> np.ndarray:
    v = np.asarray(vetores, dtype=np.float64) - np.asarray(media, dtype=np.float64)
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    return v / np.where(n < 1e-12, 1.0, n)


def validar_par(d: dict, ids: list[str]) -> None:
    if not isinstance(d, dict) or set(d) != {"redundante", "com", "manter", "motivo"}:
        raise ValueError("Use exatamente as chaves redundante, com, manter e motivo.")
    if type(d["redundante"]) is not bool or not isinstance(d["motivo"], str) or not d["motivo"].strip():
        raise ValueError("redundante deve ser true/false e motivo, uma frase preenchida.")
    if d["redundante"]:
        if d["com"] not in ids or d["manter"] not in ("nova", "existente"):
            raise ValueError(f"Quando redundante, com deve ser um de {ids} e manter, 'nova' ou 'existente'.")
    elif d["com"] is not None or d["manter"] is not None:
        raise ValueError("Quando não redundante, com e manter devem ser null.")


def julgar(cliente, nova: dict, existentes: list[dict], tag: str = "dedup_par", item=None) -> dict:
    ids = [f"E{k}" for k in range(1, len(existentes) + 1)]
    user = json.dumps({"nova": {"pergunta": nova["pergunta"], "resposta": nova["resposta"]},
                       "existentes": [{"id": i, "pergunta": e["pergunta"], "resposta": e["resposta"]}
                                      for i, e in zip(ids, existentes)]}, ensure_ascii=False)
    d = cliente.json(prompt("dedup_par"), user, tag=tag, max_tokens=4000, item=item, validate=lambda d: validar_par(d, ids))
    return {**d, "com_uid": existentes[ids.index(d["com"])]["uid"] if d["redundante"] else None}


class DedupIncremental:
    def __init__(self, pasta: Path, embedder, media: np.ndarray, limiar_auto: float, limiar_juiz: float, juiz,
                 k: int = 5, progress=print):
        if limiar_juiz > limiar_auto:
            raise ValueError("limiar_juiz não pode passar de limiar_auto")
        self.pasta, self.embedder, self.media = Path(pasta), embedder, np.asarray(media, dtype=np.float64)
        self.limiar_auto, self.limiar_juiz, self.juiz, self.k, self.progress = limiar_auto, limiar_juiz, juiz, k, progress

    def _arq(self, item: str, uid: str) -> Path:
        return self.pasta / item / (uid.replace(":", "_") + ".json")

    def processar(self, item: str, candidatas: list[dict], falha=None, ok=None) -> int:
        """candidatas: aprovadas pelo auditor (antes da deduplicação), na ordem de geração. Retorna falhas."""
        if not candidatas:
            return 0
        try:
            vetores = centrar(self.embedder.encode([texto_questao(q) for q in candidatas]), self.media)
        except Exception as exc:  # noqa: BLE001 - embeddings indisponíveis: o tópico fica pendente, sem decisões
            if falha:
                falha(f"dedup_{item}_embeddings", exc)
                return 1
            raise
        if ok:
            ok(f"dedup_{item}_embeddings")
        pos = {q["uid"]: k for k, q in enumerate(candidatas)}
        ativos: list[str] = []
        falhas = novas = 0
        for k, q in enumerate(candidatas):
            arq = self._arq(item, q["uid"])
            d = read_json(arq) if arq.exists() else None
            if d is None:
                try:
                    d = self._decidir(item, q, vetores[k], [candidatas[pos[u]] for u in ativos],
                                      vetores[[pos[u] for u in ativos]] if ativos else None)
                except Exception as exc:  # noqa: BLE001 - isolada por questão
                    falhas += 1
                    if falha:
                        falha(f"dedup_{item}_{q['uid'].replace(':', '_')}", exc)
                    continue
                atomic_json(arq, d)
                if ok:
                    ok(f"dedup_{item}_{q['uid'].replace(':', '_')}")
                novas += 1
            if d["decisao"] == "nova":
                ativos.append(q["uid"])
            elif d["decisao"] == "substitui":
                if d["substituida"] in ativos:
                    ativos.remove(d["substituida"])
                ativos.append(q["uid"])
        if novas:
            self.progress(f"   dedup incremental {item}: {novas} decisões novas, {len(ativos)} no banco", flush=True)
        return falhas

    def _decidir(self, item, q, vetor, banco, vetores_banco) -> dict:
        base = {"uid": q["uid"], "item": item, "em": datetime.now(timezone.utc).isoformat(),
                "limiar_auto": self.limiar_auto, "limiar_juiz": self.limiar_juiz}
        if not banco:
            return {**base, "decisao": "nova", "via": "banco_vazio", "max_cosseno": None, "vizinhos": []}
        s = vetores_banco @ vetor
        ordem = np.argsort(-s)
        vizinhos = [{"uid": banco[i]["uid"], "cosseno": round(float(s[i]), 4)} for i in ordem[: self.k]]
        topo = float(s[ordem[0]])
        base.update(max_cosseno=round(topo, 4), vizinhos=vizinhos)
        if topo >= self.limiar_auto:
            return {**base, "decisao": "redundante", "via": "automatico", "com": banco[ordem[0]]["uid"]}
        cands = [banco[i] for i in ordem[: self.k] if s[i] >= self.limiar_juiz]
        if not cands:
            return {**base, "decisao": "nova", "via": "abaixo_do_limiar"}
        j = julgar(self.juiz, q, cands, tag="dedup_incremental", item=item)
        if not j["redundante"]:
            return {**base, "decisao": "nova", "via": "juiz", "juiz": j}
        if j["manter"] == "nova":
            return {**base, "decisao": "substitui", "via": "juiz", "substituida": j["com_uid"], "juiz": j}
        return {**base, "decisao": "redundante", "via": "juiz", "com": j["com_uid"], "juiz": j}

    def redundantes(self, item: str) -> dict:
        """uid removido -> uid mantido (redundantes e substituídas)."""
        out = {}
        for p in sorted((self.pasta / item).glob("*.json")):
            d = read_json(p)
            if d["decisao"] == "redundante":
                out[d["uid"]] = d["com"]
            elif d["decisao"] == "substitui":
                out[d["substituida"]] = d["uid"]
        # uma substituição posterior pode remover quem já tinha absorvido outra: aponta para quem ficou
        for u in list(out):
            visto, alvo = {u}, out[u]
            while alvo in out and alvo not in visto:
                visto.add(alvo)
                alvo = out[alvo]
            out[u] = alvo
        return out


def carregar_calibracao(arq: Path) -> dict:
    d = read_json(arq)
    for k in ("embedding", "media", "limiar_auto", "limiar_juiz", "juiz"):
        if k not in d:
            raise ValueError(f"calibracao.json sem o campo {k}; rode a etapa de calibração")
    return d
