"""Experimento de refino: um refinador forte recupera mais questões reprovadas do que o fraco?

Parte de uma rodada já auditada (por padrão o piloto v19) e não gera nada novo. Pega as questões originais
(janela e compostas) reprovadas pelo auditor e, para cada braço (modelo do refinador):

  1. refino com o prompt `refinador_v3.md`: motivo e justificativa do auditor, blocos de origem, dois exemplos
     aprovados do mesmo tipo (de outros tópicos) e, a partir da 2ª rodada, o histórico das versões reprovadas;
     cobre todos os motivos (também trivial, prudência genérica, sim ou não disfarçado e tecnicamente errada) e
     pode mudar o tipo;
  2. validação em código (forma, regras do tipo, referência à fonte, mudança só cosmética);
  3. nova auditoria (auditor v3, com o texto-fonte);
  4. rodadas seguintes só para as que voltaram a ser reprovadas;
  5. ganho líquido: deduplicação por sentido entre as aprovadas da rodada de origem e as recuperadas.

Saídas: `REFINO.md` e `resultado.json` na pasta do experimento.
"""
from __future__ import annotations

import hashlib
import json
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pipeline.qa_research.piloto_janela.core import QA, ROOT, atomic_json, janela, read_json
from pipeline.qa_research.tipos import TIPOS, problemas_tipo

from .core import EXEMPLOS, _texto, carregar_banco, prompt
from .rodadas import (BANCO_INICIAL, MODELOS, PROMPT_AUDITORIA, GeracaoMeta, _filtrado, _h, _nome_arq,
                      mudanca_cosmetica, validar_auditoria, validar_refino_v3)

ORIGEM = QA / "relatorios" / "teste_v19_20261024T053346Z" / "geracao"
BRACOS = {"mini": "gpt-5-mini-petrobras:medium", "forte": "gpt-5-4-petrobras:high"}
# Braços com sufixo "_cob" recebem as questões já aprovadas sobre os mesmos blocos (<ja_cobertas>).
MODELOS_BRACO = {"mini": BRACOS["mini"], "forte": BRACOS["forte"], "mini_cob": BRACOS["mini"], "forte_cob": BRACOS["forte"]}
CHAVES = {"status", "motivo", "tipo", "cenario", "pergunta", "resposta"}


class ExperimentoRefino:
    def __init__(self, saida: Path, *, origem: Path = ORIGEM, bracos: dict | None = None, rodadas: int = 2,
                 auditor: str = MODELOS["auditoria"], workers: int = 8, lote: int = 10, clientes: dict | None = None,
                 banco_inicial=BANCO_INICIAL, exemplos: Path = EXEMPLOS, progress=print):
        self.saida, self.origem = Path(saida), Path(origem)
        self.bracos = dict(bracos or BRACOS)
        self.rodadas, self.auditor, self.workers, self.lote = rodadas, auditor, workers, lote
        self.clientes, self.progress, self.lock = dict(clientes or {}), progress, threading.Lock()
        cfg = read_json(self.origem / "config.json")
        self.g = GeracaoMeta(self.origem, cfg["itens"], banco_inicial=banco_inicial, exemplos=exemplos,
                             progress=lambda *a, **k: None)
        self.itens = cfg["itens"]
        self.base = carregar_banco(exemplos)
        din = self.g._dinamico()
        self.pool_exemplos = [e for e in self.base["exemplos"] + din["aprovadas"] if e.get("tipo") in TIPOS]
        self.questoes = {i: self.g.questoes(i) for i in self.itens}

    # ---------------------------------------------------------------- infraestrutura
    def cliente(self, papel: str, modelo: str):
        with self.lock:
            if papel not in self.clientes:
                from pipeline.inventario.llm import LLMClient, load_dotenv
                load_dotenv(ROOT)
                model, effort = modelo.rsplit(":", 1) if ":" in modelo else (modelo, "")
                self.clientes[papel] = LLMClient(
                    model, effort, self.saida / ".local" / f"{papel}.sqlite3", self.saida / "chamadas" / f"{papel}.jsonl",
                    provider="azure", max_attempts=3, timeout=600, max_tokens_cap=32000, max_calls=100000,
                    response_dir=self.saida / ".local" / "respostas" / papel)
            return self.clientes[papel]

    def _paralelo(self, tarefas, funcao, rotulo: str) -> int:
        if not tarefas:
            return 0
        falhas = 0
        with ThreadPoolExecutor(max_workers=max(1, self.workers)) as pool:
            for k, ok in enumerate(pool.map(funcao, tarefas), 1):
                falhas += 0 if ok else 1
                if k % 20 == 0 or k == len(tarefas):
                    self.progress(f"  {rotulo}: {k}/{len(tarefas)} | falhas {falhas}", flush=True)
        return falhas

    def _falha(self, nome: str, exc: Exception) -> None:
        atomic_json(self.saida / "falhas" / f"{nome}.json", {"erro": type(exc).__name__, "mensagem": str(exc)[:2000]})

    def _ok(self, nome: str) -> None:
        f = self.saida / "falhas" / f"{nome}.json"
        if f.exists():
            f.unlink()

    # ---------------------------------------------------------------- dados
    def candidatas(self) -> list[dict]:
        """Originais (janela e compostas) reprovadas pelo auditor na rodada de origem."""
        return [q for i in self.itens for q in self.questoes[i]
                if q["origem"] in ("janela", "composta") and q.get("auditoria")
                and q["auditoria"].get("motivo") not in ("", "nenhum")]

    def aprovadas_origem(self, item: str) -> list[dict]:
        return [q for q in self.questoes[item] if q.get("aprovada")]

    def _dir(self, braco: str, rodada: int) -> Path:
        return self.saida / braco / f"r{rodada}"

    def versao(self, braco: str, rodada: int, uid: str) -> dict | None:
        arq = self._dir(braco, rodada) / "refinadas" / f"{_nome_arq(uid)}.json"
        return read_json(arq) if arq.exists() else None

    def auditorias(self, braco: str, rodada: int) -> dict:
        return {a["uid"]: a for p in (self._dir(braco, rodada) / "auditoria").glob("*.json")
                for a in read_json(p)["avaliacoes"]}

    def exemplos_para(self, q: dict, tipo: str) -> str:
        pool = [e for e in self.pool_exemplos if e["tipo"] == tipo and e.get("item") != q["item"]]
        escolhidos = sorted(pool, key=lambda e: _h("ref", q["uid"], e.get("id", e["pergunta"])))[:2]
        return "\n\n".join(f"Pergunta: {e['pergunta']}\nResposta: {e['resposta']}" for e in escolhidos)

    def blocos_de(self, q: dict) -> set:
        if q.get("foco") is not None:
            return {b["indice"] for _, b in janela(self.g.docs[q["item"]], q["foco"])}
        return set(q.get("blocos") or [])

    def cobertas(self, braco: str, rodada: int, q: dict) -> list[dict]:
        """Aprovadas que tocam os mesmos blocos: as da origem e as recuperadas pelo braço nas rodadas anteriores."""
        alvo = self.blocos_de(q)
        cands = list(self.aprovadas_origem(q["item"]))
        orig = {c["uid"]: c for c in self.candidatas()}
        for r in range(1, rodada):
            aud = self.auditorias(braco, r)
            for uid, a in aud.items():
                v = self.versao(braco, r, uid)
                if a["motivo"] == "nenhum" and v and uid != q["uid"] and orig.get(uid, {}).get("item") == q["item"]:
                    cands.append({**orig[uid], "pergunta": v["pergunta"], "resposta": v["resposta"]})
        return [c for c in cands if self.blocos_de(c) & alvo]

    def _estado(self, braco: str, rodada: int, q: dict) -> tuple[dict, dict, list]:
        """Versão a refinar nesta rodada, a revisão dela e o histórico das anteriores."""
        atual = {"tipo": q["tipo"] if q["tipo"] in TIPOS else q["auditoria"]["tipo_sugerido"],
                 "pergunta": q["pergunta"], "resposta": q["resposta"]}
        revisao, historico = q["auditoria"], []
        for r in range(1, rodada):
            v = self.versao(braco, r, q["uid"])
            a = self.auditorias(braco, r).get(q["uid"])
            historico.append((atual, revisao))
            atual, revisao = {"tipo": v["tipo"], "pergunta": v["pergunta"], "resposta": v["resposta"]}, a
        return atual, revisao, historico

    # ---------------------------------------------------------------- etapas
    def pendentes(self, braco: str, rodada: int) -> list[dict]:
        """Rodada 1: todas as candidatas. Depois: as que a rodada anterior refinou e o auditor reprovou."""
        cands = self.candidatas()
        if rodada == 1:
            return cands
        aud = self.auditorias(braco, rodada - 1)
        out = []
        for q in cands:
            v = self.versao(braco, rodada - 1, q["uid"])
            a = aud.get(q["uid"])
            if v and v["status"] == "ok" and a and a["motivo"] != "nenhum":
                out.append(q)
        return out

    def refinar(self, braco: str, rodada: int) -> int:
        tarefas = [q for q in self.pendentes(braco, rodada) if not self.versao(braco, rodada, q["uid"])]
        self.progress(f"   refinador {braco} ({self.bracos[braco]}), rodada {rodada}: {len(tarefas)} questões", flush=True)
        system = prompt("refinador_v3")

        def um(q):
            atual, revisao, historico = self._estado(braco, rodada, q)
            partes = [f"<questao>\nTipo: {atual['tipo']}\nPergunta: {atual['pergunta']}\nResposta: {atual['resposta']}\n</questao>",
                      f"<revisao>\nMotivo: {revisao['motivo']}\nJustificativa: {revisao['justificativa']}\n</revisao>"]
            if historico:
                partes.append("<historico>\n" + "\n\n".join(
                    f"Versão {k}: {v['pergunta']} → {v['resposta']}\nReprovada por {a['motivo']}: {a['justificativa']}"
                    for k, (v, a) in enumerate(historico, 1)) + "\n</historico>")
            if braco.endswith("_cob"):
                cob = self.cobertas(braco, rodada, q)
                partes.append("<ja_cobertas>\n" + ("\n".join(f"- {c['pergunta']} → {c['resposta']}" for c in cob)
                                                     or "(nenhuma)") + "\n</ja_cobertas>")
            partes += [f"<exemplos_aprovados>\n{self.exemplos_para(q, atual['tipo'])}\n</exemplos_aprovados>",
                       f"<blocos>\n{self.g._blocos_da_questao(q)}\n</blocos>"]
            nome = f"refino_{braco}_r{rodada}_{_nome_arq(q['uid'])}"
            try:
                d = self.cliente(f"refinador_{braco}", self.bracos[braco]).json(
                    system, "\n\n".join(partes), tag="refino_forte", max_tokens=12000, item=q["item"],
                    validate=lambda d: validar_refino_v3(d, atual["tipo"], atual))
            except Exception as exc:  # noqa: BLE001
                if not _filtrado(exc):
                    self._falha(nome, exc)
                    return False
                d = {"status": "descartar", "motivo": "bloqueado pelo filtro de conteúdo", "tipo": atual["tipo"],
                     "cenario": False, "pergunta": "", "resposta": ""}
            atomic_json(self._dir(braco, rodada) / "refinadas" / f"{_nome_arq(q['uid'])}.json",
                        {"original": q["uid"], "item": q["item"], "motivo_anterior": revisao["motivo"], **d})
            self._ok(nome)
            return True

        return self._paralelo(tarefas, um, f"refino {braco} r{rodada}")

    def auditar(self, braco: str, rodada: int) -> int:
        feitas = self.auditorias(braco, rodada)
        pend = []
        for q in self.pendentes(braco, rodada):
            v = self.versao(braco, rodada, q["uid"])
            if v and v["status"] == "ok" and q["uid"] not in feitas:
                pend.append((q, v))
        pend.sort(key=lambda x: _h("aud", braco, x[0]["uid"]))
        lotes = [pend[i:i + self.lote] for i in range(0, len(pend), self.lote)]
        self.progress(f"   auditoria {braco}, rodada {rodada}: {len(pend)} questões", flush=True)
        system = prompt(PROMPT_AUDITORIA)

        def um(lote):
            ids = [f"Q{k}" for k in range(1, len(lote) + 1)]
            itens = [{"id": i, "tipo_declarado": v["tipo"], "pergunta": v["pergunta"], "resposta_referencia": v["resposta"],
                      "texto_fonte": self.g._blocos_da_questao(q)} for i, (q, v) in zip(ids, lote)]
            nome = hashlib.sha256("|".join(q["uid"] for q, _ in lote).encode()).hexdigest()[:16]
            try:
                d = self.cliente("auditoria", self.auditor).json(
                    system, json.dumps(itens, ensure_ascii=False), tag="refino_auditoria", max_tokens=16000,
                    validate=lambda d: validar_auditoria(d, ids))
            except Exception as exc:  # noqa: BLE001
                self._falha(f"auditoria_{braco}_r{rodada}_{nome}", exc)
                return False
            atomic_json(self._dir(braco, rodada) / "auditoria" / f"{nome}.json",
                        {"avaliacoes": [{**a, "uid": q["uid"]} for a, (q, _) in zip(d["avaliacoes"], lote)]})
            self._ok(f"auditoria_{braco}_r{rodada}_{nome}")
            return True

        return self._paralelo(lotes, um, f"auditoria {braco} r{rodada}")

    def recuperadas(self, braco: str) -> list[dict]:
        """Versão aprovada de cada candidata (a da primeira rodada em que o auditor aprovou)."""
        out = []
        for q in self.candidatas():
            for r in range(1, self.rodadas + 1):
                v, a = self.versao(braco, r, q["uid"]), self.auditorias(braco, r).get(q["uid"])
                if v and v["status"] == "ok" and a and a["motivo"] == "nenhum":
                    out.append({"uid": q["uid"] + f":{braco}", "item": q["item"], "rodada_refino": r,
                                "motivo_original": q["auditoria"]["motivo"], "origem_original": q["origem"],
                                "tipo_original": q["tipo"], "pergunta_original": q["pergunta"],
                                "resposta_original": q["resposta"], "tipo": a.get("tipo_sugerido") or v["tipo"],
                                "cenario": v["cenario"], "pergunta": v["pergunta"], "resposta": v["resposta"],
                                "justificativa_auditor": a["justificativa"]})
                    break
        return out

    def deduplicar(self, braco: str) -> int:
        """Ganho líquido: dedup por sentido entre as aprovadas da origem e as recuperadas do braço, por tópico."""
        system, falhas = prompt("dedup"), 0
        rec = self.recuperadas(braco)
        for item in self.itens:
            arq = self.saida / braco / f"dedup_{item}.json"
            base = [{"uid": q["uid"], "pergunta": q["pergunta"], "resposta": q["resposta"]} for q in self.aprovadas_origem(item)]
            novas = [q for q in rec if q["item"] == item]
            todas = base + novas
            uids = sorted(q["uid"] for q in todas)
            if arq.exists() and read_json(arq).get("consideradas") == uids:
                continue
            if not novas:
                atomic_json(arq, {"consideradas": uids, "grupos": []})
                continue
            ids = {f"Q{k}": q for k, q in enumerate(todas, 1)}
            user = json.dumps([{"id": i, "pergunta": q["pergunta"], "resposta": q["resposta"]} for i, q in ids.items()],
                              ensure_ascii=False)

            def validar(d, ids=ids):
                gs = d.get("grupos") if isinstance(d, dict) else None
                if not isinstance(gs, list):
                    raise ValueError('Retorne {"grupos": [...]}.')
                vistos = set()
                for g in gs:
                    if not isinstance(g, dict) or g.get("manter") not in ids or not isinstance(g.get("remover"), list) \
                            or any(r not in ids for r in g["remover"]):
                        raise ValueError("Cada grupo precisa de 'manter' e 'remover' com ids recebidos.")
                    membros = [g["manter"], *g["remover"]]
                    if vistos & set(membros) or len(set(membros)) != len(membros):
                        raise ValueError("Cada id aparece em no máximo um grupo.")
                    vistos |= set(membros)

            try:
                d = self.cliente("auditoria", self.auditor).json(system, user, tag="refino_dedup", max_tokens=16000,
                                                                 item=item, validate=validar)
            except Exception as exc:  # noqa: BLE001
                self._falha(f"dedup_{braco}_{item}", exc)
                falhas += 1
                continue
            atomic_json(arq, {"consideradas": uids, "grupos": [
                {"manter": ids[g["manter"]]["uid"], "remover": [ids[r]["uid"] for r in g["remover"]],
                 "motivo": g.get("motivo", "")} for g in d["grupos"] if g["remover"]]})
            self._ok(f"dedup_{braco}_{item}")
        return falhas

    # ---------------------------------------------------------------- execução
    def run(self) -> int:
        atomic_json(self.saida / "config.json", {"schema": "refino-forte-v1", "origem": str(self.origem),
                                                 "bracos": self.bracos, "rodadas": self.rodadas, "auditor": self.auditor,
                                                 "itens": self.itens})
        self.progress(f"Candidatas (reprovadas na origem): {len(self.candidatas())}", flush=True)
        falhas = 0
        for braco in self.bracos:
            for r in range(1, self.rodadas + 1):
                falhas += self.refinar(braco, r)
                falhas += self.auditar(braco, r)
            falhas += self.deduplicar(braco)
        self.relatorio()
        return falhas

    def relatorio(self) -> dict:
        cands = self.candidatas()
        por_motivo = Counter(q["auditoria"]["motivo"] for q in cands)
        base = {i: len(self.aprovadas_origem(i)) for i in self.itens}
        ref = [q for i in self.itens for q in self.questoes[i] if q["origem"] == "refinada"]
        try:
            origem = str(self.origem.resolve().relative_to(ROOT.resolve()))
        except ValueError:
            origem = str(self.origem)
        res = {"origem": origem, "candidatas": len(cands), "candidatas_por_motivo": dict(por_motivo),
               "aprovadas_origem": base, "bracos": {},
               "refinador_da_origem": {"reescritas": len(ref), "aprovadas": sum(1 for q in ref if q.get("aprovada"))}}
        for braco, modelo in self.bracos.items():
            rodadas = []
            for r in range(1, self.rodadas + 1):
                pend = self.pendentes(braco, r)
                vs = [self.versao(braco, r, q["uid"]) for q in pend]
                aud = self.auditorias(braco, r)
                ok = [v for v in vs if v and v["status"] == "ok"]
                rodadas.append({"rodada": r, "tentadas": len(pend), "descartadas": sum(1 for v in vs if v and v["status"] == "descartar"),
                                "reescritas": len(ok), "aprovadas": sum(1 for v in ok if aud.get(v["original"], {}).get("motivo") == "nenhum"),
                                "motivos_auditor": dict(Counter(aud[v["original"]]["motivo"] for v in ok if v["original"] in aud))})
            rec = self.recuperadas(braco)
            nova_por_rodada, dup_por_rodada, liquido = Counter(), Counter(), {}
            por_uid = {q["uid"]: q for q in rec}
            for item in self.itens:
                arq = self.saida / braco / f"dedup_{item}.json"
                grupo = {}
                for g in (read_json(arq)["grupos"] if arq.exists() else []):
                    membros = [g["manter"], *g["remover"]]
                    com_base = any(u not in por_uid for u in membros)
                    for u in membros:
                        grupo[u] = (com_base, g["manter"])
                liquido[item] = 0
                for q in rec:
                    if q["item"] != item:
                        continue
                    com_base, manter = grupo.get(q["uid"], (False, q["uid"]))
                    # nova = conhecimento que as aprovadas da origem não cobrem (uma por grupo de recuperadas)
                    nova = not com_base and manter == q["uid"]
                    (nova_por_rodada if nova else dup_por_rodada)[q["rodada_refino"]] += 1
                    liquido[item] += nova
            res["bracos"][braco] = {
                "modelo": modelo, "rodadas": rodadas, "recuperadas": len(rec),
                "recuperadas_por_motivo": {m: f"{sum(q['motivo_original'] == m for q in rec)}/{n}" for m, n in por_motivo.items()},
                "recuperadas_por_origem": dict(Counter(q["origem_original"] for q in rec)),
                "tipo_mudou": sum(q["tipo"] != q["tipo_original"] for q in rec),
                "ganho_liquido_por_topico": liquido, "ganho_liquido": sum(liquido.values()),
                "novas_por_rodada": dict(nova_por_rodada), "repetem_aprovadas_por_rodada": dict(dup_por_rodada)}
            with (self.saida / braco / "recuperadas.jsonl").open("w", encoding="utf-8") as f:
                for q in rec:
                    f.write(json.dumps(q, ensure_ascii=False) + "\n")
        atomic_json(self.saida / "resultado.json", res)
        self._markdown(res)
        return res

    def _markdown(self, res: dict) -> None:
        total = sum(res["aprovadas_origem"].values())
        L = ["# Experimento de refino: refinador fraco x forte", "",
             f"Origem: `{res['origem']}` ({total} aprovadas). Candidatas: {res['candidatas']} originais reprovadas pelo "
             f"auditor, por motivo: {res['candidatas_por_motivo']}.",
             "Prompt `refinador_v3.md` (todos os motivos, histórico das versões reprovadas, exemplos aprovados do mesmo "
             "tipo); nova auditoria com o auditor v3 e o texto-fonte; ganho líquido depois da deduplicação por sentido "
             "contra as aprovadas da origem: conta só a recuperada com conhecimento que as aprovadas não cobrem (uma por "
             "grupo de recuperadas equivalentes). Braços `_cob` recebem as aprovadas sobre os mesmos blocos.", "",
             "| Braço | modelo | recuperadas | ganho líquido | por rodada (aprov./reescritas/tentadas, descartadas) |",
             "|---|---|---|---|---|"]
        for b, d in res["bracos"].items():
            rod = "; ".join(f"r{r['rodada']}: {r['aprovadas']}/{r['reescritas']}/{r['tentadas']}, desc. {r['descartadas']}"
                            for r in d["rodadas"])
            L.append(f"| {b} | {d['modelo']} | {d['recuperadas']}/{res['candidatas']} | **{d['ganho_liquido']}** "
                     f"({total} → {total + d['ganho_liquido']}) | {rod} |")
        ro = res["refinador_da_origem"]
        L += ["", f"Referência: na rodada de origem, o refinador antigo (gpt-5-mini, prompt v19, só motivos recuperáveis) "
                  f"teve {ro['aprovadas']} aprovadas de {ro['reescritas']} reescritas, já descontadas a deduplicação e a "
                  "revisão manual.", ""]
        for b, d in res["bracos"].items():
            L += [f"## {b}", "", f"- Recuperadas por motivo original: {d['recuperadas_por_motivo']}",
                  f"- Por origem: {d['recuperadas_por_origem']}; tipo mudou em {d['tipo_mudou']}",
                  f"- Ganho líquido por tópico: {d['ganho_liquido_por_topico']}",
                  f"- Conhecimento novo por rodada: {d['novas_por_rodada']}; repetem conhecimento já aprovado: "
                  f"{d['repetem_aprovadas_por_rodada']}"]
            for r in d["rodadas"]:
                L.append(f"- Rodada {r['rodada']}, motivos do auditor nas reescritas: {r['motivos_auditor']}")
            L += ["", "### Amostra de recuperadas", ""]
            rec = [json.loads(l) for l in (self.saida / b / "recuperadas.jsonl").read_text(encoding="utf-8").splitlines() if l]
            for q in sorted(rec, key=lambda q: _h("am", q["uid"]))[:15]:
                L += [f"**[{q['item']} · {q['motivo_original']} · {q['tipo_original']} → {q['tipo']} · r{q['rodada_refino']}]**",
                      f"- Antes: {q['pergunta_original']} → {q['resposta_original']}",
                      f"- Depois: {q['pergunta']} → {q['resposta']}", ""]
        (self.saida / "REFINO.md").write_text("\n".join(L), encoding="utf-8")
