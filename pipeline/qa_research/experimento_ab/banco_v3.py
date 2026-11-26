"""Banco final v3 do PetroQuest (relatorios/petroquest_banco_v3): todas as válidas da geração final v3 e dos loops,
uma por conhecimento, avaliadas pelos modelos e revisadas uma a uma.

Momento: depois de todas as gerações (principal com paciência maior e loops), porque a avaliação e a revisão são pagas
por questão e só fazem sentido sobre o banco já deduplicado. Tudo é retomável e incremental: rodar de novo depois de
um loop novo só paga as questões novas.

Etapas (`ETAPAS`), repetidas em até RODADAS rodadas:
  montar     grupos de equivalentes da deduplicação única (principal + loops). Cada grupo é representado pela primeira
             questão que não caiu nas regras locais nem na revisão; se o representante cai, o próximo equivalente do
             grupo (até MAX_TENTATIVAS) entra na rodada seguinte, em vez de o conhecimento sair do banco.
             Regras locais (sem API):
               R2 resposta_no_enunciado   80% ou mais das palavras de conteúdo do gabarito já estão na pergunta;
               R3 forma_por_que_nao_basta "Por que X não basta/garante...";
               R9 enunciado_dependente    o enunciado remete ao texto ("segundo o procedimento descrito", "no
                                          cenário acima", "conforme o documento").
  avaliar    GPT-4.1 Mini, GPT-4.1, GPT-5 mini e GPT-5 (independentes) e GPT-5.4 (referência), sem e com o contexto,
             resposta de até 20 palavras, juiz GPT-5.4 (o mesmo protocolo do dataset final v2).
  unicidade  revisão de TODAS as questões representantes (não só das que o GPT-5 erra, como no banco v1), juiz GPT-5.4
             com prompts/unicidade_v3.md: vê o documento, o gabarito, a resposta padrão e as respostas sem contexto de
             GPT-5, GPT-5 mini e GPT-4.1 (e, quando GPT-5 e GPT-5.4 erram mesmo com o documento, as respostas deles com
             o documento). Saem:
               R5 gabarito_nao_unico      outra resposta também é correta;
               R6 gabarito_vago           o gabarito não nomeia um elemento técnico concreto;
               R7 depende_documento       a resposta exige algo próprio do documento;
               R9 enunciado_dependente    o enunciado não se entende ou não se responde sem o documento;
               R10 trivial                a resposta está no enunciado ou sai de bom senso.
             Resposta "equivalente" que o juiz da avaliação não aceitou vira acerto (veredito corrigido).
  banco      banco.jsonl (ids PQ3B-00001...), poda.jsonl, resumo.json e BANCO.md (validade, tipos, áreas,
             documentos, origem, acurácia com e sem contexto e estratos de dificuldade).

python -m pipeline.qa_research.experimento_ab banco-v3 [--etapas montar,avaliar,unicidade,banco] [--rodadas 3]
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.geracao_tipos.rodadas import _filtrado, _nome_arq

from . import comum as C
from .banco import sobreposicao
from .final import NAO_BASTA
from .final_v3 import CONFIG, DOCS_FINAIS, SAIDA as ORIGEM, GeracaoFinalV3, ler_unidades
from .painel import ESTRATOS, estrato

SAIDA = C.QA / "relatorios" / "petroquest_banco_v3"
ETAPAS = ("montar", "avaliar", "unicidade", "banco")
RODADAS = 3
MAX_TENTATIVAS = 3          # questões de um mesmo grupo de equivalentes que podem ser tentadas como representante
INDEPENDENTES = ("gpt-4-1-mini", "gpt-4-1", "gpt-5-mini", "gpt-5")
REVISADOS = ("gpt-5", "gpt-5-mini", "gpt-4-1")
FORTES_COM_CONTEXTO = ("gpt-5", "gpt-5-4")
JUIZ_UNICIDADE = "gpt-5-4-petrobras:high"
DEPENDENTE = re.compile(
    r"\b(segundo|conforme|de acordo com) (o|a) (texto|documento|procedimento descrito|trecho|material|bloco)|"
    r"\b(no|do|neste|deste) (texto|documento|trecho)\b|descrit[oa]s? (acima|anteriormente)|"
    r"\b(cen[aá]rio|situa[cç][aã]o|caso) (descrit|apresentad)[oa]|mencionad[oa]s? (acima|no texto)|"
    r"\b(é|são|foi|foram) (citad|mencionad|listad)[oa]s?\b", re.I)
REGRAS = {"R2": "resposta_no_enunciado", "R3": "forma_por_que_nao_basta", "R5": "gabarito_nao_unico",
          "R6": "gabarito_vago", "R7": "depende_documento", "R9": "enunciado_dependente", "R10": "trivial"}
DESCRICAO = {"R2": "o gabarito já está no enunciado", "R3": "forma \"por que X não basta/garante\"",
             "R5": "revisão: outra resposta também é correta", "R6": "revisão: gabarito vago",
             "R7": "revisão: depende do documento", "R9": "o enunciado precisa do documento",
             "R10": "revisão: trivial (resposta no enunciado ou por bom senso)"}
CHAVES_REVISAO = {"respostas", "gabarito_especifico", "gabarito_unico", "depende_documento", "enunciado_autocontido",
                  "trivial", "justificativa"}
# Fica só no servidor: caches, uma resposta e um julgamento por arquivo, uma revisão por arquivo (as revisões vão ao
# GitHub consolidadas em revisoes.jsonl).
GITIGNORE = """.local/
chamadas/
falhas/
avaliacao/respostas/
avaliacao/juiz/
avaliacao/falhas/
avaliacao/.local/
unicidade/
"""
CAMPOS = ("uid", "item", "tipo", "cenario", "pergunta", "resposta", "explicacao", "conhecimento", "resposta_padrao",
          "por_que_nao", "foco", "par", "visita", "config", "origem_uid", "origem_defeito")


def validar_revisao(d: dict, ids: list[str]) -> None:
    if not isinstance(d, dict) or set(d) != CHAVES_REVISAO:
        raise ValueError(f"use exatamente as chaves {sorted(CHAVES_REVISAO)}")
    if not isinstance(d["respostas"], list) or sorted(r.get("id") for r in d["respostas"] if isinstance(r, dict)) != \
            sorted(ids) or any(r.get("avaliacao") not in ("equivalente", "alternativa_valida", "incorreta")
                               for r in d["respostas"]):
        raise ValueError(f"respostas deve avaliar {ids} como equivalente, alternativa_valida ou incorreta")
    for k in CHAVES_REVISAO - {"respostas", "justificativa"}:
        if not isinstance(d[k], bool):
            raise ValueError(f"{k} deve ser true ou false")
    if not isinstance(d["justificativa"], str) or not d["justificativa"].strip():
        raise ValueError("justificativa deve ser um texto")


def regra_revisao(r: dict) -> tuple[str, str] | None:
    """Regra que a revisão aplica (ou None, se a questão fica)."""
    if any(x["avaliacao"] == "alternativa_valida" for x in r["respostas"]) or not r["gabarito_unico"]:
        return "R5", r["justificativa"]
    if not r["gabarito_especifico"]:
        return "R6", r["justificativa"]
    if r["depende_documento"]:
        return "R7", r["justificativa"]
    if not r["enunciado_autocontido"]:
        return "R9", r["justificativa"]
    if r["trivial"]:
        return "R10", r["justificativa"]
    return None


def regra_local(q: dict) -> tuple[str, str] | None:
    if sobreposicao(q) >= 0.8:
        return "R2", f"sobreposição {sobreposicao(q):.2f}"
    if re.match(r"\s*por que\b", q["pergunta"], re.I) and NAO_BASTA.search(q["pergunta"]):
        return "R3", "forma 'por que X não basta/garante'"
    if DEPENDENTE.search(q["pergunta"]):
        return "R9", f"remete ao texto: \"{DEPENDENTE.search(q['pergunta']).group(0)}\""
    return None


class Leitor(GeracaoFinalV3):
    """Lê a pasta da geração final v3 (principal e loops) sem gerar nada nem tocar no registro da geração."""

    def __init__(self, origem: Path = ORIGEM, **kw):
        super().__init__(origem, **kw)

    def _config(self) -> None:
        pass

    def _unidades(self) -> list[dict]:
        self.fechados = {}
        return [u for u in ler_unidades(self.saida / CONFIG) if u["item"] in self.todos]


class BancoV3:
    def __init__(self, origem: Path = ORIGEM, saida: Path = SAIDA, *, docs: Path = DOCS_FINAIS, exp: Path = C.EXPERIMENTO,
                 workers: int = 8, judge_workers: int = 2, clientes: dict | None = None, cliente_unicidade=None,
                 leitor=None, progress=print):
        self.origem, self.saida, self.docs, self.exp = Path(origem), Path(saida), Path(docs), Path(exp)
        self.workers, self.judge_workers, self.progress = max(1, int(workers)), int(judge_workers), progress
        self._clientes, self._cliente_u, self._leitor = clientes, cliente_unicidade, leitor
        self.saida.mkdir(parents=True, exist_ok=True)
        (self.saida / ".gitignore").write_text(GITIGNORE, encoding="utf-8")

    @property
    def leitor(self) -> Leitor:
        if self._leitor is None:
            self._leitor = Leitor(self.origem, docs=self.docs, exp=self.exp, progress=self.progress)
        return self._leitor

    # ---------------------------------------------------------------- 1. grupos e representantes
    def grupos(self) -> tuple[list[list[dict]], int]:
        """Grupos de equivalentes (o mantido pela deduplicação primeiro, depois os demais na ordem de geração) e o
        número de válidas ainda sem decisão de deduplicação (ficam de fora até a geração ser retomada)."""
        lt = self.leitor
        validas = lt.validas_banco()
        red = lt.redundantes()
        decididas = {q["uid"] for q in validas if lt._arq_dedup(q["item"], q["uid"]).exists()}
        por_uid = {q["uid"]: q for q in validas if q["uid"] in decididas}
        membros = defaultdict(list)
        for q in validas:
            if q["uid"] in por_uid:
                membros[red.get(q["uid"], q["uid"])].append(q)
        out = []
        for chefe, ms in membros.items():
            if chefe not in por_uid:          # o mantido não é válido (não deveria ocorrer): o grupo usa os membros
                out.append(ms)
                continue
            out.append([por_uid[chefe]] + [m for m in ms if m["uid"] != chefe])
        out.sort(key=lambda g: (g[0]["item"], g[0]["ordem_config"], g[0]["onda"], g[0]["foco"], g[0]["k"]))
        return out, len(validas) - len(decididas)

    def _arq_u(self, uid: str) -> Path:
        return self.saida / "unicidade" / f"{_nome_arq(uid)}.json"

    def rejeicao(self, q: dict) -> tuple[str, str] | None:
        """Regra que tira esta questão (local ou de uma revisão já feita), ou None."""
        r = regra_local(q)
        if r:
            return r
        rev = read_json(self._arq_u(q["uid"])) if self._arq_u(q["uid"]).exists() else None
        return regra_revisao(rev) if rev and rev.get("status") == "revisada" else None

    def montar(self) -> dict:
        grupos, pendentes = self.grupos()
        reps, poda, esgotados = [], [], 0
        for g in grupos:
            escolhido = None
            for tent, q in enumerate(g[:MAX_TENTATIVAS]):
                rj = self.rejeicao(q)
                if rj is None:
                    escolhido = q
                    break
                poda.append({"uid": q["uid"], "regra": rj[0], "nome": REGRAS[rj[0]], "detalhe": rj[1],
                             "tentativa": tent + 1, "grupo": g[0]["uid"], **{k: q.get(k) for k in CAMPOS}})
            if escolhido is None:
                esgotados += 1
                continue
            reps.append({**{k: escolhido.get(k) for k in CAMPOS},
                         "composicao": "composta" if escolhido["config"] == "loop_composta" else "simples",
                         "fonte": escolhido["config"],
                         "grupo": g[0]["uid"],
                         "tamanho_grupo": len(g), "tentativa": g.index(escolhido) + 1,
                         "contexto_tecnico": self._contexto(escolhido),
                         "blocos_contexto": [{"id": b["id"], "texto": b["texto"], "indice_documento": b["indice_documento"]}
                                             for b in escolhido["blocos_contexto"]]})
        C.gravar_jsonl(self.saida / "dataset.jsonl", reps)
        C.gravar_jsonl(self.saida / "poda.jsonl", poda)
        res = {"grupos": len(grupos), "representantes": len(reps), "grupos_esgotados": esgotados,
               "validas_sem_dedup": pendentes, "podadas": dict(Counter(p["regra"] for p in poda))}
        atomic_json(self.saida / "montagem.json", res)
        self.progress(f"[banco v3] {len(grupos)} conhecimentos (grupos), {len(reps)} representantes, "
                      f"{esgotados} grupos sem representante válido, {pendentes} válidas sem deduplicação", flush=True)
        return res

    def _contexto(self, q: dict) -> str:
        bs = self.leitor.todos[q["item"]]
        return "\n\n".join(f"{bs[b['indice_documento']]['titulo_capitulo']} / {bs[b['indice_documento']]['subtitulo']}\n"
                           f"{b['texto']}" for b in q["blocos_contexto"])

    # ---------------------------------------------------------------- 2. avaliação (modelos com e sem contexto)
    def avaliar(self) -> int:
        from .completo import DatasetCompleto
        av = DatasetCompleto(saida=self.saida, exp=self.exp, fontes_=[], v1=self.saida, progress=self.progress)
        return av.avaliar(workers=self.workers, judge_workers=self.judge_workers, clientes=self._clientes)

    def vereditos(self) -> dict:
        """uid -> modelo -> linha de pares.csv."""
        vs: dict = {}
        arq = self.saida / "pares.csv"
        if arq.exists():
            with arq.open(encoding="utf-8-sig") as f:
                for r in csv.DictReader(C.sem_nul(f)):
                    vs.setdefault(r["uid"], {})[r["modelo"]] = r
        return vs

    # ---------------------------------------------------------------- 3. revisão de unicidade (todas)
    def cliente_u(self):
        if self._cliente_u is None:
            self._cliente_u = C.cliente_llm(JUIZ_UNICIDADE, self.saida, "unicidade")
        return self._cliente_u

    @staticmethod
    def suspeita(v: dict) -> bool:
        return all(v.get(m, {}).get("veredito_open_book") not in (None, "", "correta") for m in FORTES_COM_CONTEXTO)

    def entrada(self, q: dict, v: dict) -> tuple[str, dict]:
        mostrar = [(m, "closed_book") for m in REVISADOS]
        if self.suspeita(v):
            mostrar += [(m, "open_book") for m in FORTES_COM_CONTEXTO]
        resp, ids = [], {}
        for m, cond in mostrar:
            texto = v.get(m, {}).get(f"resposta_{cond}")
            if texto:
                i = f"R{len(resp) + 1}"
                resp.append({"id": i, "com_documento": cond == "open_book", "resposta": texto})
                ids[i] = [m, cond]
        payload = {"pergunta": q["pergunta"], "gabarito": q["resposta"], "explicacao": q.get("explicacao"),
                   "resposta_padrao": q.get("resposta_padrao"), "por_que_nao": q.get("por_que_nao"),
                   "documento": q["contexto_tecnico"], "respostas": resp}
        return json.dumps({k: x for k, x in payload.items() if x is not None}, ensure_ascii=False), ids

    def unicidade(self) -> int:
        qs = C.linhas(self.saida / "dataset.jsonl")
        vs = self.vereditos()
        cfg = {"schema": "petroquest-unicidade-v3", "juiz": JUIZ_UNICIDADE, "prompt_sha256": C.sha(C.prompt("unicidade_v3")),
               "revisados": list(REVISADOS), "fortes_com_contexto": list(FORTES_COM_CONTEXTO)}
        pasta = self.saida / "unicidade"
        with output_lock(pasta):
            old = read_json(pasta / "config.json")
            if old is not None and old != cfg:
                raise ValueError(f"Revisão com outro juiz ou prompt em {C.relativo(pasta)}; apague a pasta unicidade/")
            atomic_json(pasta / "config.json", cfg)
            (pasta / "falhas").mkdir(parents=True, exist_ok=True)
            # questões que já passaram pela avaliação (a revisão usa as respostas sem contexto). Basta estarem nos pares:
            # uma resposta sem nota do juiz (ou bloqueada pelo provedor) não volta numa nova execução, e exigir a nota de
            # todos os modelos travava a etapa para sempre; a revisão mostra só as respostas que existem.
            prontas = [q for q in qs if any(vs.get(q["uid"], {}).get(m) for m in REVISADOS)]
            faltam = [q for q in prontas if not self._arq_u(q["uid"]).exists()]
            self.progress(f"[banco v3] unicidade: {len(prontas) - len(faltam)}/{len(qs)} revisadas; {len(faltam)} a revisar"
                          + (f"; {len(qs) - len(prontas)} ainda sem avaliação" if len(prontas) < len(qs) else ""),
                          flush=True)
            sistema = C.prompt("unicidade_v3")

            def um(q: dict) -> bool:
                user, ids = self.entrada(q, vs.get(q["uid"], {}))
                try:
                    d = self.cliente_u().json(sistema, user, tag="unicidade_v3", max_tokens=6000, item=q["item"],
                                              validate=lambda d: validar_revisao(d, list(ids)))
                    rec = {"uid": q["uid"], "status": "revisada", "ids": ids, **d}
                except Exception as exc:  # noqa: BLE001
                    if not _filtrado(exc):
                        atomic_json(pasta / "falhas" / self._arq_u(q["uid"]).name,
                                    {"uid": q["uid"], "erro": f"{type(exc).__name__}: {exc}"[:1500]})
                        return False
                    rec = {"uid": q["uid"], "status": "bloqueio_provedor"}
                atomic_json(self._arq_u(q["uid"]), rec)
                (pasta / "falhas" / self._arq_u(q["uid"]).name).unlink(missing_ok=True)
                return True

            ok = 0
            with ThreadPoolExecutor(max_workers=self.workers) as pool:
                for k, r in enumerate(pool.map(um, faltam), 1):
                    ok += r
                    if k % 200 == 0:
                        self.progress(f"[banco v3] unicidade {k}/{len(faltam)}", flush=True)
            return (len(faltam) - ok) + (len(qs) - len(prontas))

    # ---------------------------------------------------------------- 4. evidência (gabarito de recuperação)
    def evidencia(self, q: dict) -> dict | None:
        """Blocos e trechos literais que sustentam o gabarito, da verificação de sustentação. Registros antigos não
        guardavam as evidências: a mesma chamada é refeita e lida do cache do cliente (sem custo), e o registro é
        completado."""
        from .ablacao_v3 import evidencias
        lt = self.leitor
        arq = lt._arq_sust(q["uid"])
        rec = read_json(arq) if arq.exists() else None
        if rec is None or rec.get("status") != "totalmente_sustentado":
            return None
        if "evidencias" not in rec:
            try:
                rec["evidencias"] = evidencias(lt.chamar_sustentacao(q))
            except Exception as exc:  # noqa: BLE001
                if not _filtrado(exc):
                    raise
                return None
            atomic_json(arq, rec)
        idx = {b["id"]: b["indice_documento"] for b in q["blocos_contexto"]}
        trechos = [{"indice_documento": idx[t["bloco"]], "trecho": t["trecho"]}
                   for e in rec["evidencias"] for t in e["trechos"] if t["bloco"] in idx]
        return {"blocos": sorted({t["indice_documento"] for t in trechos}), "trechos": trechos}

    def evidencias(self, qs: list[dict]) -> dict:
        def um(q):
            try:
                return q["uid"], self.evidencia(q)
            except Exception as exc:  # noqa: BLE001
                self.progress(f"[banco v3] evidência de {q['uid']}: {type(exc).__name__}", flush=True)
                return q["uid"], None
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            return dict(pool.map(um, qs))

    # ---------------------------------------------------------------- 5. banco
    def banco(self) -> dict:
        from pipeline.qa_research.piloto_janela.core import tema
        qs = C.linhas(self.saida / "dataset.jsonl")
        vs = self.vereditos()
        poda = C.linhas(self.saida / "poda.jsonl")
        temas = {i: tema(i) for i in sorted({q["item"] for q in qs} | {p["item"] for p in poda})}
        banco, sem_revisao, novas_podas, corrigidas = [], 0, [], 0
        ev = self.evidencias([q for q in qs if self._arq_u(q["uid"]).exists()])
        for q in qs:
            u, v = q["uid"], vs.get(q["uid"], {})
            rev = read_json(self._arq_u(u)) if self._arq_u(u).exists() else None
            if not rev or rev.get("status") != "revisada":
                sem_revisao += 1
                continue
            rj = regra_revisao(rev)
            if rj:      # reprovada nesta rodada: o próximo equivalente entra na próxima montagem
                novas_podas.append(u)
                continue
            corr = {}
            for x in rev["respostas"]:
                m, cond = rev["ids"][x["id"]]
                if x["avaliacao"] == "equivalente" and v.get(m, {}).get(f"veredito_{cond}") != "correta":
                    corr.setdefault(cond, {})[m] = "correta"
            corrigidas += bool(corr)
            fech = {m: r["veredito_closed_book"] for m, r in v.items()} | corr.get("closed_book", {})
            aberto = {m: r["veredito_open_book"] for m, r in v.items()} | corr.get("open_book", {})
            banco.append({"uid": u, "item": q["item"], "area": temas[q["item"]]["area"], "tema": temas[q["item"]]["tema"],
                          "tipo": q["tipo"], "cenario": q.get("cenario"), "pergunta": q["pergunta"],
                          "resposta": q["resposta"], "explicacao": q.get("explicacao"),
                          "resposta_padrao": q.get("resposta_padrao"), "por_que_nao": q.get("por_que_nao"),
                          "fonte": q["fonte"], "composicao": q.get("composicao", "simples"),
                          "origem_uid": q.get("origem_uid"), "grupo": q["grupo"], "tamanho_grupo": q["tamanho_grupo"],
                          "blocos_contexto": [{"item": q["item"], "indice_documento": b["indice_documento"]}
                                              for b in q["blocos_contexto"]],
                          "evidencia": ev.get(u),
                          "dificuldade": {"estrato": estrato({m: fech.get(m) for m in INDEPENDENTES})
                                          if all(fech.get(m) for m in INDEPENDENTES) else None,
                                          "sem_contexto": fech, "com_contexto": aberto,
                                          "veredito_corrigido": {c: sorted(ms) for c, ms in corr.items()}}})
        banco.sort(key=lambda b: (b["item"], b["tipo"] or "", b["uid"]))
        for k, b in enumerate(banco, 1):
            b["id"] = f"PQ3B-{k:05d}"
        C.gravar_jsonl(self.saida / "banco.jsonl", [{"id": b["id"], **{k: v for k, v in b.items() if k != "id"}}
                                                     for b in banco])
        C.gravar_jsonl(self.saida / "revisoes.jsonl", [read_json(p) for p in sorted((self.saida / "unicidade").glob("*.json"))
                                                       if p.name != "config.json"])
        res = self.resumo(banco, poda, sem_revisao, len(novas_podas), corrigidas, temas)
        atomic_json(self.saida / "resumo.json", res)
        (self.saida / "BANCO.md").write_text(markdown(res), encoding="utf-8")
        self.progress(f"[banco v3] {res['n']} questões ({'provisório' if res['provisorio'] else 'final'}): "
                      f"{C.relativo(self.saida / 'BANCO.md')}", flush=True)
        return res

    def resumo(self, banco, poda, sem_revisao, reprovadas_rodada, corrigidas, temas) -> dict:
        n = len(banco)
        pct = lambda c, t: round(100 * c / t, 1) if t else None  # noqa: E731
        mont = read_json(self.saida / "montagem.json") or {}
        modelos = [m for m in (*INDEPENDENTES, "gpt-5-4") if banco and all(m in b["dificuldade"]["sem_contexto"] for b in banco)]
        acc = {m: {c: pct(sum(b["dificuldade"][c].get(m) == "correta" for b in banco), n)
                   for c in ("sem_contexto", "com_contexto")} for m in modelos}
        est = Counter(b["dificuldade"]["estrato"] for b in banco)
        regras = Counter(p["regra"] for p in poda)
        return {"n": n, "provisorio": bool(sem_revisao or reprovadas_rodada or mont.get("validas_sem_dedup")),
                "grupos": mont.get("grupos"), "grupos_esgotados": mont.get("grupos_esgotados"),
                "validas_sem_dedup": mont.get("validas_sem_dedup"), "sem_revisao": sem_revisao,
                "reprovadas_a_substituir": reprovadas_rodada, "vereditos_corrigidos": corrigidas,
                "poda": {k: regras.get(k, 0) for k in REGRAS},
                "substituidos": sum(b["tamanho_grupo"] > 1 and b["uid"] != b["grupo"] for b in banco),
                "por_tipo": dict(Counter(b["tipo"] for b in banco).most_common()),
                "por_fonte": dict(Counter(b["fonte"] for b in banco).most_common()),
                "por_composicao": dict(Counter(b["composicao"] for b in banco).most_common()),
                "consertadas": sum(bool(b.get("origem_uid")) for b in banco),
                "com_evidencia": sum(bool(b.get("evidencia") and b["evidencia"]["blocos"]) for b in banco),
                "evidencia_em_2_blocos_ou_mais": sum(len((b.get("evidencia") or {}).get("blocos", [])) >= 2 for b in banco),
                "por_area": dict(Counter(b["area"] for b in banco).most_common()),
                "por_documento": dict(sorted(Counter(b["item"] for b in banco).items())),
                "acuracia": acc, "estratos_pct": {e: pct(est.get(e, 0), n) for e in ESTRATOS},
                "dificil_por_tipo": {t: pct(sum(b["dificuldade"]["estrato"] in ("dificil", "muito_dificil") for b in bs),
                                            len(bs))
                                     for t in sorted({b["tipo"] for b in banco if b["tipo"]})
                                     for bs in [[b for b in banco if b["tipo"] == t]]},
                "palavras_pergunta": float(np.mean([len(b["pergunta"].split()) for b in banco])) if banco else None,
                "palavras_resposta": float(np.mean([len(b["resposta"].split()) for b in banco])) if banco else None,
                "abertura_em_um_pct": pct(sum(bool(re.match(r"(em uma?|num|numa)\b", b["pergunta"], re.I))
                                              for b in banco), n)}

    # ---------------------------------------------------------------- execução
    def executar(self, etapas=ETAPAS, rodadas: int = RODADAS) -> int:
        etapas = tuple(etapas)
        st = 0
        for r in range(1, max(1, rodadas) + 1):
            self.progress(f"[banco v3] rodada {r}", flush=True)
            if "montar" in etapas:
                antes = (self.saida / "dataset.jsonl").read_text(encoding="utf-8") \
                    if (self.saida / "dataset.jsonl").exists() else None
                self.montar()
                mudou = antes != (self.saida / "dataset.jsonl").read_text(encoding="utf-8")
                if r > 1 and not mudou:
                    break             # nenhum representante novo: as rodadas seguintes não mudariam nada
            if "avaliar" in etapas:
                st = self.avaliar()
                if st:
                    return st
            if "unicidade" in etapas:
                st = self.unicidade()
                if st:
                    self.progress(f"[banco v3] {st} revisões pendentes; repita o comando", flush=True)
                    break
            if not ({"avaliar", "unicidade"} & set(etapas)):
                break
        if "banco" in etapas:
            if "montar" in etapas and {"unicidade"} & set(etapas):
                self.montar()         # aplica as revisões da última rodada (sem API): reprovadas vão à poda
            res = self.banco()
            return 2 if res["provisorio"] and st else 0
        return st


NOMES = {"gpt-4-1-mini": "GPT-4.1 Mini", "gpt-4-1": "GPT-4.1", "gpt-5-mini": "GPT-5 mini", "gpt-5": "GPT-5",
         "gpt-5-4": "GPT-5.4 (referência)"}


def markdown(r: dict) -> str:
    f = lambda v, c=1: "-" if v is None else f"{v:.{c}f}"  # noqa: E731
    out = [f"# Banco PetroQuest v3{' (PROVISÓRIO)' if r['provisorio'] else ''}", "",
           f"{r['n']} questões, uma por conhecimento, de {r['grupos']} grupos de válidas equivalentes da geração final v3 "
           f"e dos loops (auditor v23, gabarito de até 20 palavras e totalmente sustentado, deduplicação única). Todas "
           f"foram avaliadas pelos modelos e revisadas uma a uma; quando o representante de um grupo caiu, o próximo "
           f"equivalente foi tentado ({r['substituidos']} questões do banco são substitutas).", "",
           f"Grupos sem nenhum representante válido: {r['grupos_esgotados']}. Pendências: {r['sem_revisao']} sem revisão, "
           f"{r['reprovadas_a_substituir']} reprovadas aguardando o substituto, {r['validas_sem_dedup']} válidas sem "
           f"deduplicação. Vereditos corrigidos pela revisão: {r['vereditos_corrigidos']}.", "",
           "## Poda", "", "| Regra | Motivo | Questões |", "|---|---|---|"]
    out += [f"| {k} | {DESCRICAO[k]} | {v} |" for k, v in r["poda"].items()]
    out += ["", "## Composição", "", f"Por tipo: {r['por_tipo']}.", "", f"Por origem: {r['por_fonte']}.", "",
            f"Simples e compostas: {r['por_composicao']}. Consertadas (vindas de uma reprovada): {r['consertadas']}.", "",
            f"Com evidência rotulada (blocos e trechos que sustentam o gabarito, gabarito de recuperação para avaliar "
            f"RAG e memória): {r['com_evidencia']}; com evidência em 2 blocos ou mais: "
            f"{r['evidencia_em_2_blocos_ou_mais']}.", "",
            f"Por área: {r['por_area']}.", "", f"Por documento: {r['por_documento']}.", "",
            "## Modelos (resposta de até 20 palavras)", "",
            "| Modelo | Sem contexto | Com contexto | Ganho com contexto |", "|---|---|---|---|"]
    for m, a in r["acuracia"].items():
        ganho = a["com_contexto"] - a["sem_contexto"] if None not in a.values() else None
        out.append(f"| {NOMES.get(m, m)} | {f(a['sem_contexto'])}% | {f(a['com_contexto'])}% | {f(ganho)} |")
    e = r["estratos_pct"]
    out += ["", "## Dificuldade e forma", "",
            f"Estratos (4 modelos independentes, sem contexto): fácil {f(e['facil'])}%, média {f(e['media'])}%, "
            f"difícil {f(e['dificil'])}%, muito difícil {f(e['muito_dificil'])}%.", "",
            f"Difícil para o GPT-5 por tipo: {r['dificil_por_tipo']}.", "",
            f"Palavras na pergunta: {f(r['palavras_pergunta'])}; no gabarito: {f(r['palavras_resposta'])}; "
            f"perguntas que abrem com \"Em um/Num\": {f(r['abertura_em_um_pct'])}%."]
    return "\n".join(out) + "\n"
