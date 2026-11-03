"""Gerador v22: gerador → régua → auditor → deduplicação, em rodadas por foco até saturar.

Mudanças em relação à v21, cada uma ligada a um defeito observado na revisão do braço B:
  1. o gerador entrega de 0 a 4 questões por foco, sem cota por tipo, e vê os conhecimentos já aceitos no documento
     (os focos de um documento rodam em ondas sequenciais); devolver zero é o sinal de que o foco saturou;
  2. exclusões explícitas no prompt: nomes comerciais, nomenclatura de projeto, itens de lista, princípios genéricos
     do tipo "por que X não garante Y";
  3. gabarito curto (só o elemento decisivo) com a explicação num campo separado, que não entra na avaliação;
  4. auditor por questão, com o texto-fonte e cinco verificações binárias (sem documento, resposta única com a
     alternativa explícita, atalho, sustentação, elemento único);
  5. sem refinador: a correção é feita pelo próprio gerador, que recebe a questão recusada e o motivo e passa de novo
     pela régua, pelo auditor e pela deduplicação. Um foco cuja visita não rendeu conhecimento novo, mas teve recusas
     por qualidade, ganha uma única revisita; uma composta recusada por qualidade ganha uma única segunda tentativa.

Uma questão inválida nunca invalida as outras: a régua e o auditor decidem questão por questão, e cada etapa é um
arquivo (retomável). Inventário (relações e encadeamentos) e deduplicação incremental são os do experimento A/B.
"""
from __future__ import annotations

import hashlib
import json
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from pipeline.qa_research.geracao_tipos.core import _texto
from pipeline.qa_research.geracao_tipos.rodadas import _filtrado, _nome_arq
from pipeline.qa_research.piloto_janela.core import atomic_json, janela, normalizar, read_json
from pipeline.qa_research.tipos import TIPOS, problemas_tipo

from . import comum as C
from .geracao import GeracaoAB

CHAVES = ("tipo", "cenario", "conhecimento", "pergunta", "resposta", "explicacao", "fundamentos")
TIPOS_FOCO = ("conceito", "mecanismo", "consequencia", "diagnostico", "procedimento")
TIPOS_COMPOSTA = ("mecanismo", "consequencia", "diagnostico", "decisao", "procedimento")
TETO_RESPOSTA = 20          # o prompt pede até 15 palavras; a régua tolera 20
TETO_EXPLICACAO = 60
POR_FOCO = 4
VERIFICACOES = (("sem_documento", True, "depende_do_documento"), ("alternativa_excluida", True, "varias_respostas"),
                ("atalho", False, "atalho"), ("sustentada", True, "fora_da_fonte"), ("elemento_unico", True, "nao_unico"))


def _h(*p) -> int:
    return int(hashlib.sha256("|".join(map(str, p)).encode()).hexdigest()[:12], 16)


# ------------------------------------------------------------------ validações
def validar_saida(d: dict, maximo: int) -> None:
    """Só a estrutura geral: defeitos de uma questão são tratados pela régua, questão por questão."""
    if not isinstance(d, dict) or set(d) != {"questoes", "motivo"}:
        raise ValueError("Use exatamente as chaves questoes e motivo.")
    if not isinstance(d["questoes"], list) or not isinstance(d["motivo"], str):
        raise ValueError("questoes deve ser lista e motivo, texto.")
    if len(d["questoes"]) > maximo:
        raise ValueError(f"Entregue no máximo {maximo} questões; zero é aceitável.")
    if not d["questoes"] and not d["motivo"].strip():
        raise ValueError("Sem questões, explique o porquê em motivo.")


def regua(q, textos: dict, tipos: tuple, rotulo_obrigatorio: str | None = None, chaves: tuple = CHAVES) -> list[str]:
    """Checagens determinísticas de uma questão. Lista vazia = segue para o auditor."""
    if not isinstance(q, dict) or set(q) != set(chaves):
        return [f"use exatamente os campos {', '.join(chaves)}"]
    out = [f"{c} vazio" for c in ("conhecimento", "pergunta", "resposta") if not _texto(q[c])]
    if not isinstance(q["explicacao"], str):
        out.append("explicacao deve ser texto")
    elif len(q["explicacao"].split()) > TETO_EXPLICACAO:
        out.append(f"explicação com mais de {TETO_EXPLICACAO} palavras")
    if out:
        return out
    if q["tipo"] not in tipos:
        out.append(f"tipo deve ser um de: {', '.join(tipos)}")
    else:
        out += problemas_tipo(q["tipo"], q["cenario"], q["pergunta"], q["resposta"])
    if len(q["resposta"].split()) > TETO_RESPOSTA:
        out.append(f"resposta com mais de {TETO_RESPOSTA} palavras: deixe só o elemento decisivo")
    fs = q["fundamentos"]
    if not isinstance(fs, list) or not fs or any(
            not isinstance(f, dict) or set(f) != {"bloco", "trecho"} or f["bloco"] not in textos or not _texto(f["trecho"])
            for f in fs):
        out.append(f"fundamentos deve ser lista de {{bloco: {'|'.join(textos)}, trecho}}")
        return out
    literais = [normalizar(f["trecho"]) in normalizar(textos[f["bloco"]]) for f in fs]
    if not any(literais):
        out.append("nenhum fundamento é cópia literal dos blocos")
    elif rotulo_obrigatorio and not any(ok and f["bloco"] == rotulo_obrigatorio for ok, f in zip(literais, fs)):
        out.append(f"nenhum fundamento literal do bloco [{rotulo_obrigatorio}]")
    return out


def validar_auditoria(d: dict) -> None:
    chaves = {"sem_documento", "resposta_alternativa", "alternativa_excluida", "atalho", "sustentada",
              "elemento_unico", "tipo_sugerido", "justificativa"}
    if not isinstance(d, dict) or set(d) != chaves:
        raise ValueError("Use exatamente as chaves: " + ", ".join(sorted(chaves)) + ".")
    for k in ("sem_documento", "alternativa_excluida", "atalho", "sustentada", "elemento_unico"):
        if type(d[k]) is not bool:
            raise ValueError(f"{k} deve ser true ou false.")
    for k in ("resposta_alternativa", "justificativa"):
        if not _texto(d[k]):
            raise ValueError(f"{k} deve ser um texto preenchido.")
    if d["tipo_sugerido"] not in TIPOS:
        raise ValueError(f"tipo_sugerido deve ser um de: {', '.join(TIPOS)}.")


def veredito(d: dict, tipo_declarado: str) -> dict:
    falhas = [m for k, esperado, m in VERIFICACOES if d[k] != esperado]
    return {**d, "aprovada": not falhas, "motivo": falhas[0] if falhas else "nenhum", "falhas": falhas,
            # campos da v21, usados pelas métricas da comparação
            "referencia_valida": d["sem_documento"] and d["alternativa_excluida"] and d["sustentada"] and d["elemento_unico"],
            "tipo_confere": d["tipo_sugerido"] == tipo_declarado}


# ------------------------------------------------------------------ gerador
class GeracaoV22(GeracaoAB):
    VERSAO = "v22"
    CHAVES, TIPOS_FOCO, TIPOS_COMPOSTA = CHAVES, TIPOS_FOCO, TIPOS_COMPOSTA

    def prompt_nome(self, papel: str) -> str:
        return f"{papel}_{self.VERSAO}"

    def sistema(self, papel: str, item: str) -> str:
        """Prompt de sistema de um papel (a v23 acrescenta os exemplos fixos do documento)."""
        return C.prompt(self.prompt_nome(papel))

    def extra_config(self) -> dict:
        return {}

    def regua(self, q, textos, tipos, rotulo_obrigatorio=None) -> list[str]:
        return regua(q, textos, tipos, rotulo_obrigatorio, self.CHAVES)

    def __init__(self, saida: Path, itens, *, docs: Path, braco: str = "?", reusar=(), calibracao: Path,
                 saturacao: dict | None = None, onda: int = 4, modelos: dict | None = None, clientes: dict | None = None,
                 embedder=None, workers: int = 8, progress=print):
        super().__init__(saida, itens, docs=docs, unidade="janela", braco=braco, reusar=reusar, calibracao=calibracao,
                         dedup="incremental", modelos=modelos, clientes=clientes, embedder=embedder, workers=workers,
                         progress=progress)
        s = {"max_rodadas": 5, "paciencia": 1, **(saturacao or {})}
        self.sat = {"max_rodadas": int(s["max_rodadas"]), "paciencia": int(s["paciencia"])}
        if self.sat["max_rodadas"] < 1 or self.sat["paciencia"] < 1:
            raise ValueError("max_rodadas e paciencia devem ser >= 1")
        self.onda_foco = max(1, int(onda))
        # auditorias de uma unidade rodam em paralelo; o semáforo limita as chamadas simultâneas do auditor no total
        # (2 x workers: com 3 documentos e ondas de 4 focos, a v22 sequencial já fazia até 12 auditorias de uma vez)
        self._vagas_auditor = threading.BoundedSemaphore(2 * max(1, int(workers)))

    # -------------------------------------------------------------- configuração
    def config(self) -> None:
        cfg = {"schema": f"experimento-ab-geracao-{self.VERSAO}", "braco": self.braco, "unidade": "janela",
               "docs": C.relativo(self.docs_dir), "docs_sha256": self.docs_sha, "modelos": self.modelos,
               "prompts_sha256": {n: C.sha(C.prompt(n)) for n in (*(self.prompt_nome(p) for p in ("foco", "composta", "auditoria")),
                                                                 "dedup_par")},
               "exemplos_sha256": C.sha(self.caminho_exemplos.read_text(encoding="utf-8")),
               "combinacoes_por_doc": self.combinacoes_por_doc, "reusar_inventario": [str(r) for r in self.reusar],
               "dedup_calibracao": {k: self.calibracao[k] for k in ("embedding", "limiar_auto", "limiar_juiz", "juiz")},
               "saturacao": self.sat, "onda": self.onda_foco, "por_foco": POR_FOCO, "teto_resposta": TETO_RESPOSTA,
               "segunda_chance": 1, **self.extra_config()}
        path = self.saida / "config.json"
        if path.exists():
            antigo = read_json(path)
            fixos = {k: v for k, v in antigo.items() if k not in ("itens", "criado_em", "origem")}
            if fixos != cfg:
                diff = sorted(k for k in set(fixos) | set(cfg) if fixos.get(k) != cfg.get(k))
                raise ValueError(f"Configuração diferente da pasta existente ({', '.join(diff)}); use outra saída")
            cfg = {**antigo, "itens": sorted(set(antigo["itens"]) | set(self.itens))}
        else:
            cfg.update(itens=sorted(self.itens), criado_em=datetime.now(timezone.utc).isoformat())
        atomic_json(path, cfg)

    # -------------------------------------------------------------- estado a partir dos arquivos
    def _arq_foco(self, item, r, f) -> Path:
        return self._dir(item) / "focos" / f"r{r}" / f"{f:03d}.json"

    def _arq_composta(self, item, cid, tentativa: int = 1) -> Path:
        pasta = self._dir(item) / "compostas_v22"
        return (pasta if tentativa == 1 else pasta / f"t{tentativa}") / f"{cid}.json"

    @staticmethod
    def _prefixo_composta(item, cid, tentativa: int = 1) -> str:
        return f"{item}:c:{cid}" + ("" if tentativa == 1 else f":t{tentativa}")

    def _arq_aud(self, item, uid) -> Path:
        return self._dir(item) / "auditoria_v22" / f"{_nome_arq(uid)}.json"

    def questoes(self, item: str, aplicar_dedup: bool = True) -> list[dict]:
        out = []
        for t in (1, 2):
            pasta = self._arq_composta(item, "x", t).parent
            for p in sorted(pasta.glob("*.json"), key=lambda p: int(p.stem[1:])):
                d = read_json(p)
                for q in d["questoes"]:
                    out.append(self._registro(item, q, f"{self._prefixo_composta(item, d['id'], t)}:{q['k']}", "composta",
                                              0, {"blocos": d["blocos"], "foco": None, "encadeamento": d["id"],
                                                  "tentativa": t}))
        for p in sorted((self._dir(item) / "focos").glob("r*/*.json"), key=lambda p: (int(p.parent.name[1:]), p.stem)):
            d = read_json(p)
            for q in d["questoes"]:
                out.append(self._registro(item, q, f"{item}:j:r{d['rodada']}:{d['foco']:03d}:{q['k']}", "janela",
                                          d["rodada"], {"foco": d["foco"]}))
        removidas = self.dedup.redundantes(item) if aplicar_dedup else {}
        pasta = self.saida / "dedup_incremental" / item
        decididas = {p.stem for p in pasta.glob("*.json")} if aplicar_dedup else set()
        for q in out:
            if q["uid"] in removidas:
                q["redundante"] = removidas[q["uid"]]
            q["aprovada"] = bool(q.get("aprovada_auditor") and (not aplicar_dedup or (
                _nome_arq(q["uid"]) in decididas and q["uid"] not in removidas)))
        return out

    def _registro(self, item, q, uid, origem, rodada, extra) -> dict:
        r = {"uid": uid, "item": item, "origem": origem, "rodada": rodada, "composicao":
             "composta" if origem == "composta" else "simples", **extra, "regua": q.get("regua", [])}
        if isinstance(q, dict) and all(k in q for k in self.CHAVES):
            r.update({k: q[k] for k in self.CHAVES}, tipo_declarado=q["tipo"])
        aud = self._arq_aud(item, uid)
        if not r["regua"] and aud.exists():
            a = read_json(aud)
            r["auditoria"] = a
            r["aprovada_auditor"] = a["aprovada"]
            r["tipo"] = a["tipo_sugerido"]
        return r

    def _aceitas(self, item) -> list[dict]:
        return [q for q in self.questoes(item) if q.get("aprovada")]

    def _decisoes(self, item) -> dict:
        return {d["uid"]: d for d in (read_json(p) for p in (self.saida / "dedup_incremental" / item).glob("*.json"))}

    # -------------------------------------------------------------- prompts
    def _exemplos(self, item: str, semente: str, composta: bool) -> str:
        # só exemplos que já seguem o formato v22 (resposta curta): os demais ensinariam o contrário da regra
        ex = [e for e in self.base["exemplos"] if len(e["resposta"].split()) <= 15]
        if composta:
            pool = [e for e in ex if e.get("composicao") == "composta" and e["item"] != item] or \
                   [e for e in ex if e.get("composicao") == "composta"]
            escolhidos = sorted(pool, key=lambda e: _h(semente, e["id"]))[:3]
        else:
            escolhidos = []
            for t in self.TIPOS_FOCO:
                pool = [e for e in ex if e["tipo"] == t and e["item"] != item and e.get("composicao", "simples") == "simples"]
                pool = pool or [e for e in ex if e["tipo"] == t]
                pool = [e for e in pool if e["tipo"] == t]
                if pool:
                    escolhidos.append(pool[_h(semente, t) % len(pool)])
        contra = sorted(self.base["contraexemplos"], key=lambda c: _h(semente, c["id"]))[:5]
        bons = "\n\n".join(f"[{e['tipo']}] Pergunta: {e['pergunta']}\nResposta: {e['resposta']}\nPor que é boa: {e['por_que']}"
                           for e in escolhidos)
        ruins = "\n\n".join(f"[{c['tipo']}] Pergunta: {c['pergunta']}\nResposta: {c['resposta']}\nProblema: {c['problema']}"
                            for c in contra)
        return f"<exemplos>\n{bons}\n</exemplos>\n\n<contraexemplos>\n{ruins}\n</contraexemplos>"

    def _cobertos(self, item) -> str:
        linhas = [f"- {q['conhecimento']} (resposta: {q['resposta']})" for q in self._aceitas(item)]
        return "\n".join(linhas) or "Nenhum ainda."

    @staticmethod
    def _estado(q) -> str | None:
        """Como uma questão já proposta aparece para o gerador (None = ainda sem decisão)."""
        if "pergunta" not in q:
            return None
        if q.get("aprovada"):
            return "aceita"
        if q["regua"]:
            return "recusada pela régua: " + q["regua"][0]
        if q.get("redundante"):
            return "recusada: repete conhecimento já aceito"
        if "auditoria" in q:
            a = q["auditoria"]
            extra = f" Resposta alternativa apontada: {a['resposta_alternativa']}" if "varias_respostas" in a["falhas"] else ""
            return f"recusada ({a['motivo']}): {a['justificativa']}{extra}"
        return None

    @staticmethod
    def _recusada_por_qualidade(q) -> bool:
        """Recusa que uma nova tentativa pode corrigir (régua ou auditor); redundância e bloqueio não contam."""
        if q["regua"]:
            return True
        a = q.get("auditoria")
        return bool(a) and not a["aprovada"] and a["motivo"] != "bloqueio"

    def _historico_foco(self, item, foco) -> str:
        linhas = [f"- [{e}] {q['pergunta']} → {q['resposta']}" for q in self.questoes(item)
                  if q.get("foco") == foco and (e := self._estado(q))]
        return "\n".join(linhas) or "Nenhuma."

    def _tema(self, item) -> str:
        t = self.temas[item]
        return (f"<tema>\nÁrea: {t['area']}\nTema: {t['tema']}\n</tema>\n\n"
                f"<escopo_orientador>\n{t['escopo']}\n</escopo_orientador>")

    # -------------------------------------------------------------- auditoria (uma chamada por questão)
    def _auditar(self, item: str, uid: str, q: dict, blocos_txt: str) -> bool:
        arq = self._arq_aud(item, uid)
        if arq.exists():
            return True
        nome = f"auditoria_{item}_{_nome_arq(uid)}"
        user = json.dumps({"tipo_declarado": q["tipo"], "pergunta": q["pergunta"], "resposta_referencia": q["resposta"],
                           "explicacao_do_autor": q["explicacao"], "blocos": blocos_txt}, ensure_ascii=False)
        try:
            d = self.cliente("auditoria").json(C.prompt(self.prompt_nome("auditoria")), user, tag=f"{self.VERSAO}_auditoria",
                                               max_tokens=6000,
                                               item=item, validate=validar_auditoria)
            rec = {"uid": uid, **veredito(d, q["tipo"])}
        except Exception as exc:  # noqa: BLE001 - isolada por questão
            if not _filtrado(exc):
                self._falha(nome, exc)
                return False
            rec = {"uid": uid, "sem_documento": False, "resposta_alternativa": "-", "alternativa_excluida": False,
                   "atalho": False, "sustentada": False, "elemento_unico": False, "tipo_sugerido": q["tipo"],
                   "justificativa": "bloqueada pelo filtro de conteúdo", "aprovada": False, "motivo": "bloqueio",
                   "falhas": ["bloqueio"], "referencia_valida": False, "tipo_confere": True}
        atomic_json(arq, rec)
        self._ok(nome)
        return True

    def _auditar_unidade(self, item, d, prefixo, blocos_txt) -> bool:
        """Audita as questões da unidade em paralelo (cada uma é independente e vira um arquivo próprio)."""
        pendentes = [q for q in d["questoes"] if not q["regua"]
                     and not self._arq_aud(item, f"{prefixo}:{q['k']}").exists()]
        if not pendentes:
            return True

        def auditar(q) -> bool:
            with self._vagas_auditor:
                return self._auditar(item, f"{prefixo}:{q['k']}", q, blocos_txt)

        with ThreadPoolExecutor(max_workers=len(pendentes)) as pool:
            return all(list(pool.map(auditar, pendentes)))

    # -------------------------------------------------------------- unidades de geração
    def _foco(self, item: str, rodada: int, foco: int) -> bool:
        arq, nome = self._arq_foco(item, rodada, foco), f"foco_{item}_r{rodada}_{foco:03d}"
        jan = janela(self.docs[item], foco)
        textos = {r: b["texto"] for r, b in jan}
        bloco_txt = "\n\n".join(f"[{r}] {b['titulo_capitulo']} / {b['subtitulo']}\n{b['texto']}" for r, b in jan)
        if not arq.exists():
            user = "\n\n".join(filter(None, (self._tema(item), f"<conhecimentos_cobertos>\n{self._cobertos(item)}\n</conhecimentos_cobertos>",
                                f"<questoes_deste_foco>\n{self._historico_foco(item, foco)}\n</questoes_deste_foco>",
                                self._exemplos(item, f"{item}:{foco}:r{rodada}", composta=False),
                                f"<janela>\n{bloco_txt}\n</janela>")))
            try:
                d = self.cliente("geracao").json(self.sistema("foco", item), user, tag=f"{self.VERSAO}_foco", max_tokens=16000,
                                                 item=item,
                                                 validate=lambda d: validar_saida(d, POR_FOCO))
            except Exception as exc:  # noqa: BLE001
                if not _filtrado(exc):
                    self._falha(nome, exc)
                    return False
                d = {"questoes": [], "motivo": "bloqueado pelo filtro de conteúdo"}
            atomic_json(arq, {"item": item, "foco": foco, "rodada": rodada, "contexto": {r: b["indice"] for r, b in jan},
                              "motivo": d["motivo"],
                              "questoes": [{**q, "k": k, "regua": self.regua(q, textos, self.TIPOS_FOCO, "F")} if isinstance(q, dict)
                                           else {"k": k, "regua": ["questão não é um objeto"]}
                                           for k, q in enumerate(d["questoes"], 1)]})
            self._ok(nome)
        return self._auditar_unidade(item, read_json(arq), f"{item}:j:r{rodada}:{foco:03d}", bloco_txt)

    def _composta(self, item: str, c: dict, rels: list[dict], tentativa: int = 1) -> bool:
        arq = self._arq_composta(item, c["id"], tentativa)
        nome = f"composta_{item}_{c['id']}" + ("" if tentativa == 1 else f"_t{tentativa}")
        bs = {b["indice"]: b for b in self.docs[item]}
        usados = sorted({r["bloco"] for r in rels})
        rot = {f"B{k}": i for k, i in enumerate(usados, 1)}
        textos = {r: bs[i]["texto"] for r, i in rot.items()}
        bloco_txt = "\n\n".join(f"[{r}] {bs[i]['titulo_capitulo']} / {bs[i]['subtitulo']}\n{bs[i]['texto']}" for r, i in rot.items())
        if not arq.exists():
            enc = {k: c[k] for k in ("tipo", "titulo", "ponte", "cadeia", "cenario", "resposta", "resposta_atraente",
                                     "sinal_que_descarta", "condicoes_enunciado", "limites") if k in c}
            enc["relacoes"] = [{k: r[k] for k in ("id", "afirmacao", "condicoes", "limites")} for r in rels]
            partes = [self._tema(item), f"<conhecimentos_cobertos>\n{self._cobertos(item)}\n</conhecimentos_cobertos>",
                      f"<encadeamento>\n{json.dumps(enc, ensure_ascii=False, indent=2)}\n</encadeamento>"]
            if tentativa > 1:
                anteriores = [f"- [{e}] {q['pergunta']} → {q['resposta']}" for q in self.questoes(item)
                              if q.get("encadeamento") == c["id"] and q["tentativa"] < tentativa and (e := self._estado(q))]
                partes.append("<tentativa_anterior>\n" + "\n".join(anteriores) + "\n</tentativa_anterior>")
            semente = f"{item}:{c['id']}" + ("" if tentativa == 1 else f":t{tentativa}")
            partes += [self._exemplos(item, semente, composta=True), f"<blocos>\n{bloco_txt}\n</blocos>"]
            user = "\n\n".join(p for p in partes if p)
            try:
                d = self.cliente("geracao").json(self.sistema("composta", item), user, tag=f"{self.VERSAO}_composta",
                                                 max_tokens=12000,
                                                 item=item, validate=lambda d: validar_saida(d, 1))
            except Exception as exc:  # noqa: BLE001
                if not _filtrado(exc):
                    self._falha(nome, exc)
                    return False
                d = {"questoes": [], "motivo": "bloqueado pelo filtro de conteúdo"}
            atomic_json(arq, {"item": item, "id": c["id"], "tentativa": tentativa, "blocos": usados, "rotulos": rot,
                              "motivo": d["motivo"],
                              "questoes": [{**q, "k": k, "regua": self.regua(q, textos, self.TIPOS_COMPOSTA)} if isinstance(q, dict)
                                           else {"k": k, "regua": ["questão não é um objeto"]}
                                           for k, q in enumerate(d["questoes"], 1)]})
            self._ok(nome)
        return self._auditar_unidade(item, read_json(arq), self._prefixo_composta(item, c["id"], tentativa), bloco_txt)

    def _segundas_compostas(self, item: str, cadeias: list) -> list:
        """Encadeamentos cuja 1ª tentativa terminou com questão recusada por qualidade (ou cuja 2ª já começou)."""
        qs = self.questoes(item, aplicar_dedup=False)
        out = []
        for t in cadeias:
            cid = t[0]["id"]
            if self._arq_composta(item, cid, 2).exists():
                out.append(t)
                continue
            q1 = [q for q in qs if q.get("encadeamento") == cid and q["tentativa"] == 1]
            completa = all(q["regua"] or "auditoria" in q for q in q1)
            if q1 and completa and any(self._recusada_por_qualidade(q) for q in q1):
                out.append(t)
        return out

    # -------------------------------------------------------------- ondas e saturação
    def _ondas(self, unidades: list) -> list[list]:
        """Ondas de até `onda` unidades distantes entre si no documento (menos sobreposição dentro da onda)."""
        n = len(unidades)
        if not n:
            return []
        passo = -(-n // self.onda_foco)
        return [[unidades[t + passo * k] for k in range(self.onda_foco) if t + passo * k < n] for t in range(passo)]

    def _rodar_ondas(self, item, unidades, funcao) -> int:
        falhas = 0
        for onda in self._ondas(unidades):
            with ThreadPoolExecutor(max_workers=len(onda)) as pool:
                falhas += sum(not ok for ok in pool.map(funcao, onda))
            cands = [q for q in self.questoes(item, aplicar_dedup=False) if q.get("aprovada_auditor")]
            falhas += self.dedup.processar(item, cands, falha=self._falha, ok=self._ok)
        return falhas

    def ganhos(self, item) -> dict:
        """foco -> {rodada: conhecimentos novos aceitos} (substituições não contam como conhecimento novo)."""
        dec = self._decisoes(item)
        out = defaultdict(lambda: defaultdict(int))
        for q in self._aceitas(item):
            if q.get("foco") is not None and dec.get(q["uid"], {}).get("decisao") == "nova":
                out[q["foco"]][q["rodada"]] += 1
        return out

    def _visitas(self, item) -> dict:
        out = defaultdict(list)
        for p in (self._dir(item) / "focos").glob("r*/*.json"):
            out[int(p.stem)].append(int(p.parent.name[1:]))
        return {f: sorted(v) for f, v in out.items()}

    def _completo(self, item: str, rodada: int, foco: int) -> bool:
        """A visita do foco terminou: todas as questões passaram pela régua, pelo auditor e (se aprovadas) pela
        deduplicação. Só então o ganho da visita é conhecido e o foco pode abrir na rodada seguinte."""
        arq = self._arq_foco(item, rodada, foco)
        if not arq.exists():
            return False
        pasta = self.saida / "dedup_incremental" / item
        for q in read_json(arq)["questoes"]:
            if q["regua"]:
                continue
            uid = f"{item}:j:r{rodada}:{foco:03d}:{q['k']}"
            aud = self._arq_aud(item, uid)
            if not aud.exists() or (read_json(aud)["aprovada"] and not (pasta / f"{_nome_arq(uid)}.json").exists()):
                return False
        return True

    def focos_abertos(self, item: str, rodada: int) -> list[int]:
        if rodada == 1:
            return list(range(len(self.docs[item])))
        g, vis, out = self.ganhos(item), self._visitas(item), []
        recusas = Counter((q["foco"], q["rodada"]) for q in self.questoes(item, aplicar_dedup=False)
                          if q["origem"] == "janela" and self._recusada_por_qualidade(q))
        for f in range(len(self.docs[item])):
            v = [r for r in vis.get(f, []) if r < rodada]
            if not v or v[-1] != rodada - 1 or len(v) >= self.sat["max_rodadas"]:
                continue
            if not self._completo(item, rodada - 1, f):
                continue   # visita anterior com falha pendente: o foco espera a retomada
            if not read_json(self._arq_foco(item, rodada - 1, f))["questoes"]:
                continue   # o gerador disse que não há mais nada: foco saturado
            if any(g[f][r] > 0 for r in v[-self.sat["paciencia"]:]):
                out.append(f)
            elif recusas[(f, rodada - 1)] and sum(g[f][r] == 0 for r in v) == 1:
                out.append(f)   # segunda chance: visita sem ganho, mas com recusas corrigíveis (uma vez por foco)
        return out

    def _documento(self, item: str) -> int:
        arq = self._dir(item) / "combinacoes.json"
        if not arq.exists():
            self.progress(f"[{item}] sem inventário de encadeamentos; repita para tentar de novo", flush=True)
            return 1
        rels = {r["id"]: r for p in sorted((self._dir(item) / "relacoes").glob("*.json")) for r in read_json(p)["relacoes"]}
        cadeias = [(c, [rels[i] for i in c["relacoes"] if i in rels]) for c in read_json(arq)["combinacoes"]]
        # Falhas ficam isoladas: uma composta ou um foco com falha não impede os demais; o foco com falha só volta
        # a abrir depois que a retomada completar a sua visita (ver _completo).
        falhas = self._rodar_ondas(item, cadeias, lambda t: self._composta(item, *t))
        segundas = self._segundas_compostas(item, cadeias)
        falhas += self._rodar_ondas(item, segundas, lambda t: self._composta(item, *t, tentativa=2))
        self.progress(f"[{item}] compostas: {len(cadeias)} encadeamentos, {len(segundas)} segundas tentativas | "
                      f"aceitas {len(self._aceitas(item))}", flush=True)
        for rodada in range(1, self.sat["max_rodadas"] + 1):
            abertos = self.focos_abertos(item, rodada)
            if not abertos:
                break
            f_rodada = self._rodar_ondas(item, abertos, lambda f, r=rodada: self._foco(item, r, f))
            falhas += f_rodada
            novos = sum(self.ganhos(item)[f][rodada] for f in abertos)
            self.progress(f"[{item}] rodada {rodada}: {len(abertos)} focos | {novos} conhecimentos novos | "
                          f"aceitas {len(self._aceitas(item))} | falhas {f_rodada}", flush=True)
        return falhas

    # -------------------------------------------------------------- execução
    def run(self) -> int:
        self.config()
        falhas = self.inventario()
        with ThreadPoolExecutor(max_workers=max(1, len(self.itens))) as pool:
            falhas += sum(pool.map(self._documento, self.itens))
        self.finalizar(self.itens)
        self.relatorio()
        marcador = self.saida / "geracao_concluida.json"
        if falhas:
            marcador.unlink(missing_ok=True)
        else:
            atomic_json(marcador, {"em": datetime.now(timezone.utc).isoformat()})
        return falhas

    def finalizar(self, itens) -> None:
        pendentes = {p.stem for p in (self.saida / "falhas").glob("*.json")}
        for item in itens:
            if any(item in f for f in pendentes):
                continue
            C.gravar_jsonl(self._dir(item) / "aprovadas.jsonl", self._aceitas(item))

    def relatorio(self) -> dict:
        todas = [q for i in self.itens for q in self.questoes(i)]
        aprovadas = [q for q in todas if q.get("aprovada")]
        C.gravar_jsonl(self.saida / "questoes.jsonl", todas)
        C.gravar_jsonl(self.saida / "aprovadas.jsonl", aprovadas)
        unidades = [read_json(p) for i in self.itens for p in list((self._dir(i) / "focos").glob("r*/*.json"))
                    + list((self._dir(i) / "compostas_v22").glob("*.json"))
                    + list((self._dir(i) / "compostas_v22").glob("t*/*.json"))]

        def funil(qs):
            aud = [q for q in qs if "auditoria" in q]
            return {"propostas": len(qs), "reprovadas_regua": sum(bool(q["regua"]) for q in qs), "auditadas": len(aud),
                    "aprovadas_auditor": sum(q["auditoria"]["aprovada"] for q in aud),
                    "falhas_auditor": dict(Counter(f for q in aud for f in q["auditoria"]["falhas"])),
                    "redundantes": sum(bool(q.get("redundante")) for q in qs),
                    "finais": sum(bool(q.get("aprovada")) for q in qs)}

        dec = [read_json(p) for i in self.itens for p in (self.saida / "dedup_incremental" / i).glob("*.json")]
        por_rodada, focos, revisitas = defaultdict(int), {}, Counter()
        for i in self.itens:
            g, vis = self.ganhos(i), self._visitas(i)
            for f, v in vis.items():
                focos[f"{i}:{f:03d}"] = {"visitas": len(v), "novos_por_rodada": [g[f][r] for r in v]}
                for r in v:
                    por_rodada[r] += g[f][r]
                for anterior, r in zip(v, v[1:]):
                    if g[f][anterior] == 0:   # revisita depois de uma visita sem ganho (segunda chance)
                        revisitas["visitas"] += 1
                        revisitas["conhecimentos_novos"] += g[f][r]
        segunda = [q for q in todas if q.get("tentativa") == 2]
        res = {"braco": self.braco, "gerador": "v22", "unidade": "janela", "docs": C.relativo(self.docs_dir),
               "total": funil(todas), "por_origem": {o: funil([q for q in todas if q["origem"] == o])
                                                       for o in ("janela", "composta")},
               "por_item": {i: funil([q for q in todas if q["item"] == i]) for i in self.itens},
               "chamadas": {"total": len(unidades), "vazias": sum(not u["questoes"] for u in unidades),
                            "questoes_por_chamada": dict(sorted(Counter(len(u["questoes"]) for u in unidades).items()))},
               "motivos_vazias": dict(Counter(u["motivo"][:80] for u in unidades if not u["questoes"]).most_common(8)),
               "regua": dict(Counter(m.split(":")[0][:60] for q in todas for m in q["regua"]).most_common(10)),
               "tipos_finais": dict(Counter(q.get("tipo") for q in aprovadas)),
               "dedup_incremental": {"decisoes": len(dec),
                                     "por_decisao": {k: sum(d["decisao"] == k for d in dec) for k in ("nova", "redundante", "substitui")},
                                     "por_via": {k: sum(d["via"] == k for d in dec)
                                                 for k in ("banco_vazio", "abaixo_do_limiar", "automatico", "juiz")}},
               "segunda_chance": {"focos": {"visitas": revisitas["visitas"],
                                            "conhecimentos_novos": revisitas["conhecimentos_novos"]},
                                  "compostas": {"tentativas": sum(u.get("tentativa") == 2 for u in unidades),
                                                "finais": sum(bool(q.get("aprovada")) for q in segunda)}},
               "saturacao": {"config": self.sat, "conhecimentos_novos_por_rodada": dict(sorted(por_rodada.items())),
                             "focos_por_numero_de_visitas": dict(sorted(Counter(v["visitas"] for v in focos.values()).items())),
                             "focos": focos},
               "falhas_pendentes": sorted(p.stem for p in (self.saida / "falhas").glob("*.json"))}
        atomic_json(self.saida / "resultado.json", res)
        atomic_json(self.saida / "saturacao.json", res["saturacao"])
        t = res["total"]
        l = ["# Geração v22", "",
             f"Braço {self.braco}: {t['finais']} questões finais de {t['propostas']} propostas "
             f"({t['reprovadas_regua']} recusadas pela régua, {t['aprovadas_auditor']}/{t['auditadas']} aprovadas pelo "
             f"auditor, {t['redundantes']} redundantes).", "",
             f"Chamadas do gerador: {res['chamadas']['total']}, das quais {res['chamadas']['vazias']} sem questões; "
             f"questões por chamada: {res['chamadas']['questoes_por_chamada']}.",
             f"Falhas do auditor por verificação: {t['falhas_auditor']}.",
             f"Segunda chance: {res['segunda_chance']['focos']['visitas']} revisitas de foco após visita sem ganho "
             f"({res['segunda_chance']['focos']['conhecimentos_novos']} conhecimentos novos); "
             f"{res['segunda_chance']['compostas']['tentativas']} segundas tentativas de composta "
             f"({res['segunda_chance']['compostas']['finais']} finais).",
             f"Conhecimentos novos por rodada: {res['saturacao']['conhecimentos_novos_por_rodada']}; "
             f"focos por número de visitas: {res['saturacao']['focos_por_numero_de_visitas']}.",
             f"Tipos finais: {res['tipos_finais']}.", f"Falhas pendentes: {len(res['falhas_pendentes'])}.", "",
             "## Amostra de questões finais", ""]
        for q in sorted(aprovadas, key=lambda q: _h("md", q["uid"]))[:15]:
            l += [f"**[{q['item']} · {q.get('tipo')} · {q['origem']}]** {q['pergunta']}", "", f"- Resposta: {q['resposta']}",
                  f"- Explicação: {q.get('explicacao', '')}", ""]
        (self.saida / "RELATORIO.md").write_text("\n".join(l), encoding="utf-8")
        return res
