"""Gerador v21 com três ajustes controlados para o experimento (o resto é o código de geracao_tipos/rodadas.py):

  - documentos e unidade de contexto configuráveis (janela de 3 blocos ou capítulo do bloco foco);
  - nada herdado de rodadas anteriores (inventário e banco dinâmico começam vazios);
  - deduplicação incremental calibrada (dedup.py) no lugar da chamada única por tópico.

Opcional (etapa 4): checagem de sustentação por questão antes da deduplicação, com reparo do gabarito para a
resposta mínima sustentada e descarte individual quando não houver sustentação.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np

from pipeline.qa_research.geracao_tipos.core import CAMPOS, _texto
from pipeline.qa_research.geracao_tipos.rodadas import (PROMPT_AUDITORIA, PROMPT_JANELA, PROMPT_REFINO, GeracaoMeta,
                                                        _filtrado, _nome_arq)
from pipeline.qa_research.geracao_tipos.core import prompt as prompt_v21
from pipeline.qa_research.piloto_janela.core import atomic_json, blocos, carregar_prompt, preencher, read_json, verificar
from pipeline.qa_research.tipos import GRUPOS_V16, MAXIMO_V15, problemas_composicao, problemas_tipo

from . import comum as C
from .dedup import DedupIncremental, carregar_calibracao

# Única diferença entre os prompts das duas unidades: a descrição do contexto e os rótulos dos blocos de apoio.
TROCAS_CAPITULO = (
    ("Leia a janela de três blocos consecutivos de um documento técnico e elabore até quatro questões sobre o bloco foco [F]",
     "Leia um capítulo de um documento técnico, com todos os seus blocos na ordem do documento, e elabore até quatro "
     "questões sobre o bloco foco [F]"),
    ("- `<janela>` contém três blocos consecutivos, na ordem do documento, cada um com capítulo e subtítulo.",
     "- `<capitulo>` contém todos os blocos do capítulo do bloco foco, na ordem do documento, cada um com capítulo e "
     "subtítulo."),
    ("  - [A1] e [A2] são apoio para entender [F].",
     "  - [A1], [A2], ... (os demais blocos do capítulo) são apoio para entender [F]."),
    ('`{"bloco": "F" | "A1" | "A2", "trecho": "..."}`',
     '`{"bloco": "F" ou o rótulo de um bloco de apoio (\"A1\", \"A2\", ...), "trecho": "..."}`'),
    ("<janela>\n{{JANELA}}\n</janela>", "<capitulo>\n{{JANELA}}\n</capitulo>"),
)


def prompt_capitulo(base: Path = PROMPT_JANELA) -> str:
    texto = base.read_text(encoding="utf-8")
    for antes, depois in TROCAS_CAPITULO:
        if texto.count(antes) != 1:
            raise ValueError(f"Prompt base mudou; trecho não encontrado uma única vez: {antes[:60]}")
        texto = texto.replace(antes, depois)
    return texto


def validar_unidade(d: dict, rotulos: set) -> None:
    """validar_janela_v16 da v21 com o conjunto de rótulos da unidade (idêntica para a janela: A1, F, A2)."""
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
                not isinstance(f, dict) or set(f) != {"bloco", "trecho"} or f["bloco"] not in rotulos
                or not _texto(f["trecho"]) for f in fs):
            raise ValueError(f'Questão {k}: fundamentos deve ser lista de {{"bloco": {"|".join(sorted(rotulos))}, '
                             '"trecho": texto}.')
        problemas += [f"Questão {k} ({q['tipo']}): {m}." for m in
                      problemas_tipo(q["tipo"], q["cenario"], q["pergunta"], q["resposta"])]
    problemas += [m[0].upper() + m[1:] + "." for m in problemas_composicao(
        d["status"], [q["tipo"] for q in d["questoes"]], d["motivo"], maximo=MAXIMO_V15, grupos=GRUPOS_V16)]
    if problemas:
        raise ValueError(" ".join(problemas) + " Corrija ou descarte a questão (use parcial e explique em motivo).")


def validar_reparo(d: dict, original: str) -> None:
    if not isinstance(d, dict) or set(d) != {"status", "resposta", "explicacao", "motivo"}:
        raise ValueError("Use exatamente as chaves status, resposta, explicacao e motivo.")
    if d["status"] not in ("ok", "descartar") or not all(isinstance(d[k], str) for k in ("resposta", "explicacao", "motivo")):
        raise ValueError("status deve ser ok ou descartar; resposta, explicacao e motivo são textos.")
    if not d["motivo"].strip():
        raise ValueError("motivo é obrigatório.")
    if d["status"] == "ok":
        n = len(d["resposta"].split())
        if not n or n > 35:
            raise ValueError(f"A resposta mínima deve ter de 1 a 30 palavras (tem {n}); corte o que não é decisivo.")
        if re.sub(r"\W+", " ", d["resposta"]).strip().lower() == re.sub(r"\W+", " ", original).strip().lower():
            raise ValueError("A resposta é igual à anterior: corte as afirmações sem suporte ou use descartar.")


class _Preguicoso:
    """Cliente criado só na primeira chamada (o juiz da deduplicação só existe depois do config)."""
    def __init__(self, fabrica):
        self.fabrica, self.c = fabrica, None

    def json(self, *a, **kw):
        self.c = self.c or self.fabrica()
        return self.c.json(*a, **kw)


class GeracaoAB(GeracaoMeta):
    def __init__(self, saida: Path, itens, *, docs: Path, unidade: str, braco: str = "?", reusar=(),
                 calibracao: Path | None = None, dedup: str = "incremental", sustentacao: bool = False,
                 modelos: dict | None = None, clientes: dict | None = None, embedder=None, workers: int = 8,
                 progress=print):
        if unidade not in C.UNIDADES:
            raise ValueError(f"Unidade inválida: {unidade}")
        if dedup not in ("incremental", "llm"):
            raise ValueError("dedup deve ser incremental ou llm")
        cal = carregar_calibracao(calibracao) if dedup == "incremental" else None
        extra = {"sustentacao": C.SUSTENTACAO, "reparo": C.REPARO}
        if cal:
            extra["dedup_juiz"] = cal["juiz"]
        super().__init__(saida, list(itens), meta=None, modelos={**extra, **(modelos or {})}, reusar=list(reusar or ()),
                         banco_inicial=(), clientes=clientes, workers=workers, onda=max(1, len(list(itens))),
                         progress=progress)
        self.braco, self.unidade, self.docs_dir = braco, unidade, Path(docs)
        self.docs = {i: blocos(i, self.docs_dir)[1] for i in self.itens}
        self.docs_sha = {i: C.sha(read_json(self.docs_dir / i / "documento.json")) for i in self.itens}
        self.sustentacao, self.modo_dedup = sustentacao, dedup
        if unidade == "janela":
            self.prompt_janela = PROMPT_JANELA
        else:
            self.prompt_janela = self.saida / "prompt_capitulo.md"
            self.prompt_janela.parent.mkdir(parents=True, exist_ok=True)
            self.prompt_janela.write_text(prompt_capitulo(), encoding="utf-8")
        self.calibracao, self.dedup = cal, None
        if cal:
            media = np.asarray(read_json(Path(calibracao).parent / cal["media"]), dtype=float)
            self.dedup = DedupIncremental(self.saida / "dedup_incremental", embedder or C.embedder(cal["embedding"], self.saida),
                                          media, cal["limiar_auto"], cal["limiar_juiz"],
                                          _Preguicoso(lambda: self.cliente("dedup_juiz")), progress=progress)

    # ------------------------------------------------------------ configuração
    def config(self) -> None:
        cfg = {"schema": "experimento-ab-geracao-v1", "braco": self.braco, "unidade": self.unidade,
               "docs": C.relativo(self.docs_dir), "docs_sha256": self.docs_sha, "modelos": self.modelos,
               "prompt_janela_sha256": C.sha(self.prompt_janela.read_text(encoding="utf-8")),
               "prompt_composta_sha256": C.sha(prompt_v21("composta")),
               "prompt_auditoria_sha256": C.sha(prompt_v21(PROMPT_AUDITORIA)),
               "prompt_refinador_sha256": C.sha(prompt_v21(PROMPT_REFINO)),
               "exemplos_sha256": C.sha(self.caminho_exemplos.read_text(encoding="utf-8")),
               "combinacoes_por_doc": self.combinacoes_por_doc, "banco_inicial": self.n_banco_inicial,
               "reusar_inventario": [str(r) for r in self.reusar], "dedup": self.modo_dedup,
               "dedup_calibracao": {k: self.calibracao[k] for k in ("embedding", "limiar_auto", "limiar_juiz", "juiz")}
               if self.calibracao else None,
               "sustentacao": self.sustentacao,
               "prompt_sustentacao_sha256": C.sha(C.prompt_gap("faithfulness") + C.prompt("reparo_sustentacao"))
               if self.sustentacao else None}
        path = self.saida / "config.json"
        if path.exists():
            antigo = read_json(path)
            fixos = {k: v for k, v in antigo.items() if k not in ("itens", "criado_em", "origem")}
            if fixos != cfg:
                diff = sorted(k for k in set(fixos) | set(cfg) if fixos.get(k) != cfg.get(k))
                raise ValueError(f"Configuração diferente da pasta existente ({', '.join(diff)}); use outra saída")
            cfg = {**antigo, "itens": sorted(set(antigo["itens"]) | set(self.itens))}
        else:
            from datetime import datetime, timezone
            cfg.update(itens=sorted(self.itens), criado_em=datetime.now(timezone.utc).isoformat())
        atomic_json(path, cfg)

    # ------------------------------------------------------------ contexto da unidade
    def _contexto(self, item: str, foco: int):
        return C.contexto_foco(self.docs[item], foco, self.unidade)

    def _blocos_da_questao(self, q: dict) -> str:
        bs = self.docs[q["item"]]
        return "\n\n".join(f"{bs[i]['titulo_capitulo']} / {bs[i]['subtitulo']}\n{bs[i]['texto']}"
                           for i in C.indices_geracao(q, bs, self.unidade))

    def _blocos_ids(self, q: dict) -> set:
        return set(C.indices_geracao(q, self.docs[q["item"]], self.unidade))

    def janelas(self, rodada: int, itens: list[str] | None = None) -> int:
        itens = itens or self.itens
        system, modelo_usuario, _ = carregar_prompt(4, 4, self.prompt_janela)
        tarefas = [(i, f) for i in itens
                   if rodada == 1 or (self.meta and self.validas(i) < self.meta)
                   for f in self.escolher_janelas(i, rodada)
                   if not (self._dir(i) / "janelas" / f"r{rodada}" / f"{f:03d}.json").exists()]
        self.progress(f"3. {self.unidade}, rodada {rodada}: {len(tarefas)} focos", flush=True)
        anteriores = {i: self._passagens(i) for i in itens}

        def um(t):
            item, foco = t
            jan = self._contexto(item, foco)
            rotulos = {r for r, _ in jan}
            existentes = [f"- [{q['tipo']}] {q['pergunta']} → {q['resposta']}" for j in anteriores[item].get(foco, [])
                          for q in j["questoes"]]
            user = preencher(modelo_usuario, self.temas[item], "", "\n".join(existentes) or "Nenhuma.", jan,
                             self.render_exemplos(item, "simples", f"{item}:{foco}:r{rodada}"))
            nome = f"janela_{item}_r{rodada}_{foco:03d}"
            try:
                d = self.cliente("geracao").json(system, user, tag="meta_janela", max_tokens=16000, item=item,
                                                 validate=lambda d: validar_unidade(d, rotulos))
            except Exception as exc:  # noqa: BLE001
                if not _filtrado(exc):
                    self._falha(nome, exc)
                    return False
                d = {"status": "sem_questoes", "motivo": "bloqueado pelo filtro de conteúdo", "questoes": []}
            textos = {r: b["texto"] for r, b in jan}
            atomic_json(self._dir(item) / "janelas" / f"r{rodada}" / f"{foco:03d}.json", {
                "item": item, "foco": foco, "rodada": rodada, "unidade": self.unidade, "status": d["status"],
                "motivo": d["motivo"], "contexto": {r: b["indice"] for r, b in jan},
                "questoes": [{**q, "verificacoes": verificar(q, textos)} for q in d["questoes"]]})
            self._ok(nome)
            return True

        return self._paralelo(tarefas, um, f"{self.unidade} r{rodada}")

    # ------------------------------------------------------------ sustentação (etapa 4)
    def _arq_sust(self, q: dict) -> Path:
        return self._dir(q["item"]) / "sustentacao" / f"{_nome_arq(q['uid'])}.json"

    def _registros_sust(self, item: str) -> dict:
        if not self.sustentacao:
            return {}
        return {d["uid"]: d for d in (read_json(p) for p in sorted((self._dir(item) / "sustentacao").glob("*.json")))}

    def _remocoes_manuais(self) -> dict:
        out = dict(super()._remocoes_manuais())
        for item in self.itens:
            for uid, d in self._registros_sust(item).items():
                if d["status"] == "descartada":
                    out[uid] = "sem sustentação no texto-fonte: " + d.get("motivo", "")
        return out

    def questoes(self, item: str, aplicar_dedup: bool = True) -> list[dict]:
        out = super().questoes(item, aplicar_dedup)
        reg = self._registros_sust(item)
        for q in out:
            d = reg.get(q["uid"])
            if d:
                q["sustentacao"] = d["status"]
                if d["status"] == "reparada":
                    q["resposta_original"], q["resposta"] = q["resposta"], d["resposta"]
                    q["explicacao"] = d.get("explicacao", "")
        return out

    def _blocos_contexto(self, q: dict) -> list[dict]:
        bs = self.docs[q["item"]]
        return [{"id": f"B{k}", "texto": bs[i]["texto"], "indice_documento": i}
                for k, i in enumerate(C.indices_geracao(q, bs, self.unidade), 1)]

    def sustentar(self, itens: list[str] | None = None) -> int:
        from pipeline.qa_research.benchmark_gap import resumo_faithfulness, validar_faithfulness
        tarefas = [q for item in itens or self.itens for q in self.questoes_sem_dedup(item)
                   if q.get("aprovada") and not self._arq_sust(q).exists()]
        self.progress(f"   sustentação: {len(tarefas)} questões", flush=True)

        def faith(q, blocos_, resposta, tag):
            bmap = {b["id"]: b["texto"] for b in blocos_}
            d = self.cliente("sustentacao").json(
                C.prompt_gap("faithfulness"),
                json.dumps(dict(pergunta=q["pergunta"], gabarito=resposta, blocos=blocos_), ensure_ascii=False),
                tag=tag, max_tokens=12000, item=q["item"], validate=lambda d: validar_faithfulness(d, bmap))
            return d, resumo_faithfulness(d)

        def um(q):
            nome = f"sustentacao_{q['item']}_{_nome_arq(q['uid'])}"
            bl = self._blocos_contexto(q)
            base = {"uid": q["uid"], "item": q["item"], "resposta_original": q["resposta"]}
            try:
                pre, rp = faith(q, bl, q["resposta"], "sust_pre")
                if rp["status"] == "totalmente_sustentado":
                    rec = {**base, "status": "sustentada", "pre": rp, "avaliacao_pre": pre}
                else:
                    sem = [{k: a[k] for k in ("afirmacao", "veredito", "justificativa")}
                           for a in pre["afirmacoes"] if a["veredito"] != "sustentada"]
                    if not sem:   # cobertura incompleta sem afirmação reprovada
                        sem = [{"afirmacao": "(gabarito não coberto por completo)", "veredito": "insuficiente",
                                "justificativa": pre["observacoes"]}]
                    r = self.cliente("reparo").json(
                        C.prompt("reparo_sustentacao"),
                        json.dumps(dict(pergunta=q["pergunta"], gabarito=q["resposta"], afirmacoes_sem_suporte=sem,
                                        blocos=bl), ensure_ascii=False),
                        tag="sust_reparo", max_tokens=8000, item=q["item"],
                        validate=lambda d: validar_reparo(d, q["resposta"]))
                    if r["status"] == "descartar":
                        rec = {**base, "status": "descartada", "motivo": r["motivo"], "pre": rp, "sem_suporte": sem,
                               "avaliacao_pre": pre}
                    else:
                        pos, rpos = faith(q, bl, r["resposta"], "sust_pos")
                        if rpos["status"] == "totalmente_sustentado":
                            rec = {**base, "status": "reparada", "resposta": r["resposta"], "explicacao": r["explicacao"],
                                   "motivo": r["motivo"], "pre": rp, "pos": rpos, "sem_suporte": sem,
                                   "avaliacao_pre": pre, "avaliacao_pos": pos}
                        else:
                            rec = {**base, "status": "descartada", "motivo": "reparo ainda sem sustentação completa",
                                   "resposta_tentada": r["resposta"], "pre": rp, "pos": rpos, "sem_suporte": sem,
                                   "avaliacao_pre": pre, "avaliacao_pos": pos}
            except Exception as exc:  # noqa: BLE001 - isolada por questão
                if not _filtrado(exc):
                    self._falha(nome, exc)
                    return False
                rec = {**base, "status": "bloqueio", "motivo": "filtro de conteúdo; questão mantida sem checagem"}
            atomic_json(self._arq_sust(q), rec)
            self._ok(nome)
            return True

        return self._paralelo(tarefas, um, "sustentação")

    # ------------------------------------------------------------ deduplicação
    def deduplicar(self, itens: list[str] | None = None) -> int:
        falhas = self.sustentar(itens) if self.sustentacao else 0
        if self.dedup is None:
            return falhas + super().deduplicar(itens)
        for item in itens or self.itens:
            cands = [q for q in self.questoes_sem_dedup(item) if q.get("aprovada")]
            falhas += self.dedup.processar(item, cands, falha=self._falha, ok=self._ok)
        return falhas

    def _redundantes(self, item: str) -> dict:
        return self.dedup.redundantes(item) if self.dedup is not None else super()._redundantes(item)

    def relatorio(self) -> dict:
        res = super().relatorio()
        extra = {"braco": self.braco, "unidade": self.unidade, "docs": str(self.docs_dir)}
        if self.dedup is not None:
            dec = [read_json(p) for item in self.itens for p in (self.saida / "dedup_incremental" / item).glob("*.json")]
            extra["dedup_incremental"] = {"decisoes": len(dec),
                                          "por_decisao": {k: sum(d["decisao"] == k for d in dec)
                                                          for k in ("nova", "redundante", "substitui")},
                                          "por_via": {k: sum(d["via"] == k for d in dec)
                                                      for k in ("banco_vazio", "abaixo_do_limiar", "automatico", "juiz")}}
        if self.sustentacao:
            regs = [d for item in self.itens for d in self._registros_sust(item).values()]
            extra["sustentacao"] = {k: sum(d["status"] == k for d in regs)
                                    for k in ("sustentada", "reparada", "descartada", "bloqueio")}
        res.update(extra)
        atomic_json(self.saida / "resultado.json", res)
        return res
