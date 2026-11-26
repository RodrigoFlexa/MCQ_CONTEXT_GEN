"""Verificação final do banco v3: o gabarito está correto e quais respostas devem ser aceitas.

Roda como etapas do banco v3 (banco_v3.py), depois da revisão de unicidade, sobre os representantes revisados e sobre
as questões que a revisão cortou por "outra resposta também correta" (R5), que podem voltar com um gabarito que aceita
mais de uma resposta.

Por questão:
  1. alternativas  GPT-5 (high) recebe SÓ a pergunta, sem gabarito nem documento, e propõe de 1 a 3 respostas que um
                   especialista defenderia, além de consultas de busca em português e inglês
                   (prompts/verif_alternativas.md);
  2. fontes        busca nos corpora técnicos do refino (índices BM25, fusão RRF, PT e EN), independentes do documento
                   de origem; até N_FONTES trechos;
  3. decisão       GPT-5.4 (high) julga o gabarito (correto, discutível, incorreto) com o documento, as fontes externas,
                   as respostas propostas e as respostas dos modelos sem contexto, classifica cada resposta diferente
                   (equivalente, válida e diferente, incorreta) e decide (prompts/verif_decisao.md):
                     manter      um item, com os equivalentes como sinônimos;
                     aceitar     conjunto fechado de até 3 itens (modo "qualquer"), cada um com sinônimos;
                     reescrever  nova versão do enunciado (ou do gabarito, se ele era abstrato); a reescrita volta ao
                                 auditor, à sustentação e, no banco, à avaliação, à revisão e a esta verificação (sem
                                 nova reescrita);
                     descartar   gabarito errado, conjunto aberto, gabarito abstrato ou dependente do documento.
                   Perguntas que pedem mais de um elemento ("Quais...") usam o modo "todas": até 3 itens, todos
                   exigidos, cada um com sinônimos. A resposta padrão nunca entra no gabarito.
  4. rejulgamento  as respostas dos modelos (com e sem contexto) são julgadas de novo contra o gabarito final
                   (prompts/juiz_aceitas.md), e a dificuldade do banco passa a usar esses vereditos.
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.geracao_tipos.rodadas import _filtrado, _nome_arq

from . import comum as C
from .ablacao_v3 import TETO_RESPOSTA
from .v22 import TIPOS, validar_auditoria, veredito

MODELO_ALTERNATIVAS = "gpt-5-petrobras:high"
MODELO_DECISAO = "gpt-5-4-petrobras:high"
MODELO_JUIZ = "gpt-5-4-petrobras:medium"
N_FONTES = 6
MAX_ITENS = 3
DECISOES = ("manter", "aceitar", "reescrever", "descartar")
CLASSES = ("equivalente", "valida_diferente", "incorreta")
CONDICOES = ("closed_book", "open_book")
INDICES = C.ROOT / "dataset" / "indices_refino"


# ------------------------------------------------------------------ validação das respostas dos modelos
def validar_alternativas(d: dict) -> None:
    if not isinstance(d, dict) or set(d) != {"respostas", "consultas"}:
        raise ValueError("use exatamente as chaves respostas e consultas")
    r, c = d["respostas"], d["consultas"]
    if not isinstance(r, list) or not 1 <= len(r) <= 3 or any(
            not isinstance(x, dict) or not str(x.get("resposta", "")).strip() for x in r):
        raise ValueError("respostas: de 1 a 3 objetos com resposta e justificativa")
    if not isinstance(c, list) or not 1 <= len(c) <= 2 or any(
            not isinstance(x, dict) or not str(x.get("pt", "")).strip() or not str(x.get("en", "")).strip() for x in c):
        raise ValueError("consultas: de 1 a 2 objetos com pt e en")


def validar_gabarito(g, resposta_padrao: str | None = None) -> None:
    if not isinstance(g, dict) or set(g) != {"modo", "itens"} or g["modo"] not in ("qualquer", "todas"):
        raise ValueError('gabarito_final: {"modo": "qualquer" | "todas", "itens": [...]}')
    its = g["itens"]
    if not isinstance(its, list) or not 1 <= len(its) <= MAX_ITENS:
        raise ValueError(f"gabarito_final: de 1 a {MAX_ITENS} itens")
    if g["modo"] == "todas" and len(its) < 2:
        raise ValueError('modo "todas" exige 2 ou 3 itens')
    for it in its:
        if not isinstance(it, dict) or set(it) != {"resposta", "sinonimos"} or not str(it["resposta"]).strip() \
                or not isinstance(it["sinonimos"], list):
            raise ValueError("cada item tem resposta e sinonimos (lista)")
    if resposta_padrao:
        alvo = _norm(resposta_padrao)
        if any(_norm(x) == alvo for it in its for x in [it["resposta"], *it["sinonimos"]]):
            raise ValueError("a resposta padrão não pode estar entre as respostas aceitas")


def validar_decisao(d: dict, pode_reescrever: bool, resposta_padrao: str | None = None) -> None:
    chaves = {"gabarito", "apoio_externo", "fontes", "alternativas", "decisao", "gabarito_final", "reescrita", "motivo"}
    if not isinstance(d, dict) or set(d) != chaves:
        raise ValueError(f"use exatamente as chaves {sorted(chaves)}")
    if d["gabarito"] not in ("correto", "discutivel", "incorreto"):
        raise ValueError("gabarito: correto, discutivel ou incorreto")
    if d["apoio_externo"] not in ("confirma", "contradiz", "sem_evidencia") or not isinstance(d["fontes"], list):
        raise ValueError("apoio_externo: confirma, contradiz ou sem_evidencia; fontes: lista de ids")
    if not isinstance(d["alternativas"], list) or any(
            not isinstance(a, dict) or a.get("classe") not in CLASSES for a in d["alternativas"]):
        raise ValueError("alternativas: lista de {resposta, classe}")
    if d["decisao"] not in DECISOES or (d["decisao"] == "reescrever" and not pode_reescrever):
        raise ValueError("decisao: " + ", ".join(DECISOES if pode_reescrever else
                                                  [x for x in DECISOES if x != "reescrever"]))
    if d["decisao"] in ("manter", "aceitar"):
        if d["gabarito"] == "incorreto":
            raise ValueError("gabarito incorreto não pode ser mantido nem aceito")
        validar_gabarito(d["gabarito_final"], resposta_padrao)
        if d["decisao"] == "manter" and d["gabarito_final"]["modo"] == "qualquer" and len(d["gabarito_final"]["itens"]) > 1:
            raise ValueError("manter tem um item; mais de um item é aceitar")
    elif d["gabarito_final"] is not None:
        raise ValueError("gabarito_final é null quando a decisão é reescrever ou descartar")
    if d["decisao"] == "reescrever":
        r = d["reescrita"]
        if not isinstance(r, dict) or set(r) != {"pergunta", "resposta", "explicacao", "resposta_padrao", "por_que_nao"} \
                or not all(isinstance(v, str) and v.strip() for v in r.values()):
            raise ValueError("reescrita: pergunta, resposta, explicacao, resposta_padrao e por_que_nao")
    elif d["reescrita"] is not None:
        raise ValueError("reescrita é null quando a decisão não é reescrever")
    if not isinstance(d["motivo"], str) or not d["motivo"].strip():
        raise ValueError("motivo deve ser um texto")


def validar_juiz(d: dict, ids: list[str]) -> None:
    a = d.get("avaliacoes") if isinstance(d, dict) else None
    if not isinstance(a, list) or [x.get("id") for x in a if isinstance(x, dict)] != ids or any(
            x.get("veredito") not in ("correta", "parcial", "incorreta") for x in a):
        raise ValueError(f"avaliacoes: uma por id, na ordem {ids}, com veredito correta, parcial ou incorreta")


def _norm(t: str) -> str:
    return " ".join(str(t).lower().replace(".", " ").split())


def gabarito_simples(resposta: str) -> dict:
    return {"modo": "qualquer", "itens": [{"resposta": resposta, "sinonimos": []}]}


def texto_gabarito(g: dict) -> str:
    its = [it["resposta"] + (f" (ou {', '.join(it['sinonimos'])})" if it["sinonimos"] else "") for it in g["itens"]]
    if len(its) == 1:
        return its[0]
    return ("Qualquer um de: " if g["modo"] == "qualquer" else "Todos estes: ") + "; ".join(its)


# ------------------------------------------------------------------ verificador
class Verificador:
    def __init__(self, banco, clientes: dict | None = None, acervo=None):
        self.b = banco
        self.pasta = banco.saida / "verificacao"
        self.pasta_reescritas = banco.saida / "reescritas"
        self.pasta_juiz = banco.saida / "rejulgamento"
        self._clientes = dict(clientes or {})
        self._acervo = acervo
        self._trava = threading.Lock()

    def cliente(self, papel: str):
        with self._trava:
            if papel not in self._clientes:
                modelo = {"alternativas": MODELO_ALTERNATIVAS, "decisao": MODELO_DECISAO, "juiz": MODELO_JUIZ}[papel]
                self._clientes[papel] = C.cliente_llm(modelo, self.b.saida, f"verif_{papel}")
            return self._clientes[papel]

    def acervo(self):
        with self._trava:
            if self._acervo is None:
                from pipeline.qa_research.refino.retrieval import Acervo, discover
                manifestos, _ = discover(C.ROOT, ["auto"])
                if not manifestos:
                    raise ValueError("Nenhum corpus técnico pronto para a checagem externa (dataset/domain_corpora)")
                self.b.progress(f"[verificação] carregando os índices dos corpora ({len(manifestos)} manifestos)",
                                flush=True)
                self._acervo = Acervo.from_manifests(manifestos, INDICES)
            return self._acervo

    # arquivos
    def _arq(self, pasta: Path, uid: str) -> Path:
        return pasta / f"{_nome_arq(uid)}.json"

    def registro(self, uid: str) -> dict | None:
        a = self._arq(self.pasta, uid)
        return read_json(a) if a.exists() else None

    def decisao(self, uid: str) -> dict | None:
        r = self.registro(uid)
        return r["decisao"] if r and r.get("status") == "verificada" else None

    def reescrita(self, uid: str) -> dict | None:
        a = self._arq(self.pasta_reescritas, uid)
        return read_json(a) if a.exists() else None

    def rejulgamento(self, uid: str, gab: dict) -> dict | None:
        a = self._arq(self.pasta_juiz, uid)
        r = read_json(a) if a.exists() else None
        return r if r and r.get("gabarito_sha256") == C.sha(gab) else None

    # 1 a 3: verificação de uma questão
    def fontes(self, consultas: list[dict], q: dict) -> list[dict]:
        pares = [{"pt": c["pt"], "en": c["en"]} for c in consultas]
        pares.append({"pt": f"{q['resposta']} {q['pergunta']}"[:300], "en": q["resposta"]})
        escolhidas, _ = self.acervo().query(pares, 8, keep=N_FONTES)
        return [{"id": p["id"], "colecao": p.get("collection"), "titulo": p.get("title"), "url": p.get("url"),
                 "texto": " ".join(str(p["texto"]).split())[:1500]} for p in escolhidas]

    def verificar_um(self, q: dict, respostas_modelos: list[str], revisao: dict | None, pode_reescrever: bool) -> bool:
        arq = self._arq(self.pasta, q["uid"])
        if arq.exists():
            return True
        try:
            alt = self.cliente("alternativas").json(
                C.prompt("verif_alternativas"), json.dumps({"pergunta": q["pergunta"]}, ensure_ascii=False),
                tag="verif_alternativas", max_tokens=8000, item=q["item"], validate=validar_alternativas)
            fontes = self.fontes(alt["consultas"], q)
            entrada = {"pergunta": q["pergunta"], "gabarito": q["resposta"], "explicacao": q.get("explicacao"),
                       "resposta_padrao": q.get("resposta_padrao"), "por_que_nao": q.get("por_que_nao"),
                       "documento": q["contexto_tecnico"],
                       "respostas_propostas": [r["resposta"] for r in alt["respostas"]],
                       "respostas_dos_modelos": sorted({r for r in respostas_modelos if r}),
                       "fontes_externas": fontes, "pode_reescrever": pode_reescrever}
            if revisao:
                entrada["revisao_anterior"] = revisao.get("justificativa")
            d = self.cliente("decisao").json(
                C.prompt("verif_decisao"), json.dumps({k: v for k, v in entrada.items() if v is not None},
                                                      ensure_ascii=False),
                tag="verif_decisao", max_tokens=12000, item=q["item"],
                validate=lambda d: validar_decisao(d, pode_reescrever, q.get("resposta_padrao")))
            rec = {"uid": q["uid"], "status": "verificada", "alternativas_propostas": alt["respostas"],
                   "consultas": alt["consultas"], "fontes": fontes, "decisao": d}
        except Exception as exc:  # noqa: BLE001
            if not _filtrado(exc):
                self.b.progress(f"[verificação] {q['uid']}: {type(exc).__name__}: {str(exc)[:200]}", flush=True)
                return False
            rec = {"uid": q["uid"], "status": "bloqueio_provedor"}
        if rec.get("status") == "verificada" and rec["decisao"]["decisao"] == "reescrever":
            if not self.reescrever(q, rec["decisao"]):
                return False
        atomic_json(arq, rec)
        return True

    def reescrever(self, q: dict, d: dict) -> bool:
        """A reescrita passa pelo auditor v23 e pela sustentação, como qualquer questão gerada."""
        arq = self._arq(self.pasta_reescritas, q["uid"])
        if arq.exists():
            return True
        r = d["reescrita"]
        nova = {**q, **r, "uid": f"verif:{q['uid']}", "reescrita_de": q["uid"]}
        lt = self.b.leitor
        bs = lt.todos[q["item"]]
        ctx = [{"id": b["id"], "titulo": f"{bs[b['indice_documento']]['titulo_capitulo']} / "
                                         f"{bs[b['indice_documento']]['subtitulo']}", "texto": b["texto"]}
               for b in q["blocos_contexto"]]
        tipo = q.get("tipo") if q.get("tipo") in TIPOS else "nao_declarado"
        try:
            a = lt.cliente("auditoria").json(
                C.prompt("auditoria_v23"),
                json.dumps({"tipo_declarado": tipo, "pergunta": nova["pergunta"], "resposta_referencia": nova["resposta"],
                            "explicacao_do_autor": nova.get("explicacao") or "(não informada)",
                            "blocos": lt._blocos_txt(ctx)}, ensure_ascii=False),
                tag="verif_auditoria", max_tokens=6000, item=q["item"], validate=validar_auditoria)
            aud = veredito(a, tipo)
            curta = len(nova["resposta"].split()) <= TETO_RESPOSTA
            sust, evid = None, None
            if aud["aprovada"] and curta:
                from pipeline.qa_research.benchmark_gap import resumo_faithfulness
                from .ablacao_v3 import evidencias
                ds = lt.chamar_sustentacao(nova)
                sust, evid = resumo_faithfulness(ds)["status"], evidencias(ds)
        except Exception as exc:  # noqa: BLE001
            if not _filtrado(exc):
                self.b.progress(f"[verificação] reescrita de {q['uid']}: {type(exc).__name__}", flush=True)
                return False
            aud, curta, sust, evid = ({"aprovada": False, "motivo": "bloqueio", "justificativa": "filtro de conteúdo"},
                                      True, None, None)
        ok = aud["aprovada"] and curta and sust == "totalmente_sustentado"
        motivo = ("aprovada" if ok else f"auditor: {aud.get('motivo')} ({aud.get('justificativa', '')[:200]})"
                  if not aud["aprovada"] else "gabarito com mais de 20 palavras" if not curta
                  else f"sustentação: {sust}")
        atomic_json(arq, {"uid_origem": q["uid"], "status": "aprovada" if ok else "reprovada", "motivo": motivo,
                          "auditoria": {k: aud.get(k) for k in ("aprovada", "motivo", "falhas", "justificativa")},
                          "sustentacao": sust, "evidencias": evid, "questao": nova})
        return True

    # 4: rejulgamento das respostas dos modelos contra o gabarito final
    def rejulgar_um(self, q: dict, gab: dict, pares: dict) -> bool:
        if self.rejulgamento(q["uid"], gab):
            return True
        cand, mapa = [], {}
        for m, r in sorted(pares.items()):
            for cond in CONDICOES:
                texto = r.get(f"resposta_{cond}")
                if texto:
                    i = f"R{len(cand) + 1}"
                    cand.append({"id": i, "resposta": texto})
                    mapa[i] = (m, cond)
        vere: dict = {c: {} for c in CONDICOES}
        if cand:
            ids = [c["id"] for c in cand]
            try:
                d = self.cliente("juiz").json(
                    C.prompt("juiz_aceitas"), json.dumps({"pergunta": q["pergunta"], "gabarito": gab, "candidatas": cand},
                                                         ensure_ascii=False),
                    tag="juiz_aceitas", max_tokens=8000, item=q["item"], validate=lambda d: validar_juiz(d, ids))
            except Exception as exc:  # noqa: BLE001
                if not _filtrado(exc):
                    self.b.progress(f"[rejulgamento] {q['uid']}: {type(exc).__name__}", flush=True)
                    return False
                return True     # bloqueado: fica com os vereditos da avaliação
            for x in d["avaliacoes"]:
                m, cond = mapa[x["id"]]
                vere[cond][m] = x["veredito"]
        atomic_json(self._arq(self.pasta_juiz, q["uid"]),
                    {"uid": q["uid"], "gabarito_sha256": C.sha(gab), "gabarito": gab, "vereditos": vere})
        return True
