"""Geração híbrida por tipo de questão (ver pipeline/qa_research/TIPOS_QUESTAO.md).

  - Janela (EC, prompt v14): por janela de 3 blocos, 4 questões simples, 1 conceito, 1 mecanismo ou
    consequência, 1 diagnóstico, decisão ou procedimento e 1 livre.
  - Compostas: uma questão por encadeamento do inventário (relações de blocos diferentes ligadas por
    uma ponte oculta), já extraídos no piloto de dificuldade v2.
  - Auditoria: um juiz forte confere o tipo, a validade da referência e atalhos.
  - Reclassificação: aplica os tipos às questões já avaliadas no piloto v2 e cruza com a acurácia.

Tudo é retomável: cada janela, encadeamento ou lote vira um arquivo.
"""
from __future__ import annotations

import csv
import hashlib
import json
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from pipeline.qa_research.piloto_janela.core import (QA, ROOT, atomic_json, blocos, carregar_prompt, janela,
                                                     palavras, preencher, quase_duplicadas, read_json,
                                                     selecionar_focos, sha, tema, verificar)
from pipeline.qa_research.tipos import TIPOS, problemas_composicao, problemas_tipo

AQUI = Path(__file__).resolve().parent
PROMPTS = AQUI / "prompts"
PROMPT_JANELA = QA / "prompt_janela_qa_14.md"
ITENS = ("01_01", "02_02")
ENCADEAMENTOS = QA / "relatorios" / "piloto_dificuldade_20261023T053615Z"
MODELOS = {"geracao": "gpt-5-4-petrobras:high", "auditoria": "gpt-5-4-petrobras:high"}
CAMPOS = ("id", "tipo", "cenario", "conhecimento", "pergunta", "resposta", "fundamentos")
ROTULOS = ("A1", "F", "A2")
TIPOS_COMPOSTA = tuple(t for t in TIPOS if t != "conceito")
V = {"correta": 1.0, "parcial": 0.5, "incorreta": 0.0}


def prompt(nome: str) -> str:
    return (PROMPTS / f"{nome}.md").read_text(encoding="utf-8").strip()


def _texto(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


# ---------------------------------------------------------------- validações
def validar_janela(d: dict) -> None:
    if not isinstance(d, dict) or set(d) != {"status", "motivo", "questoes"}:
        raise ValueError("Use exatamente as chaves status, motivo e questoes.")
    if d["status"] not in ("ok", "parcial", "sem_questoes") or not isinstance(d["questoes"], list) \
            or not isinstance(d["motivo"], str):
        raise ValueError("status deve ser ok, parcial ou sem_questoes; motivo, texto; questoes, lista.")
    problemas = []
    for k, q in enumerate(d["questoes"], 1):
        if not isinstance(q, dict) or set(q) != set(CAMPOS):
            raise ValueError(f"Questão {k}: use exatamente os campos {', '.join(CAMPOS)}.")
        if q["id"] != k:
            raise ValueError(f"Questão {k}: id deve ser {k}.")
        for campo in ("conhecimento", "pergunta", "resposta"):
            if not _texto(q[campo]):
                raise ValueError(f"Questão {k}: {campo} vazio.")
        fs = q["fundamentos"]
        if not isinstance(fs, list) or not fs or any(
                not isinstance(f, dict) or set(f) != {"bloco", "trecho"} or f["bloco"] not in ROTULOS
                or not _texto(f["trecho"]) for f in fs):
            raise ValueError(f'Questão {k}: fundamentos deve ser lista de {{"bloco": A1|F|A2, "trecho": texto}}.')
        problemas += [f"Questão {k} ({q['tipo']}): {m}." for m in
                      problemas_tipo(q["tipo"], q["cenario"], q["pergunta"], q["resposta"])]
    problemas += [m[0].upper() + m[1:] + "." for m in
                  problemas_composicao(d["status"], [q["tipo"] for q in d["questoes"]], d["motivo"])]
    if problemas:
        raise ValueError(" ".join(problemas) + " Corrija ou descarte a questão (use parcial e explique em motivo).")


def validar_composta(d: dict) -> None:
    if not isinstance(d, dict) or set(d) != {"status", "motivo", "tipo", "cenario", "pergunta", "resposta"}:
        raise ValueError("Use exatamente as chaves status, motivo, tipo, cenario, pergunta e resposta.")
    if d["status"] == "insuficiente":
        if not _texto(d["motivo"]):
            raise ValueError("insuficiente exige motivo.")
        return
    if d["status"] != "ok" or not (_texto(d["pergunta"]) and _texto(d["resposta"])):
        raise ValueError("status deve ser ok (com pergunta e resposta) ou insuficiente.")
    if d["tipo"] not in TIPOS_COMPOSTA:
        raise ValueError(f"tipo de questão composta deve ser um de: {', '.join(TIPOS_COMPOSTA)}.")
    p = problemas_tipo(d["tipo"], d["cenario"], d["pergunta"], d["resposta"])
    if p:
        raise ValueError("Corrija: " + "; ".join(p) + ". Se não for possível, use insuficiente.")


def validar_lote(d: dict, ids: list[str], chave: str, campos_bool: tuple, campo_tipo: str) -> None:
    av = d.get(chave) if isinstance(d, dict) else None
    if not isinstance(av, list) or [a.get("id") for a in av] != ids:
        raise ValueError("Devolva exatamente um objeto por id recebido, na mesma ordem.")
    for a in av:
        if a.get(campo_tipo) not in TIPOS:
            raise ValueError(f"{campo_tipo} deve ser um de: {', '.join(TIPOS)}.")
        if any(not isinstance(a.get(c), bool) for c in campos_bool):
            raise ValueError(f"{', '.join(campos_bool)} devem ser booleanos.")


# ---------------------------------------------------------------- execução
class Geracao:
    def __init__(self, saida: Path, *, itens=ITENS, ec_janelas: int = 36, encadeamentos: Path | None = ENCADEAMENTOS,
                 modelos: dict | None = None, workers: int = 6, clientes: dict | None = None,
                 limpos: Path | None = None, limite_compostas: int | None = None, lote: int = 10, progress=print):
        self.saida, self.itens, self.ec_janelas = Path(saida), list(itens), ec_janelas
        self.encadeamentos = Path(encadeamentos) if encadeamentos else None
        self.modelos = {**MODELOS, **(modelos or {})}
        self.workers, self.clientes, self.limpos, self.lote = workers, dict(clientes or {}), limpos, lote
        self.limite_compostas, self.progress = limite_compostas, progress
        self.lock = threading.Lock()
        self.temas = {i: tema(i) for i in self.itens}
        self.docs = {i: blocos(i)[1] for i in self.itens}

    # -- infraestrutura
    def cliente(self, papel: str):
        with self.lock:
            if papel not in self.clientes:
                from pipeline.inventario.llm import LLMClient, load_dotenv
                load_dotenv(ROOT)
                nome = self.modelos[papel]
                model, effort = nome.rsplit(":", 1) if ":" in nome else (nome, "")
                self.clientes[papel] = LLMClient(
                    model, effort, self.saida / ".local" / f"{papel}.sqlite3", self.saida / "chamadas" / f"{papel}.jsonl",
                    provider="azure", max_attempts=3, timeout=600, max_tokens_cap=32000, max_calls=100000,
                    response_dir=self.saida / ".local" / "respostas" / papel)
            return self.clientes[papel]

    def _paralelo(self, tarefas, funcao, rotulo: str) -> int:
        if not tarefas:
            return 0
        feitos, falhas, inicio = 0, 0, time.time()
        with ThreadPoolExecutor(max_workers=max(1, self.workers)) as pool:
            for ok in pool.map(funcao, tarefas):
                feitos += 1
                falhas += 0 if ok else 1
                if feitos % 10 == 0 or feitos == len(tarefas):
                    eta = (time.time() - inicio) / feitos * (len(tarefas) - feitos)
                    self.progress(f"  {rotulo}: {feitos}/{len(tarefas)} | falhas {falhas} | restam ~{eta / 60:.1f} min",
                                  flush=True)
        return falhas

    def _falha(self, pasta: str, nome: str, exc: Exception) -> None:
        atomic_json(self.saida / "falhas" / pasta / f"{nome}.json",
                    {"erro": type(exc).__name__, "mensagem": str(exc)[:2000], "em": datetime.now(timezone.utc).isoformat()})

    def _ok(self, pasta: str, nome: str) -> None:
        f = self.saida / "falhas" / pasta / f"{nome}.json"
        if f.exists():
            f.unlink()

    def config(self) -> None:
        cfg = {"schema": "geracao-tipos-v1", "itens": self.itens, "ec_janelas": self.ec_janelas,
               "modelos": self.modelos, "prompt_janela": PROMPT_JANELA.relative_to(ROOT).as_posix(),
               "prompt_janela_sha256": sha(PROMPT_JANELA.read_text(encoding="utf-8")),
               "encadeamentos": (self.encadeamentos.resolve().relative_to(ROOT).as_posix()
                                 if self.encadeamentos and self.encadeamentos.resolve().is_relative_to(ROOT)
                                 else (str(self.encadeamentos) if self.encadeamentos else None)),
               "limite_compostas": self.limite_compostas}
        path = self.saida / "config.json"
        if path.exists():
            antigo = {k: v for k, v in read_json(path).items() if k != "criado_em"}
            if antigo != cfg:
                diff = sorted(k for k in set(antigo) | set(cfg) if antigo.get(k) != cfg.get(k))
                raise ValueError(f"Configuração diferente da pasta existente ({', '.join(diff)}); use outra --saida")
            return
        atomic_json(path, {**cfg, "criado_em": datetime.now(timezone.utc).isoformat()})

    def _exemplos(self, item: str, semente: int) -> str:
        from pipeline.qa_research.piloto_janela import exemplos as ex
        with self.lock:
            if not hasattr(self, "_pools"):
                self._pools = ex.carregar_limpos(self.limpos)[0]
                self._banco = ex.carregar_especialista()
        return ex.render(ex.exemplos_da_janela("EC", item, semente, self._pools, self._banco))

    # -- 1. janelas (questões simples)
    def janelas(self) -> int:
        system, modelo_usuario, _ = carregar_prompt(4, 4, PROMPT_JANELA)
        tarefas = [(i, f) for i in self.itens for f in selecionar_focos(len(self.docs[i]), self.ec_janelas)]
        pend = [t for t in tarefas if not (self.saida / "janelas" / t[0] / f"{t[1]:03d}.json").exists()]
        self.progress(f"1. janelas (prompt v14): {len(tarefas)} no total, {len(pend)} a gerar", flush=True)

        def um(t):
            item, foco = t
            jan = janela(self.docs[item], foco)
            user = preencher(modelo_usuario, self.temas[item], "", "Nenhuma.", jan, self._exemplos(item, foco))
            try:
                d = self.cliente("geracao").json(system, user, tag="tipos_janela", max_tokens=16000, item=item,
                                                 validate=validar_janela)
            except Exception as exc:  # noqa: BLE001
                self._falha("janelas", f"{item}_{foco:03d}", exc)
                return False
            textos = {r: b["texto"] for r, b in jan}
            b = self.docs[item][foco]
            atomic_json(self.saida / "janelas" / item / f"{foco:03d}.json", {
                "item": item, "foco": foco, "subtitulo": b["subtitulo"], "status": d["status"], "motivo": d["motivo"],
                "janela": [{"rotulo": r, "indice": x["indice"]} for r, x in jan],
                "questoes": [{**q, "verificacoes": verificar(q, textos)} for q in d["questoes"]]})
            self._ok("janelas", f"{item}_{foco:03d}")
            return True

        return self._paralelo(pend, um, "janelas")

    # -- 2. compostas (encadeamentos do inventário)
    def _encadeamentos(self) -> list[dict]:
        if not self.encadeamentos:
            return []
        out = []
        for item in self.itens:
            arq = self.encadeamentos / "combinacoes" / f"{item}.json"
            if not arq.exists():
                continue
            rels = {r["id"]: r for p in sorted((self.encadeamentos / "relacoes" / item).glob("*.json"))
                    for r in read_json(p)["relacoes"]}
            combos = read_json(arq)["combinacoes"][: self.limite_compostas or None]
            out += [{"id": f"{item}:{c['id']}", "item": item, "combinacao": c,
                     "relacoes": [rels[i] for i in c["relacoes"] if i in rels]} for c in combos]
        return out

    def compostas(self) -> int:
        encs = self._encadeamentos()
        pend = [e for e in encs if not (self.saida / "compostas" / f"{e['id'].replace(':', '_')}.json").exists()]
        self.progress(f"2. compostas: {len(encs)} encadeamentos, {len(pend)} a redigir", flush=True)
        system = prompt("composta")

        def um(e):
            c, item = e["combinacao"], e["item"]
            bs = {b["indice"]: b for b in self.docs[item]}
            usados = sorted({r["bloco"] for r in e["relacoes"]})
            blocos_txt = "\n\n".join(f"[bloco {i:03d}] {bs[i]['titulo_capitulo']} / {bs[i]['subtitulo']}\n{bs[i]['texto']}"
                                     for i in usados)
            enc = {k: c[k] for k in ("tipo", "titulo", "ponte", "cadeia", "cenario", "resposta", "resposta_atraente",
                                     "sinal_que_descarta", "condicoes_enunciado", "limites")}
            enc["relacoes"] = [{k: r[k] for k in ("id", "afirmacao", "condicoes", "limites")} for r in e["relacoes"]]
            t_ = self.temas[item]
            semente = int(hashlib.sha256(e["id"].encode()).hexdigest()[:8], 16) % 100000
            user = "\n\n".join(x for x in (
                f"<tema>\nÁrea: {t_['area']}\nTema: {t_['tema']}\n</tema>",
                f"<encadeamento>\n{json.dumps(enc, ensure_ascii=False, indent=2)}\n</encadeamento>",
                self._exemplos(item, semente), f"<blocos>\n{blocos_txt}\n</blocos>") if x)
            nome = e["id"].replace(":", "_")
            try:
                d = self.cliente("geracao").json(system, user, tag="tipos_composta", max_tokens=12000, item=item,
                                                 validate=validar_composta)
            except Exception as exc:  # noqa: BLE001
                self._falha("compostas", nome, exc)
                return False
            atomic_json(self.saida / "compostas" / f"{nome}.json",
                        {"id": e["id"], "item": item, "blocos": usados, "relacoes": [r["id"] for r in e["relacoes"]],
                         "tipo_encadeamento": c["tipo"], **d})
            self._ok("compostas", nome)
            return True

        return self._paralelo(pend, um, "compostas")

    # -- banco unificado
    def banco(self) -> list[dict]:
        out = []
        for p in sorted((self.saida / "janelas").glob("*/*.json")):
            j = read_json(p)
            for q in j["questoes"]:
                out.append({"uid": f"j:{j['item']}-{j['foco']:03d}-{q['id']}", "origem": "janela", "item": j["item"],
                            "foco": j["foco"], "tipo": q["tipo"], "cenario": q["cenario"], "composicao": "simples",
                            "conhecimento": q["conhecimento"], "pergunta": q["pergunta"], "resposta": q["resposta"],
                            "fundamentos": q["fundamentos"], "verificacoes": q["verificacoes"]})
        for p in sorted((self.saida / "compostas").glob("*.json")):
            c = read_json(p)
            if c["status"] == "ok":
                out.append({"uid": f"c:{c['id']}", "origem": "composta", "item": c["item"], "tipo": c["tipo"],
                            "cenario": c["cenario"], "composicao": "composta", "pergunta": c["pergunta"],
                            "resposta": c["resposta"], "blocos": c["blocos"], "relacoes": c["relacoes"]})
        return out

    # -- 3. auditoria
    def auditoria(self) -> int:
        banco = self.banco()
        feitos = {a["uid"] for p in (self.saida / "auditoria").glob("*.json") for a in read_json(p)["avaliacoes"]}
        pend = sorted((q for q in banco if q["uid"] not in feitos),
                      key=lambda q: hashlib.sha256(("aud" + q["uid"]).encode()).hexdigest())
        lotes = [pend[i:i + self.lote] for i in range(0, len(pend), self.lote)]
        self.progress(f"3. auditoria ({self.modelos['auditoria']}): {len(pend)} questões em {len(lotes)} lotes", flush=True)
        system = prompt("auditoria")

        def um(lote):
            ids = [f"Q{k}" for k in range(1, len(lote) + 1)]
            itens = [{"id": i, "tipo_declarado": q["tipo"], "pergunta": q["pergunta"], "resposta_referencia": q["resposta"]}
                     for i, q in zip(ids, lote)]
            nome = hashlib.sha256("|".join(q["uid"] for q in lote).encode()).hexdigest()[:16]
            try:
                d = self.cliente("auditoria").json(
                    system, json.dumps(itens, ensure_ascii=False), tag="tipos_auditoria", max_tokens=12000,
                    validate=lambda d: validar_lote(d, ids, "avaliacoes", ("tipo_confere", "referencia_valida", "atalho"),
                                                    "tipo_sugerido"))
            except Exception as exc:  # noqa: BLE001
                self._falha("auditoria", nome, exc)
                return False
            atomic_json(self.saida / "auditoria" / f"{nome}.json",
                        {"avaliacoes": [{**a, "uid": q["uid"]} for a, q in zip(d["avaliacoes"], lote)]})
            self._ok("auditoria", nome)
            return True

        return self._paralelo(lotes, um, "auditoria")

    # -- 4. reclassificação das questões do piloto v2
    def reclassificar(self, piloto: Path) -> int:
        arq = Path(piloto) / "questoes_avaliadas.csv"
        if not arq.exists():
            self.progress(f"0. reclassificação: {arq} não encontrado; etapa ignorada", flush=True)
            return 0
        linhas = list(csv.DictReader(arq.read_text(encoding="utf-8-sig").splitlines()))
        feitos = {a["id_original"] for p in (self.saida / "reclassificacao").glob("*.json")
                  for a in read_json(p)["classificacoes"]}
        pend = [l for l in linhas if l["id"] not in feitos]
        lotes = [pend[i:i + self.lote] for i in range(0, len(pend), self.lote)]
        self.progress(f"0. reclassificação do piloto v2: {len(pend)} questões em {len(lotes)} lotes", flush=True)
        system = prompt("reclassificar")

        def um(lote):
            ids = [f"Q{k}" for k in range(1, len(lote) + 1)]
            itens = [{"id": i, "pergunta": l["pergunta"], "resposta_referencia": l["resposta"]} for i, l in zip(ids, lote)]
            nome = hashlib.sha256("|".join(l["id"] for l in lote).encode()).hexdigest()[:16]
            try:
                d = self.cliente("auditoria").json(
                    system, json.dumps(itens, ensure_ascii=False), tag="tipos_reclassificar", max_tokens=8000,
                    validate=lambda d: validar_lote(d, ids, "classificacoes",
                                                    ("ambiguo", "cenario", "resposta_dado_especifico"), "tipo"))
            except Exception as exc:  # noqa: BLE001
                self._falha("reclassificacao", nome, exc)
                return False
            atomic_json(self.saida / "reclassificacao" / f"{nome}.json",
                        {"classificacoes": [{**a, "id_original": l["id"]} for a, l in zip(d["classificacoes"], lote)]})
            self._ok("reclassificacao", nome)
            return True

        return self._paralelo(lotes, um, "reclassificação")

    # -- 5. relatório
    def relatorio(self, piloto: Path | None = None) -> dict:
        banco = self.banco()
        aud = {a["uid"]: a for p in (self.saida / "auditoria").glob("*.json") for a in read_json(p)["avaliacoes"]}
        for q in banco:
            if q["uid"] in aud:
                q["auditoria"] = {k: aud[q["uid"]][k] for k in ("tipo_confere", "tipo_sugerido", "referencia_valida",
                                                                 "atalho", "justificativa")}
        with (self.saida / "questoes.jsonl").open("w", encoding="utf-8", newline="\n") as f:
            for q in banco:
                f.write(json.dumps(q, ensure_ascii=False) + "\n")
        janelas = [read_json(p) for p in sorted((self.saida / "janelas").glob("*/*.json"))]
        compostas = [read_json(p) for p in sorted((self.saida / "compostas").glob("*.json"))]

        def resumo(qs):
            n = len(qs)
            a = [q["auditoria"] for q in qs if "auditoria" in q]
            return {"n": n, "cenario": sum(q["cenario"] for q in qs),
                    "palavras_pergunta": round(sum(palavras(q["pergunta"]) for q in qs) / n, 1) if n else None,
                    "palavras_resposta": round(sum(palavras(q["resposta"]) for q in qs) / n, 1) if n else None,
                    "auditadas": len(a), "tipo_confere": sum(x["tipo_confere"] for x in a),
                    "referencia_invalida": sum(not x["referencia_valida"] for x in a),
                    "atalho": sum(x["atalho"] for x in a)}

        res = {"modelos": self.modelos, "janelas": {
            "total": len(janelas), "status": dict(Counter(j["status"] for j in janelas)),
            "combinacoes_de_tipos": dict(Counter("+".join(sorted(q["tipo"] for q in j["questoes"])) for j in janelas)
                                         .most_common(10)),
            "fundamentos_literais": sum(q["verificacoes"]["fundamentos_literais"] for j in janelas for q in j["questoes"]),
            "usa_apoio": sum(q["verificacoes"]["usa_apoio"] for j in janelas for q in j["questoes"])},
            "compostas": {"total": len(compostas), "ok": sum(c["status"] == "ok" for c in compostas),
                          "insuficiente": sum(c["status"] == "insuficiente" for c in compostas)},
            "por_origem_tipo": {o: {t: resumo([q for q in banco if q["origem"] == o and q["tipo"] == t]) for t in TIPOS}
                                for o in ("janela", "composta")},
            "por_origem": {o: resumo([q for q in banco if q["origem"] == o]) for o in ("janela", "composta")},
            "por_item": {i: dict(Counter(q["tipo"] for q in banco if q["item"] == i)) for i in self.itens},
            "confusao_tipo": dict(Counter(f"{q['tipo']}->{q['auditoria']['tipo_sugerido']}" for q in banco
                                          if "auditoria" in q and not q["auditoria"]["tipo_confere"]).most_common(15)),
            "quase_duplicadas": quase_duplicadas(banco)[:30],
            "falhas_pendentes": sorted(p.relative_to(self.saida).as_posix() for p in (self.saida / "falhas").rglob("*.json"))}
        if piloto:
            res["reclassificacao"] = self._tabela_reclassificacao(Path(piloto))
        atomic_json(self.saida / "resultado.json", res)
        campos = ["uid", "origem", "item", "tipo", "cenario", "composicao", "pergunta", "resposta", "tipo_confere",
                  "tipo_sugerido", "referencia_valida", "atalho", "justificativa"]
        with (self.saida / "questoes.csv").open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=campos)
            w.writeheader()
            for q in banco:
                w.writerow({**{k: q.get(k, "") for k in campos}, **q.get("auditoria", {})} | {"justificativa": q.get(
                    "auditoria", {}).get("justificativa", "")})
        self._markdown(res, banco, janelas)
        return res

    def _tabela_reclassificacao(self, piloto: Path) -> dict:
        arq = piloto / "questoes_avaliadas.csv"
        cls = {a["id_original"]: a for p in (self.saida / "reclassificacao").glob("*.json")
               for a in read_json(p)["classificacoes"]}
        if not arq.exists() or not cls:
            return {}
        linhas = [l | {"c": cls[l["id"]]} for l in csv.DictReader(arq.read_text(encoding="utf-8-sig").splitlines()) if l["id"] in cls]

        def bloco(ls):
            n = len(ls)
            return {"n": n, "R1": round(sum(V[l["veredito_R1"]] for l in ls) / n, 2) if n else None,
                    "R2": round(sum(V[l["veredito_R2"]] for l in ls) / n, 2) if n else None,
                    "ref_invalida": sum(l["referencia_valida"] == "False" for l in ls)}

        return {"por_tipo": {t: bloco([l for l in linhas if l["c"]["tipo"] == t]) for t in TIPOS},
                "por_dado_especifico": {str(b): bloco([l for l in linhas if l["c"]["resposta_dado_especifico"] == b])
                                        for b in (True, False)},
                "ambiguas": sum(l["c"]["ambiguo"] for l in linhas),
                "nivel_antigo_x_tipo": {n: dict(Counter(l["c"]["tipo"] for l in linhas if l["nivel"] == n))
                                        for n in ("facil", "media", "dificil")}}

    def _markdown(self, res: dict, banco: list[dict], janelas: list[dict]) -> None:
        l = ["# Geração híbrida por tipo de questão", "",
             "Janela: prompt v14 (1 conceito, 1 mecanismo ou consequência, 1 diagnóstico, decisão ou procedimento, "
             "1 livre). Compostas: uma por encadeamento do inventário. Auditoria: " + f"`{res['modelos']['auditoria']}`.", "",
             f"Janelas: {res['janelas']['total']} ({res['janelas']['status']}); fundamentos literais "
             f"{res['janelas']['fundamentos_literais']}; questões que usam bloco de apoio {res['janelas']['usa_apoio']}. "
             f"Compostas: {res['compostas']}.", "",
             "| Origem | Tipo | n | com cenário | palavras (perg./resp.) | tipo confere | ref. inválida | atalho |",
             "|---|---|---|---|---|---|---|---|"]
        for o in ("janela", "composta"):
            for t in TIPOS + ("**total**",):
                b = res["por_origem"][o] if t == "**total**" else res["por_origem_tipo"][o][t]
                if not b["n"]:
                    continue
                l.append(f"| {o} | {t} | {b['n']} | {b['cenario']} | {b['palavras_pergunta']}/{b['palavras_resposta']} | "
                         f"{b['tipo_confere']}/{b['auditadas']} | {b['referencia_invalida']} | {b['atalho']} |")
        l += ["", f"Tipos por documento: {res['por_item']}.", "",
              f"Combinações de tipos mais comuns por janela: {res['janelas']['combinacoes_de_tipos']}.", "",
              f"Tipo declarado → sugerido pelo auditor (divergências): {res['confusao_tipo']}.", "",
              f"Pares quase duplicados (Jaccard ≥ 0,6): {len(res['quase_duplicadas'])}. "
              f"Falhas pendentes: {len(res['falhas_pendentes'])}.", ""]
        rc = res.get("reclassificacao") or {}
        if rc:
            l += ["## Reclassificação do piloto v2", "",
                  "Acurácia dos respondentes sem contexto (R1 gpt-4-1-nano, R2 gpt-5-4-nano low) por tipo atribuído:", "",
                  "| Tipo | n | R1 | R2 | ref. inválida |", "|---|---|---|---|---|"]
            for t, b in rc["por_tipo"].items():
                if b["n"]:
                    l.append(f"| {t} | {b['n']} | {b['R1']} | {b['R2']} | {b['ref_invalida']} |")
            l += ["", f"Resposta é dado específico (nome, local, parâmetro, prática) x geral: {rc['por_dado_especifico']}.",
                  f"Classificações ambíguas: {rc['ambiguas']}. Nível antigo x tipo: {rc['nivel_antigo_x_tipo']}.", ""]
        motivos = [f"- {j['item']} bloco {j['foco']:03d} ({j['status']}): {j['motivo']}" for j in janelas if j["status"] != "ok"]
        if motivos:
            l += ["## Janelas incompletas", ""] + motivos[:40] + [""]
        l += ["## Exemplos por tipo", ""]
        por_tipo = defaultdict(list)
        for q in banco:
            por_tipo[(q["origem"], q["tipo"])].append(q)
        for (o, t), qs in sorted(por_tipo.items()):
            l.append(f"### {o} · {t} ({len(qs)})")
            l.append("")
            for q in qs[:4]:
                a = q.get("auditoria", {})
                marca = ("" if a.get("tipo_confere", True) else f" · auditor: {a.get('tipo_sugerido')}") + \
                        ("" if a.get("referencia_valida", True) else " · ref. inválida") + (" · atalho" if a.get("atalho") else "")
                l += [f"**{q['uid']}{marca}** {q['pergunta']}", "", f"- Resposta: {q['resposta']}", ""]
        (self.saida / "RELATORIO.md").write_text("\n".join(l), encoding="utf-8")

    def run(self, etapas=("reclassificar", "janelas", "compostas", "auditoria", "relatorio"), piloto: Path | None = None) -> int:
        self.config()
        falhas = 0
        if "reclassificar" in etapas and piloto:
            falhas += self.reclassificar(piloto)
        if "janelas" in etapas:
            falhas += self.janelas()
        if "compostas" in etapas:
            falhas += self.compostas()
        if "auditoria" in etapas:
            falhas += self.auditoria()
        if "relatorio" in etapas:
            self.relatorio(piloto)
        return falhas
