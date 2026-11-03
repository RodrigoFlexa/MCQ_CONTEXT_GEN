"""Filtro do banco antigo: as questões da geração final (v19) com gabarito totalmente sustentado, com o gabarito
reduzido ao elemento decisivo e auditadas pelo auditor v23 (com os blocos de origem).

Para cada questão sustentada (faithfulness do benchmark_gap_full_v1):
  1. encurtar: resposta curta (até 15 palavras, mesmo conteúdo) e explicação à parte;
  2. auditar: as 5 verificações binárias do auditor v23 sobre a versão curta.
Ficam as aprovadas pelo auditor, no formato da geração final (com `blocos` ou `foco`), prontas para o benchmark_gap.
Cada etapa é um arquivo por questão: repetir o comando retoma de onde parou; uma falha não afeta as outras.
"""
from __future__ import annotations

import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from pipeline.qa_research.geracao_tipos.core import _texto
from pipeline.qa_research.geracao_tipos.rodadas import _filtrado, _nome_arq
from pipeline.qa_research.piloto_janela.core import atomic_json, read_json

from . import comum as C
from .v22 import TETO_EXPLICACAO, TETO_RESPOSTA, validar_auditoria, veredito

FONTE = C.QA / "relatorios" / "geracao_final_20261024T204734Z" / "aprovadas.jsonl"
GAP = C.QA / "relatorios" / "benchmark_gap_full_v1"
SAIDA = C.QA / "relatorios" / "banco_antigo_filtrado_v1"
AVALIACAO = C.QA / "relatorios" / "benchmark_gap_antigo_filtrado_v1"
MODELOS = {"encurtar": "gpt-5-4-petrobras:medium", "auditoria": C.REFERENCIA}


def validar_curta(d: dict) -> None:
    if not isinstance(d, dict) or set(d) != {"resposta", "explicacao"}:
        raise ValueError("Use exatamente as chaves resposta e explicacao.")
    if not _texto(d["resposta"]) or not isinstance(d["explicacao"], str):
        raise ValueError("resposta preenchida e explicacao em texto.")
    if len(d["resposta"].split()) > TETO_RESPOSTA:
        raise ValueError(f"resposta com mais de {TETO_RESPOSTA} palavras: deixe só o elemento decisivo.")
    if len(d["explicacao"].split()) > TETO_EXPLICACAO:
        raise ValueError(f"explicacao com mais de {TETO_EXPLICACAO} palavras.")


class FiltroAntigo:
    def __init__(self, saida: Path = SAIDA, fonte: Path = FONTE, gap: Path = GAP, modelos: dict | None = None,
                 clientes: dict | None = None, workers: int = 8, progress=print):
        self.saida, self.fonte, self.gap = Path(saida), Path(fonte), Path(gap)
        self.modelos = {**MODELOS, **(modelos or {})}
        self._clientes, self.workers, self.progress = dict(clientes or {}), workers, progress

    def cliente(self, papel: str):
        if papel not in self._clientes:
            self._clientes[papel] = C.cliente_llm(self.modelos[papel], self.saida, papel)
        return self._clientes[papel]

    def candidatas(self) -> list[tuple[dict, str]]:
        status = {json.loads(l)["uid"]: json.loads(l)["status"] for l in (self.gap / "faithfulness.jsonl").open(encoding="utf-8")}
        ctx = {d["uid"]: d for d in C.linhas(self.gap / "contextos.jsonl")}
        out = []
        for q in C.linhas(self.fonte):
            if status.get(q["uid"]) == "totalmente_sustentado" and q["uid"] in ctx:
                txt = "\n\n".join(f"[{b['id']}] {b['texto']}" for b in ctx[q["uid"]]["blocos_contexto"])
                out.append((q, txt))
        return out

    def _arq(self, etapa: str, uid: str) -> Path:
        return self.saida / etapa / f"{_nome_arq(uid)}.json"

    def _falha(self, nome: str, exc: Exception) -> None:
        atomic_json(self.saida / "falhas" / f"{nome}.json", {"erro": type(exc).__name__, "mensagem": str(exc)[:800]})

    def _ok(self, nome: str) -> None:
        (self.saida / "falhas" / f"{nome}.json").unlink(missing_ok=True)

    def processar(self, par) -> bool:
        q, blocos_txt = par
        arq_c, arq_a = self._arq("encurtadas", q["uid"]), self._arq("auditoria", q["uid"])
        if not arq_c.exists():
            nome = f"encurtar_{_nome_arq(q['uid'])}"
            user = json.dumps({"pergunta": q["pergunta"], "resposta_referencia": q["resposta"], "blocos": blocos_txt},
                              ensure_ascii=False)
            try:
                d = self.cliente("encurtar").json(C.prompt("encurtar_gabarito"), user, tag="antigo_encurtar",
                                                  max_tokens=4000, item=q["item"], validate=validar_curta)
            except Exception as exc:  # noqa: BLE001 - isolada por questão
                if not _filtrado(exc):
                    self._falha(nome, exc)
                    return False
                d = None
            atomic_json(arq_c, {"uid": q["uid"], "curta": d})
            self._ok(nome)
        curta = read_json(arq_c)["curta"]
        if curta is None or arq_a.exists():
            return True
        nome = f"auditoria_{_nome_arq(q['uid'])}"
        user = json.dumps({"tipo_declarado": q["tipo"], "pergunta": q["pergunta"], "resposta_referencia": curta["resposta"],
                           "explicacao_do_autor": curta["explicacao"], "blocos": blocos_txt}, ensure_ascii=False)
        try:
            d = self.cliente("auditoria").json(C.prompt("auditoria_v23"), user, tag="antigo_auditoria", max_tokens=6000,
                                               item=q["item"], validate=validar_auditoria)
            rec = {"uid": q["uid"], **veredito(d, q["tipo"])}
        except Exception as exc:  # noqa: BLE001
            if not _filtrado(exc):
                self._falha(nome, exc)
                return False
            rec = {"uid": q["uid"], "aprovada": False, "motivo": "bloqueio", "falhas": ["bloqueio"]}
        atomic_json(arq_a, rec)
        self._ok(nome)
        return True

    def run(self) -> int:
        cfg = {"schema": "banco-antigo-filtrado-v1", "fonte": C.relativo(self.fonte), "gap": C.relativo(self.gap),
               "modelos": self.modelos,
               "prompts_sha256": {n: C.sha(C.prompt(n)) for n in ("encurtar_gabarito", "auditoria_v23")}}
        arq_cfg = self.saida / "config.json"
        old = read_json(arq_cfg) if arq_cfg.exists() else None
        if old is not None and {k: v for k, v in old.items() if k != "criado_em"} != cfg:
            raise ValueError("Configuração diferente da pasta existente; use outra saída")
        atomic_json(self.saida / "config.json", {**cfg, "criado_em": (old or {}).get("criado_em")
                                                 or datetime.now(timezone.utc).isoformat()})
        pares = self.candidatas()
        self.progress(f"[antigo] {len(pares)} questões sustentadas para encurtar e auditar", flush=True)
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            falhas = sum(not ok for ok in pool.map(self.processar, pares))
        res = self.relatorio(pares)
        marcador = self.saida / "filtro_concluido.json"
        if falhas:
            marcador.unlink(missing_ok=True)
        else:
            atomic_json(marcador, {"em": datetime.now(timezone.utc).isoformat(), "aprovadas": res["aprovadas"]})
        return falhas

    def relatorio(self, pares) -> dict:
        aprovadas, auditadas, falhas_aud = [], 0, Counter()
        for q, _ in pares:
            c, a = self._arq("encurtadas", q["uid"]), self._arq("auditoria", q["uid"])
            if not (c.exists() and a.exists()):
                continue
            curta, aud = read_json(c)["curta"], read_json(a)
            auditadas += 1
            falhas_aud.update(aud.get("falhas", []))
            if aud.get("aprovada"):
                aprovadas.append({**{k: v for k, v in q.items() if k != "auditoria"}, "resposta": curta["resposta"],
                                  "explicacao": curta["explicacao"], "resposta_original": q["resposta"],
                                  "auditoria_antiga": q.get("auditoria"), "auditoria": aud,
                                  "tipo": aud.get("tipo_sugerido", q["tipo"])})
        C.gravar_jsonl(self.saida / "aprovadas.jsonl", aprovadas)
        cont = lambda chave: dict(sorted(Counter(chave(q) for q in aprovadas).items()))  # noqa: E731
        res = {"sustentadas": len(pares), "auditadas": auditadas, "aprovadas": len(aprovadas),
               "taxa_aprovacao": round(100 * len(aprovadas) / auditadas, 1) if auditadas else None,
               "falhas_auditor": dict(falhas_aud.most_common()), "por_tipo": cont(lambda q: q["tipo"]),
               "por_origem": cont(lambda q: "refinada" if ":ref" in q["uid"] else q["origem"]),
               "por_topico": cont(lambda q: q["item"]),
               "pendentes": sorted(p.stem for p in (self.saida / "falhas").glob("*.json"))}
        atomic_json(self.saida / "resultado.json", res)
        l = ["# Banco antigo filtrado (auditor v23)", "",
             f"{res['aprovadas']} aprovadas de {res['auditadas']} auditadas ({res['taxa_aprovacao']}%), entre "
             f"{res['sustentadas']} questões com gabarito totalmente sustentado.", "",
             f"Falhas do auditor por verificação: {res['falhas_auditor']}.", f"Por tipo: {res['por_tipo']}.",
             f"Por origem: {res['por_origem']}.", f"Por tópico: {res['por_topico']}.",
             f"Falhas pendentes: {len(res['pendentes'])}.", "",
             "Gabarito reduzido ao elemento decisivo (`resposta`); o original fica em `resposta_original`."]
        (self.saida / "RELATORIO.md").write_text("\n".join(l), encoding="utf-8")
        return res


def avaliar(saida: Path = AVALIACAO, filtro: Path = SAIDA, workers=8, judge_workers=2,
            mini="gpt-4-1-mini-petrobras") -> int:
    """Mesmo protocolo do benchmark_gap_full_v1 (contexto = blocos de geração), sobre o banco filtrado."""
    from pipeline.qa_research import benchmark_gap as G
    if not (Path(filtro) / "filtro_concluido.json").exists():
        raise ValueError("Filtro do banco antigo ainda não concluído; repita o comando antigo")
    return G.executar(Path(saida), source=Path(filtro) / "aprovadas.jsonl", workers=workers,
                      judge_workers=judge_workers, mini=mini)
