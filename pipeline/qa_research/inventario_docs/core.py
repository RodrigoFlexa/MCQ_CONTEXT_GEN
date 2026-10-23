"""Piloto: inventário leve sobre os documentos v2 (estilo qa_v7) x configuração EC, com avaliação cega.

Etapas (todas retomáveis; cada unidade de trabalho vira um arquivo):
  1. relações: cada bloco dos documentos vira relações técnicas avaliáveis, com trecho literal.
  2. combinações: por documento, pares ou trios de relações de blocos diferentes que interagem
     (base das difíceis B, como em pipeline/inventario/combinacoes.py).
  3. alvos: seleção estável de fácil, média, difícil A e difícil B, espalhada pelos blocos.
  4. questões: uma chamada por alvo (o gerador só redige; o alvo já vem pronto).
  5. amostra EC: questões da configuração atual (janela de 3 blocos, exemplos E+C), na mesma
     proporção de níveis e documentos.
  6. avaliação cega: um modelo pequeno responde sem contexto; um juiz forte compara com a referência.
  7. relatório: acurácia do respondente por método e dificuldade.
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
import re
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from pipeline.qa_research.piloto_janela.core import (QA, ROOT, atomic_json, blocos, normalizar, palavras,
                                                     read_json, tema)

AQUI = Path(__file__).resolve().parent
PROMPTS = AQUI / "prompts"
ITENS = ("01_01", "02_02")
MODELOS = {
    "relacoes": "gpt-5-4-petrobras:low",
    "combinacoes": "gpt-5-4-petrobras:high",
    "questao": "gpt-5-4-petrobras:high",
    "respondente": "gpt-4-1-nano-petrobras",
    "juiz": "gpt-5-4-petrobras:high",
}
PROPORCAO = {"facil": 0.25, "media": 0.50, "dificil_A": 0.125, "dificil_B": 0.125}
TIPOS_REL = ("definicao", "mecanismo", "causa_efeito", "condicao", "criterio", "comparacao", "aplicacao")
NIVEIS_REL = ("facil", "media", "dificil_A")
VEREDITOS = {"correta": 1.0, "parcial": 0.5, "incorreta": 0.0}
CAMPOS_REL = ("afirmacao", "tipo", "condicoes", "limites", "trecho", "niveis", "explicacao_concorrente",
              "condicao_que_distingue")
CAMPOS_COMB = ("relacoes", "titulo", "ligacao", "raciocinio", "cenario", "resposta", "criterios_correcao",
               "condicoes_enunciado", "limites")


def prompt(nome: str, **valores) -> str:
    texto = (PROMPTS / f"{nome}.md").read_text(encoding="utf-8").strip()
    for k, v in valores.items():
        texto = texto.replace("{{" + k + "}}", str(v))
    if "{{" in texto:
        raise ValueError(f"Marcador não preenchido em {nome}.md")
    return texto


def _lista_textos(v) -> bool:
    return isinstance(v, list) and all(isinstance(x, str) for x in v)


def _texto(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _rng(*partes) -> random.Random:
    return random.Random(int(hashlib.sha256("|".join(map(str, partes)).encode()).hexdigest()[:16], 16))


# ---------------------------------------------------------------- validações (formato e ancoragem)
def validar_relacoes(d: dict, texto_bloco: str) -> None:
    if not isinstance(d, dict) or set(d) != {"status", "motivo", "relacoes"}:
        raise ValueError("Use exatamente as chaves status, motivo e relacoes.")
    if d["status"] not in ("ok", "sem_relacoes") or not isinstance(d["relacoes"], list):
        raise ValueError("status deve ser ok ou sem_relacoes; relacoes, uma lista.")
    if d["status"] == "sem_relacoes" and (d["relacoes"] or not _texto(d["motivo"])):
        raise ValueError("sem_relacoes exige lista vazia e motivo.")
    if d["status"] == "ok" and not 1 <= len(d["relacoes"]) <= 8:
        raise ValueError("status ok exige de 1 a 8 relações.")
    bloco = normalizar(texto_bloco).lower()
    for k, r in enumerate(d["relacoes"], 1):
        if not isinstance(r, dict) or set(r) != set(CAMPOS_REL):
            raise ValueError(f"Relação {k}: use exatamente os campos {', '.join(CAMPOS_REL)}.")
        if not _texto(r["afirmacao"]) or r["tipo"] not in TIPOS_REL:
            raise ValueError(f"Relação {k}: afirmacao vazia ou tipo inválido.")
        if not (_lista_textos(r["condicoes"]) and _lista_textos(r["limites"])):
            raise ValueError(f"Relação {k}: condicoes e limites devem ser listas de textos.")
        if not r["niveis"] or not isinstance(r["niveis"], list) or not set(r["niveis"]) <= set(NIVEIS_REL):
            raise ValueError(f"Relação {k}: niveis deve conter facil, media e/ou dificil_A.")
        if "dificil_A" in r["niveis"] and not (_texto(r["explicacao_concorrente"])
                                               and _texto(r["condicao_que_distingue"])):
            raise ValueError(f"Relação {k}: dificil_A exige explicacao_concorrente e condicao_que_distingue.")
        if not _texto(r["trecho"]) or normalizar(r["trecho"]).lower().strip(" .;:\"'") not in bloco:
            raise ValueError(f"Relação {k}: trecho deve ser cópia literal do bloco.")


def validar_combinacoes(d: dict, bloco_da_relacao: dict, maximo: int) -> None:
    if not isinstance(d, dict) or set(d) != {"combinacoes", "observacao"}:
        raise ValueError("Use exatamente as chaves combinacoes e observacao.")
    if not isinstance(d["combinacoes"], list) or len(d["combinacoes"]) > maximo:
        raise ValueError(f"combinacoes deve ser lista com no máximo {maximo} itens.")
    for k, c in enumerate(d["combinacoes"], 1):
        if not isinstance(c, dict) or set(c) != set(CAMPOS_COMB):
            raise ValueError(f"Combinação {k}: use exatamente os campos {', '.join(CAMPOS_COMB)}.")
        ids = c["relacoes"]
        if not isinstance(ids, list) or not 2 <= len(ids) <= 3 or any(i not in bloco_da_relacao for i in ids):
            raise ValueError(f"Combinação {k}: informe 2 ou 3 ids de relações existentes.")
        if len({bloco_da_relacao[i] for i in ids}) < 2:
            raise ValueError(f"Combinação {k}: as relações devem vir de blocos diferentes.")
        for campo in ("titulo", "ligacao", "raciocinio", "cenario", "resposta"):
            if not _texto(c[campo]):
                raise ValueError(f"Combinação {k}: {campo} vazio.")
        if not all(_lista_textos(c[x]) for x in ("criterios_correcao", "condicoes_enunciado", "limites")):
            raise ValueError(f"Combinação {k}: listas de textos esperadas.")


def validar_questao(d: dict) -> None:
    if not isinstance(d, dict) or set(d) != {"status", "motivo", "pergunta", "resposta"}:
        raise ValueError("Use exatamente as chaves status, motivo, pergunta e resposta.")
    if d["status"] == "ok":
        if not (_texto(d["pergunta"]) and _texto(d["resposta"])):
            raise ValueError("status ok exige pergunta e resposta.")
        if palavras(d["resposta"]) > 50:
            raise ValueError("A resposta deve ter até 50 palavras.")
    elif d["status"] == "insuficiente":
        if not _texto(d["motivo"]):
            raise ValueError("insuficiente exige motivo.")
    else:
        raise ValueError("status deve ser ok ou insuficiente.")


def validar_resposta(d: dict) -> None:
    if not isinstance(d, dict) or not isinstance(d.get("resposta"), str):
        raise ValueError('Retorne {"resposta": "..."}.')


def validar_juiz(d: dict, ids: list[str]) -> None:
    av = d.get("avaliacoes") if isinstance(d, dict) else None
    if not isinstance(av, list) or [a.get("id") for a in av] != ids:
        raise ValueError("Devolva exatamente um objeto por id recebido, na mesma ordem.")
    for a in av:
        if a.get("veredito") not in VEREDITOS or not isinstance(a.get("referencia_valida"), bool):
            raise ValueError("veredito deve ser correta, parcial ou incorreta; referencia_valida, booleano.")


# ---------------------------------------------------------------- seleção
def cotas(total: int, itens: list[str], proporcao: dict = PROPORCAO) -> dict:
    """Divide o total por item e nível pelo método do maior resto."""
    celulas = [(i, n) for i in itens for n in proporcao]
    bruto = {(i, n): total * proporcao[n] / len(itens) for i, n in celulas}
    base = {c: int(v) for c, v in bruto.items()}
    resto = total - sum(base.values())
    for c in sorted(celulas, key=lambda c: (-(bruto[c] - base[c]), celulas.index(c)))[:resto]:
        base[c] += 1
    out = defaultdict(dict)
    for (i, n), v in base.items():
        out[i][n] = v
    return dict(out)


def selecionar_alvos(item: str, relacoes: list[dict], combinacoes: list[dict], cota: dict) -> tuple[list, dict]:
    """Espalha os alvos pelos blocos (rodízio) sem repetir relação; difícil B vem das combinações."""
    rng = _rng("alvos", item)
    por_bloco = defaultdict(list)
    for r in relacoes:
        por_bloco[r["bloco"]].append(r)
    ordem_blocos = sorted(por_bloco)
    rng.shuffle(ordem_blocos)
    fila = []
    for k in range(max((len(v) for v in por_bloco.values()), default=0)):
        fila += [por_bloco[b][k] for b in ordem_blocos if k < len(por_bloco[b])]
    usadas, alvos, faltas = set(), [], {}
    for nivel in ("dificil_A", "media", "facil"):   # os níveis mais escassos escolhem primeiro
        escolhidas = [r for r in fila if nivel in r["niveis"] and r["id"] not in usadas][: cota.get(nivel, 0)]
        usadas |= {r["id"] for r in escolhidas}
        alvos += [{"id": f"{item}:{nivel}:{r['id']}", "item": item, "tipo": nivel, "relacoes": [r]} for r in escolhidas]
        if len(escolhidas) < cota.get(nivel, 0):
            faltas[nivel] = cota[nivel] - len(escolhidas)
    combos = list(combinacoes)
    rng.shuffle(combos)
    escolhidos = combos[: cota.get("dificil_B", 0)]
    por_id = {r["id"]: r for r in relacoes}
    alvos += [{"id": f"{item}:dificil_B:{c['id']}", "item": item, "tipo": "dificil_B",
               "combinacao": c, "relacoes": [por_id[i] for i in c["relacoes"]]} for c in escolhidos]
    if len(escolhidos) < cota.get("dificil_B", 0):
        faltas["dificil_B"] = cota["dificil_B"] - len(escolhidos)
    return alvos, faltas


def nivel_agregado(tipo: str) -> str:
    return "dificil" if tipo.startswith("dificil") else tipo


def amostrar_ec(caminho: Path, cota_por_item: dict, seed: int = 20261023) -> tuple[list[dict], dict]:
    linhas = [json.loads(l) for l in caminho.read_text(encoding="utf-8").splitlines() if l.strip()]
    rng = random.Random(seed)
    out, faltas = [], {}
    for item, cota in cota_por_item.items():
        alvo = {"facil": cota.get("facil", 0), "media": cota.get("media", 0),
                "dificil": cota.get("dificil_A", 0) + cota.get("dificil_B", 0)}
        for nivel, n in alvo.items():
            pool = sorted((q for q in linhas if q["item"] == item and q["dificuldade"] == nivel), key=lambda q: q["uid"])
            escolha = rng.sample(pool, min(n, len(pool)))
            if len(escolha) < n:
                faltas[f"{item}:{nivel}"] = n - len(escolha)
            out += [{"id": f"ec:{q['uid']}", "metodo": "ec", "item": item, "tipo": nivel, "nivel": nivel,
                     "pergunta": q["pergunta"], "resposta": q["resposta"], "origem": q["uid"]} for q in escolha]
    return out, faltas


# ---------------------------------------------------------------- execução
class Piloto:
    def __init__(self, saida: Path, ec: Path, *, itens=ITENS, total: int = 100, modelos: dict | None = None,
                 combinacoes_por_doc: int = 15, workers: int = 6, clientes: dict | None = None,
                 sem_exemplos: bool = False, limpos: Path | None = None, limite_blocos: int | None = None,
                 progress=print):
        self.saida, self.ec, self.itens, self.total = Path(saida), Path(ec), list(itens), total
        self.modelos = {**MODELOS, **(modelos or {})}
        self.combinacoes_por_doc, self.workers = combinacoes_por_doc, workers
        self.clientes, self.sem_exemplos, self.limpos, self.progress = dict(clientes or {}), sem_exemplos, limpos, progress
        self.lock = threading.Lock()
        self.temas = {i: tema(i) for i in self.itens}
        self.docs = {}
        for i in self.itens:
            doc, bs = blocos(i)
            if doc["titulo"] != self.temas[i]["titulo"]:
                raise ValueError(f"{i}: documento não corresponde ao tópico do programa")
            self.docs[i] = bs[:limite_blocos] if limite_blocos else bs
        self.limite_blocos = limite_blocos

    # -- infraestrutura
    def cliente(self, papel: str):
        with self.lock:
            if papel not in self.clientes:
                from pipeline.inventario.llm import LLMClient, load_dotenv
                load_dotenv(ROOT)
                nome = self.modelos[papel]
                model, effort = nome.rsplit(":", 1) if ":" in nome else (nome, "")
                self.clientes[papel] = LLMClient(
                    model, effort, self.saida / ".local" / f"{papel}.sqlite3",
                    self.saida / "chamadas" / f"{papel}.jsonl", provider="azure", max_attempts=3, timeout=600,
                    max_tokens_cap=32000, max_calls=100000, response_dir=self.saida / ".local" / "respostas" / papel)
            return self.clientes[papel]

    def _paralelo(self, tarefas, funcao, rotulo: str):
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
                    {"erro": type(exc).__name__, "mensagem": str(exc)[:2000],
                     "em": datetime.now(timezone.utc).isoformat()})

    def _ok(self, pasta: str, nome: str) -> None:
        f = self.saida / "falhas" / pasta / f"{nome}.json"
        if f.exists():
            f.unlink()

    def config(self) -> None:
        cfg = {"schema": "piloto-inventario-v1", "itens": self.itens, "total": self.total, "modelos": self.modelos,
               "combinacoes_por_doc": self.combinacoes_por_doc, "ec": self.ec.as_posix(),
               "sem_exemplos": self.sem_exemplos, "proporcao": PROPORCAO, "limite_blocos": self.limite_blocos}
        path = self.saida / "config.json"
        if path.exists():
            antigo = {k: v for k, v in read_json(path).items() if k != "criado_em"}
            if antigo != cfg:
                diff = sorted(k for k in set(antigo) | set(cfg) if antigo.get(k) != cfg.get(k))
                raise ValueError(f"Configuração diferente da pasta existente ({', '.join(diff)}); use outra --saida")
            return
        atomic_json(path, {**cfg, "criado_em": datetime.now(timezone.utc).isoformat()})

    # -- 1. relações
    def relacoes(self) -> int:
        system = prompt("relacoes")
        tarefas = [(i, b) for i in self.itens for b in self.docs[i]
                   if not (self.saida / "relacoes" / i / f"{b['indice']:03d}.json").exists()]
        self.progress(f"1. relações: {len(tarefas)} blocos a processar", flush=True)

        def um(t):
            item, b = t
            t_ = self.temas[item]
            user = (f"<tema>\nÁrea: {t_['area']}\nTema: {t_['tema']}\n</tema>\n\n<documento>{t_['titulo']}</documento>\n\n"
                    f"<bloco>\n{b['titulo_capitulo']} / {b['subtitulo']}\n{b['texto']}\n</bloco>")
            try:
                d = self.cliente("relacoes").json(system, user, tag="inv_relacoes", max_tokens=8000, item=item,
                                                  validate=lambda d: validar_relacoes(d, b["texto"]))
            except Exception as exc:  # noqa: BLE001
                self._falha("relacoes", f"{item}_{b['indice']:03d}", exc)
                return False
            rels = [{**r, "id": f"B{b['indice']:03d}.R{k}", "bloco": b["indice"]} for k, r in enumerate(d["relacoes"], 1)]
            atomic_json(self.saida / "relacoes" / item / f"{b['indice']:03d}.json",
                        {"item": item, "bloco": b["indice"], "subtitulo": b["subtitulo"], "status": d["status"],
                         "motivo": d["motivo"], "relacoes": rels})
            self._ok("relacoes", f"{item}_{b['indice']:03d}")
            return True

        return self._paralelo(tarefas, um, "relações")

    def todas_relacoes(self, item: str) -> list[dict]:
        return [r for p in sorted((self.saida / "relacoes" / item).glob("*.json")) for r in read_json(p)["relacoes"]]

    # -- 2. combinações
    def combinacoes(self) -> int:
        falhas = 0
        for item in self.itens:
            destino = self.saida / "combinacoes" / f"{item}.json"
            if destino.exists():
                continue
            rels = self.todas_relacoes(item)
            if len(list((self.saida / "relacoes" / item).glob("*.json"))) < len(self.docs[item]):
                self.progress(f"2. combinações {item}: relações incompletas; rode de novo para concluir", flush=True)
                falhas += 1
                continue
            subt = {b["indice"]: b["subtitulo"] for b in self.docs[item]}
            linhas = [f"{r['id']} | bloco {r['bloco']:03d} ({subt[r['bloco']]}) | {r['afirmacao']} | condições: "
                      f"{'; '.join(r['condicoes']) or '-'} | limites: {'; '.join(r['limites']) or '-'}" for r in rels]
            t_ = self.temas[item]
            user = (f"<tema>\nÁrea: {t_['area']}\nTema: {t_['tema']}\n</tema>\n\n<documento>{t_['titulo']}</documento>\n\n"
                    "<relacoes>\n" + "\n".join(linhas) + "\n</relacoes>")
            bloco_da = {r["id"]: r["bloco"] for r in rels}
            self.progress(f"2. combinações {item}: {len(rels)} relações", flush=True)
            try:
                d = self.cliente("combinacoes").json(
                    prompt("combinacoes", QUANTIDADE=self.combinacoes_por_doc), user, tag="inv_combinacoes",
                    max_tokens=24000, item=item,
                    validate=lambda d: validar_combinacoes(d, bloco_da, self.combinacoes_por_doc))
            except Exception as exc:  # noqa: BLE001
                self._falha("combinacoes", item, exc)
                falhas += 1
                continue
            atomic_json(destino, {"item": item, "observacao": d["observacao"],
                                  "combinacoes": [{**c, "id": f"C{k}"} for k, c in enumerate(d["combinacoes"], 1)]})
            self._ok("combinacoes", item)
        return falhas

    # -- 3. alvos
    def alvos(self) -> list[dict]:
        destino = self.saida / "alvos.json"
        if destino.exists():
            return read_json(destino)["alvos"]
        c = cotas(self.total, self.itens)
        alvos, faltas = [], {}
        for item in self.itens:
            combos = read_json(self.saida / "combinacoes" / f"{item}.json")["combinacoes"]
            a, f = selecionar_alvos(item, self.todas_relacoes(item), combos, c[item])
            alvos += a
            faltas.update({f"{item}:{k}": v for k, v in f.items()})
        atomic_json(destino, {"cotas": c, "faltas": faltas, "alvos": alvos})
        if faltas:
            self.progress(f"3. alvos: faltaram {faltas} (o inventário não sustentou a cota)", flush=True)
        return alvos

    # -- 4. questões
    def _exemplos(self, alvo) -> str:
        if self.sem_exemplos:
            return ""
        from pipeline.qa_research.piloto_janela import exemplos as ex
        with self.lock:
            if not hasattr(self, "_pools"):
                self._pools = ex.carregar_limpos(self.limpos)[0]
                self._banco = ex.carregar_especialista()
        k = int(hashlib.sha256(alvo["id"].encode()).hexdigest()[:8], 16) % 100000
        return ex.render(ex.exemplos_da_janela("EC", alvo["item"], k, self._pools, self._banco))

    def questoes(self) -> int:
        alvos = self.alvos()
        system = prompt("questao")
        pendentes = [a for a in alvos if not (self.saida / "questoes" / f"{_nome(a['id'])}.json").exists()]
        self.progress(f"4. questões: {len(pendentes)} alvos a redigir", flush=True)

        def um(alvo):
            bs = {b["indice"]: b for b in self.docs[alvo["item"]]}
            usados = sorted({r["bloco"] for r in alvo["relacoes"]})
            blocos_txt = "\n\n".join(f"[bloco {i:03d}] {bs[i]['titulo_capitulo']} / {bs[i]['subtitulo']}\n{bs[i]['texto']}"
                                     for i in usados)
            conteudo = {"tipo": alvo["tipo"],
                        "relacoes": [{k: r[k] for k in ("id", "afirmacao", "condicoes", "limites")}
                                     | ({"explicacao_concorrente": r["explicacao_concorrente"],
                                         "condicao_que_distingue": r["condicao_que_distingue"]}
                                        if alvo["tipo"] == "dificil_A" else {}) for r in alvo["relacoes"]]}
            if alvo["tipo"] == "dificil_B":
                conteudo["combinacao"] = {k: alvo["combinacao"][k] for k in CAMPOS_COMB if k != "relacoes"}
            t_ = self.temas[alvo["item"]]
            user = "\n\n".join(x for x in (
                f"<tema>\nÁrea: {t_['area']}\nTema: {t_['tema']}\n</tema>",
                f"<alvo>\n{json.dumps(conteudo, ensure_ascii=False, indent=2)}\n</alvo>",
                self._exemplos(alvo),
                f"<blocos>\n{blocos_txt}\n</blocos>") if x)
            try:
                d = self.cliente("questao").json(system, user, tag="inv_questao", max_tokens=8000, item=alvo["item"],
                                                 validate=validar_questao)
            except Exception as exc:  # noqa: BLE001
                self._falha("questoes", _nome(alvo["id"]), exc)
                return False
            atomic_json(self.saida / "questoes" / f"{_nome(alvo['id'])}.json",
                        {"id": f"inv:{alvo['id']}", "metodo": "inventario", "item": alvo["item"], "tipo": alvo["tipo"],
                         "nivel": nivel_agregado(alvo["tipo"]), "status": d["status"], "motivo": d["motivo"],
                         "pergunta": d["pergunta"], "resposta": d["resposta"],
                         "relacoes": [r["id"] for r in alvo["relacoes"]],
                         "combinacao": alvo.get("combinacao", {}).get("id")})
            self._ok("questoes", _nome(alvo["id"]))
            return True

        return self._paralelo(pendentes, um, "questões")

    # -- 5. amostra EC
    def amostra_ec(self) -> list[dict]:
        destino = self.saida / "amostra_ec.json"
        if destino.exists():
            return read_json(destino)["questoes"]
        qs, faltas = amostrar_ec(self.ec, cotas(self.total, self.itens))
        atomic_json(destino, {"origem": self.ec.as_posix(), "faltas": faltas, "questoes": qs})
        return qs

    def banco_avaliado(self) -> list[dict]:
        inv = [read_json(p) for p in sorted((self.saida / "questoes").glob("*.json"))]
        return [q for q in inv if q["status"] == "ok"] + self.amostra_ec()

    # -- 6. avaliação cega
    def avaliar(self, lote_juiz: int = 10) -> int:
        banco = self.banco_avaliado()
        sys_r, sys_j = prompt("respondente"), prompt("juiz")
        pend = [q for q in banco if not (self.saida / "avaliacao" / "respostas" / f"{_nome(q['id'])}.json").exists()]
        self.progress(f"6a. respondente ({self.modelos['respondente']}): {len(pend)} perguntas", flush=True)

        def responder(q):
            try:
                d = self.cliente("respondente").json(sys_r, q["pergunta"], tag="inv_respondente", max_tokens=1500,
                                                     item=q["item"], validate=validar_resposta)
            except Exception as exc:  # noqa: BLE001
                self._falha("respostas", _nome(q["id"]), exc)
                return False
            atomic_json(self.saida / "avaliacao" / "respostas" / f"{_nome(q['id'])}.json",
                        {"id": q["id"], "resposta_candidato": d["resposta"]})
            self._ok("respostas", _nome(q["id"]))
            return True

        falhas = self._paralelo(pend, responder, "respostas")
        respondidas = [q for q in banco if (self.saida / "avaliacao" / "respostas" / f"{_nome(q['id'])}.json").exists()]
        ordem = sorted(respondidas, key=lambda q: hashlib.sha256(("juiz" + q["id"]).encode()).hexdigest())
        lotes = [ordem[i:i + lote_juiz] for i in range(0, len(ordem), lote_juiz)]
        julgados = {q["id"] for p in (self.saida / "avaliacao" / "juiz").glob("*.json") for q in read_json(p)["avaliacoes"]}
        lotes = [l for l in lotes if not {q["id"] for q in l} <= julgados]
        self.progress(f"6b. juiz ({self.modelos['juiz']}): {len(lotes)} lotes", flush=True)

        def julgar(lote):
            ids = [f"Q{k}" for k in range(1, len(lote) + 1)]   # o juiz não vê o método nem o nível
            itens = [{"id": i, "pergunta": q["pergunta"], "resposta_referencia": q["resposta"],
                      "resposta_candidato": read_json(self.saida / "avaliacao" / "respostas" /
                                                      f"{_nome(q['id'])}.json")["resposta_candidato"]}
                     for i, q in zip(ids, lote)]
            nome = hashlib.sha256("|".join(q["id"] for q in lote).encode()).hexdigest()[:16]
            try:
                d = self.cliente("juiz").json(sys_j, json.dumps(itens, ensure_ascii=False), tag="inv_juiz",
                                              max_tokens=8000, validate=lambda d: validar_juiz(d, ids))
            except Exception as exc:  # noqa: BLE001
                self._falha("juiz", nome, exc)
                return False
            atomic_json(self.saida / "avaliacao" / "juiz" / f"{nome}.json",
                        {"avaliacoes": [{**a, "id": q["id"]} for a, q in zip(d["avaliacoes"], lote)]})
            self._ok("juiz", nome)
            return True

        return falhas + self._paralelo(lotes, julgar, "juiz")

    # -- 7. relatório
    def relatorio(self) -> dict:
        banco = {q["id"]: q for q in self.banco_avaliado()}
        resp = {read_json(p)["id"]: read_json(p)["resposta_candidato"]
                for p in (self.saida / "avaliacao" / "respostas").glob("*.json")}
        juiz = {a["id"]: a for p in (self.saida / "avaliacao" / "juiz").glob("*.json") for a in read_json(p)["avaliacoes"]}
        linhas = [{**q, "resposta_candidato": resp.get(i, ""), **{k: juiz[i][k] for k in ("veredito", "referencia_valida",
                  "justificativa") if i in juiz}} for i, q in banco.items()]
        avaliadas = [l for l in linhas if "veredito" in l]

        def bloco(ls):
            n = len(ls)
            validas = [l for l in ls if l["referencia_valida"]]
            return {"n": n, "acuracia": round(sum(VEREDITOS[l["veredito"]] for l in ls) / n, 3) if n else None,
                    "corretas": sum(l["veredito"] == "correta" for l in ls),
                    "parciais": sum(l["veredito"] == "parcial" for l in ls),
                    "incorretas": sum(l["veredito"] == "incorreta" for l in ls),
                    "referencia_invalida": n - len(validas),
                    "acuracia_ref_valida": round(sum(VEREDITOS[l["veredito"]] for l in validas) / len(validas), 3)
                    if validas else None,
                    "palavras_pergunta": round(sum(palavras(l["pergunta"]) for l in ls) / n, 1) if n else None}

        res = {"modelos": self.modelos, "metodos": {}}
        for m in ("inventario", "ec"):
            lm = [l for l in avaliadas if l["metodo"] == m]
            res["metodos"][m] = {"total": bloco(lm), "por_nivel": {n: bloco([l for l in lm if l["nivel"] == n])
                                                                   for n in ("facil", "media", "dificil")}}
            if m == "inventario":
                res["metodos"][m]["por_tipo"] = {t: bloco([l for l in lm if l["tipo"] == t])
                                                 for t in ("dificil_A", "dificil_B")}
        geradas = [read_json(p) for p in (self.saida / "questoes").glob("*.json")]
        res["inventario_geracao"] = {"alvos": len(read_json(self.saida / "alvos.json")["alvos"])
                                     if (self.saida / "alvos.json").exists() else 0,
                                     "ok": sum(q["status"] == "ok" for q in geradas),
                                     "insuficiente": sum(q["status"] == "insuficiente" for q in geradas),
                                     "faltas_de_cota": read_json(self.saida / "alvos.json").get("faltas", {})
                                     if (self.saida / "alvos.json").exists() else {}}
        res["relacoes"] = {i: len(self.todas_relacoes(i)) for i in self.itens}
        res["combinacoes"] = {i: len(read_json(self.saida / "combinacoes" / f"{i}.json")["combinacoes"])
                              for i in self.itens if (self.saida / "combinacoes" / f"{i}.json").exists()}
        res["falhas_pendentes"] = sorted(p.relative_to(self.saida).as_posix() for p in (self.saida / "falhas").rglob("*.json"))
        atomic_json(self.saida / "resultado.json", res)

        campos = ["id", "metodo", "item", "tipo", "nivel", "pergunta", "resposta", "resposta_candidato", "veredito",
                  "referencia_valida", "justificativa"]
        with (self.saida / "questoes_avaliadas.csv").open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
            w.writeheader()
            for l in sorted(linhas, key=lambda l: (l["metodo"], l["nivel"], l["id"])):
                w.writerow({k: l.get(k, "") for k in campos})
        self._markdown(res, avaliadas)
        return res

    def _markdown(self, res: dict, avaliadas: list[dict]) -> None:
        def fmt(b):
            if not b or not b["n"]:
                return "–"
            return (f"{b['acuracia']:.2f} (n={b['n']}; ✓{b['corretas']} ~{b['parciais']} ✗{b['incorretas']}; "
                    f"ref. inválida {b['referencia_invalida']})")

        inv, ec = res["metodos"]["inventario"], res["metodos"]["ec"]
        l = ["# Piloto: inventário (estilo qa_v7) x configuração EC", "",
             f"Respondente sem contexto: `{res['modelos']['respondente']}`. Juiz: `{res['modelos']['juiz']}`. "
             "Acurácia: correta = 1, parcial = 0,5. Quanto mais difícil a questão, menor deve ser a acurácia.", "",
             "| Nível | Inventário | EC |", "|---|---|---|"]
        for n in ("facil", "media", "dificil"):
            l.append(f"| {n} | {fmt(inv['por_nivel'][n])} | {fmt(ec['por_nivel'][n])} |")
        l += [f"| **total** | {fmt(inv['total'])} | {fmt(ec['total'])} |", "",
              "Inventário por tipo de difícil: " + "; ".join(f"{t}: {fmt(b)}" for t, b in inv["por_tipo"].items()) + ".", "",
              "Acurácia só nas referências válidas (sem as marcadas pelo juiz como ambíguas ou erradas): "
              + "; ".join(f"{m} {n}: {res['metodos'][m]['por_nivel'][n]['acuracia_ref_valida']}"
                          for m in ("inventario", "ec") for n in ("facil", "media", "dificil")) + ".", "",
              f"Inventário: relações {res['relacoes']}, combinações {res['combinacoes']}, "
              f"geração {res['inventario_geracao']}.",
              f"Falhas pendentes: {len(res['falhas_pendentes'])}.", "", "## Questões avaliadas", ""]
        for a in sorted(avaliadas, key=lambda a: (a["metodo"], a["nivel"], a["id"])):
            l += [f"**{a['metodo']} · {a['tipo']} · {a['veredito']}{'' if a['referencia_valida'] else ' · ref. inválida'}** "
                  f"{a['pergunta']}", "", f"- Referência: {a['resposta']}", f"- Respondente: {a['resposta_candidato']}",
                  f"- Juiz: {a.get('justificativa', '')}", ""]
        (self.saida / "RELATORIO.md").write_text("\n".join(l), encoding="utf-8")

    def run(self, etapas=("relacoes", "combinacoes", "questoes", "avaliar", "relatorio")) -> int:
        self.config()
        falhas = 0
        if "relacoes" in etapas:
            falhas += self.relacoes()
        if "combinacoes" in etapas:
            falhas += self.combinacoes()
        if "questoes" in etapas:
            if all((self.saida / "combinacoes" / f"{i}.json").exists() for i in self.itens):
                falhas += self.questoes()
            else:
                self.progress("4. questões: aguardando relações e combinações completas", flush=True)
                falhas += 1
        if "avaliar" in etapas:
            falhas += self.avaliar()
        if "relatorio" in etapas:
            self.relatorio()
        return falhas


def _nome(i: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", i)


def ec_mais_recente() -> Path | None:
    cands = sorted((QA / "relatorios").glob("experimento_externos_*/EC/questoes.jsonl"))
    return cands[-1] if cands else None
