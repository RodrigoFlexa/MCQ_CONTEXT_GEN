"""Ablação v3: escada cumulativa de módulos da geração, sem poda (relatorios/ablacao_geracao_v3).

Cada configuração soma um módulo à anterior. A última é a geração definitiva (regras + documentos + exemplos externos +
retroalimentação), com o mesmo prompt montado por blocos (prompts/abl3_gerador.md, abl3_naive.md):

  naive       pedido simples ("elabore até quatro questões") + tema e escopo do especialista; nenhuma regra;
  regras      + prompt completo: critérios (unicidade, granularidade, autocontenção, verificabilidade), tipos, forma;
  documentos  + janela de 3 blocos com o bloco foco e as regras que dependem do texto;
  externos    + 8 exemplos de forma sorteados por chamada (6 de datasets externos e 2 convertidas do dataset de
              múltipla escolha, de outros documentos);
  retro       + retroalimentação: semente fixa de boas e ruins no prompt de sistema, boas e ruins sorteadas de tudo o que
              a própria configuração já gerou e o auditor julgou (de outros documentos), conhecimentos já aprovados no
              documento e as questões já propostas para o foco. Nenhuma questão é refeita: só o prompt seguinte muda.

Mesma unidade do pipeline em todas: FOCOS_POR_TOPICO blocos foco por documento, VISITAS visitas por foco, de 0 a
POR_CHAMADA questões por chamada, em ondas (visita 1 dos focos pares, visita 1 dos ímpares, visita 2...). Nas
configurações sem documento a chamada é só sobre o tópico, com o mesmo número de chamadas por tópico. Toda questão
gerada conta.

Avaliação (métrica, não filtro), igual para todas:
  auditor v23 (com a janela; sem documento, os K_BUSCA blocos mais relevantes do corpus inteiro, busca híbrida
  TF-IDF + embeddings) -> válida intrínseca (sem a verificação de fonte) e aprovada;
  resposta de até TETO_RESPOSTA palavras; sustentação total (faithfulness) das aprovadas -> válida;
  quase-duplicatas (deduplicação calibrada, só medida); diversidade em amostras do mesmo tamanho; custo;
  dificuldade: amostra de AMOSTRA_DIFICULDADE questões por configuração (válidas e inválidas), respondidas sem e com
  contexto pelos modelos independentes do painel e julgadas pelo juiz padrão.

python -m pipeline.qa_research.experimento_ab ablacao-v3 [--etapas geracao,sustentacao,dedup,dificuldade,relatorio]
"""
from __future__ import annotations

import csv
import json
import math
import random
import re
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.benchmark_gap import resumo_faithfulness, validar_faithfulness
from pipeline.qa_research.geracao_tipos.rodadas import _filtrado, _nome_arq
from pipeline.qa_research.piloto_janela.core import DOCS, blocos, janela, tema

from . import comum as C
from .ablacao import conteudo, vocabulario
from .dedup import DedupIncremental, carregar_calibracao
from .v22 import TIPOS, validar_auditoria, validar_saida, veredito
from .v23 import carregar_exemplos, selecionar_exemplos
from .variada import CONVERTIDAS, bloco_forma, carregar_convertidas, carregar_externos

SAIDA = C.QA / "relatorios" / "ablacao_geracao_v3"
CONFIGS = {
    "naive": {"regras": False, "documento": False, "externos": False, "retro": False},
    "regras": {"regras": True, "documento": False, "externos": False, "retro": False},
    "documentos": {"regras": True, "documento": True, "externos": False, "retro": False},
    "externos": {"regras": True, "documento": True, "externos": True, "retro": False},
    "retro": {"regras": True, "documento": True, "externos": True, "retro": True},
}
NOME = {"naive": "Naive", "regras": "+ Regras", "documentos": "+ Documentos", "externos": "+ Datasets externos",
        "retro": "+ Retroalimentação"}
FOCOS_POR_TOPICO = 8
VISITAS = 3
ONDAS_POR_VISITA = 2
POR_CHAMADA = 4
MISTURA_EXTERNOS = {"pira_ptbr": 2, "mmmlu_ptbr": 2, "arc_challenge": 1, "qasc": 1}
N_CONVERTIDAS = 2
FIXAS = (4, 4)            # boas e ruins da semente sempre no prompt de sistema (retro)
SORTEIO = (10, 8)         # boas e ruins sorteadas por chamada do conjunto já julgado (retro)
K_BUSCA = 5
TETO_RESPOSTA = 20
AMOSTRA_DIFICULDADE = 500
GERADOR = "gpt-5-4-petrobras:high"
AUDITOR = "gpt-5-4-petrobras:high"
PAINEL = {"gpt-4-1-mini": "gpt-4-1-mini-petrobras", "gpt-4-1": "gpt-4-1-petrobras",
          "gpt-5-mini": "gpt-5-mini-petrobras:low", "gpt-5": "gpt-5-petrobras:low"}   # independentes do gerador
CHAVES_NAIVE = {"pergunta", "resposta"}
CHAVES_REGRAS = {"tipo", "cenario", "conhecimento", "pergunta", "resposta", "explicacao", "resposta_padrao",
                 "por_que_nao"}
ETAPAS = ("geracao", "sustentacao", "dedup", "dificuldade", "relatorio")
SEMENTE = 20261109


def _rng(*p) -> random.Random:
    return random.Random(C.sha("|".join(map(str, p)))[:16])


# ------------------------------------------------------------------ prompts
def sistema_base(cfg: dict) -> str:
    """Prompt de sistema da configuração (sem a semente fixa da retroalimentação)."""
    if not cfg["regras"]:
        return C.prompt("abl3_naive")
    t = C.prompt("abl3_gerador")
    flags = {"DOC": cfg["documento"], "SEMDOC": not cfg["documento"], "EXT": cfg["externos"], "RETRO": cfg["retro"]}
    for k, v in flags.items():
        t = re.sub(r"\{\{%s\}\}(.*?)\{\{/%s\}\}" % (k, k), (lambda m: m.group(1)) if v else "", t, flags=re.S)
    if "{{" in t:
        raise ValueError("marcador não resolvido em abl3_gerador.md")
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def _boa(e: dict) -> str:
    return (f"[{e.get('tipo', '?')}] Pergunta: {e['pergunta']}\nResposta: {e['resposta']}\n"
            f"Resposta padrão (errada aqui): {e.get('resposta_padrao', '-')}\nPor que não: {e.get('por_que_nao', '-')}")


def _ruim(e: dict) -> str:
    return f"[{e.get('tipo', '?')}] Pergunta: {e['pergunta']}\nResposta: {e['resposta']}\nDefeito: {e['defeito']}"


def bloco_fixas(boas: list, ruins: list) -> str:
    return ("<questoes_boas>\n" + "\n\n".join(_boa(e) for e in boas) + "\n</questoes_boas>\n\n<questoes_ruins>\n"
            + "\n\n".join(_ruim(e) for e in ruins) + "\n</questoes_ruins>")


def validar_geracao(d: dict, chaves: set) -> None:
    validar_saida(d, POR_CHAMADA)
    for q in d["questoes"]:
        if not isinstance(q, dict) or not isinstance(q.get("pergunta"), str) or not isinstance(q.get("resposta"), str) \
                or not q["pergunta"].strip() or not q["resposta"].strip():
            raise ValueError("Cada questão é um objeto com pergunta e resposta preenchidas.")


def formato_ok(q: dict, cfg: dict) -> bool:
    chaves = CHAVES_NAIVE if not cfg["regras"] else CHAVES_REGRAS | ({"fundamentos"} if cfg["documento"] else set())
    return set(q) >= chaves and (not cfg["regras"] or q.get("tipo") in TIPOS)


# ------------------------------------------------------------------ busca no corpus (configurações sem documento)
class Busca:
    """Os k blocos mais relevantes do corpus inteiro: fusão de postos (RRF) entre TF-IDF e embeddings."""

    def __init__(self, todos: dict, embedder):
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.blocos = [{**b, "item": i} for i, bs in sorted(todos.items()) for b in bs]
        txt = [f"{b['subtitulo']} {b['texto']}" for b in self.blocos]
        self.vec = TfidfVectorizer(sublinear_tf=True).fit(txt)
        self.M = self.vec.transform(txt)
        self.embedder, self._E, self._trava = embedder, None, threading.Lock()
        self._txt = [t[:8000] for t in txt]

    def _emb(self):
        with self._trava:
            if self._E is None:
                E = np.asarray(self.embedder.encode(self._txt), dtype=float)
                self._E = E / np.clip(np.linalg.norm(E, axis=1, keepdims=True), 1e-12, None)
            return self._E

    def buscar(self, texto: str, k: int = K_BUSCA) -> list[dict]:
        s1 = (self.M @ self.vec.transform([texto]).T).toarray().ravel()
        q = np.asarray(self.embedder.encode([texto[:8000]]), dtype=float).ravel()
        s2 = self._emb() @ (q / max(np.linalg.norm(q), 1e-12))
        r1 = np.empty(len(s1), int)
        r1[np.argsort(-s1, kind="stable")] = np.arange(len(s1))
        r2 = np.empty(len(s2), int)
        r2[np.argsort(-s2, kind="stable")] = np.arange(len(s2))
        rrf = 1 / (60 + r1) + 1 / (60 + r2)
        return [self.blocos[i] for i in np.argsort(-rrf, kind="stable")[:k]]


# ------------------------------------------------------------------ estudo
class AblacaoV3:
    def __init__(self, saida: Path = SAIDA, *, exp: Path = C.EXPERIMENTO, docs: Path = DOCS, configs=None,
                 itens=None, focos_por_topico: int = FOCOS_POR_TOPICO, visitas: int = VISITAS,
                 externos: Path | None = None, convertidas: Path = CONVERTIDAS, workers: int = 8,
                 clientes: dict | None = None, embedder=None, progress=print):
        self.saida, self.docs_dir = Path(saida), Path(docs)
        self.workers, self.progress = max(1, int(workers)), progress
        self.configs = list(configs or CONFIGS)
        if any(c not in CONFIGS for c in self.configs):
            raise ValueError(f"configurações válidas: {', '.join(CONFIGS)}")
        cal_arq = Path(exp) / "calibracao" / "calibracao.json"
        if not cal_arq.exists():
            raise ValueError(f"Falta a calibração da deduplicação ({C.relativo(cal_arq)})")
        self.cal = carregar_calibracao(cal_arq)
        self.media = np.asarray(read_json(cal_arq.parent / self.cal["media"]), dtype=float)
        self.pools, self.arq_externos = carregar_externos(externos)
        self.arq_convertidas = Path(convertidas)
        self.convertidas = carregar_convertidas(self.arq_convertidas)
        self.semente = carregar_exemplos()
        self._clientes, self._embedder = dict(clientes or {}), embedder
        self._trava = threading.Lock()
        disponiveis = sorted(p.name for p in self.docs_dir.iterdir() if (p / "documento.json").exists())
        self.itens = sorted(itens) if itens else disponiveis
        self.todos = {i: blocos(i, self.docs_dir)[1] for i in disponiveis}
        self.docs = {i: self.todos[i] for i in self.itens}
        self.temas = {i: tema(i) for i in self.itens}
        self.n_focos, self.visitas = int(focos_por_topico), int(visitas)
        self.unidades = self._unidades()
        self._busca = None
        self.saida.mkdir(parents=True, exist_ok=True)
        self._config()

    def _unidades(self) -> list[dict]:
        """(documento, foco, visita, onda): focos espaçados no documento; a onda alterna a metade dos focos."""
        out = []
        for i in self.itens:
            n = len(self.docs[i])
            k = min(self.n_focos, n)
            focos = sorted({min(n - 1, int((j + 0.5) * n / k)) for j in range(k)})
            for v in range(1, self.visitas + 1):
                for pos, f in enumerate(focos):
                    out.append({"item": i, "foco": f, "visita": v, "onda": (v - 1) * ONDAS_POR_VISITA + pos % ONDAS_POR_VISITA,
                                "id": f"{i}:{f:03d}:v{v}"})
        return out

    def _config(self) -> None:
        cfg = {"schema": "ablacao-geracao-v3", "configs": CONFIGS, "itens": self.itens, "focos_por_topico": self.n_focos,
               "visitas": self.visitas, "ondas_por_visita": ONDAS_POR_VISITA, "por_chamada": POR_CHAMADA,
               "mistura_externos": MISTURA_EXTERNOS, "n_convertidas": N_CONVERTIDAS, "fixas": FIXAS, "sorteio": SORTEIO,
               "k_busca": K_BUSCA, "teto_resposta": TETO_RESPOSTA, "gerador": GERADOR, "auditor": AUDITOR,
               "sustentacao": C.SUSTENTACAO, "painel": PAINEL, "amostra_dificuldade": AMOSTRA_DIFICULDADE,
               "dedup": {k: self.cal[k] for k in ("embedding", "limiar_auto", "limiar_juiz", "juiz")},
               "prompts_sha256": {p: C.sha(C.prompt(p)) for p in ("abl3_naive", "abl3_gerador", "auditoria_v23")},
               "semente_sha256": C.sha(json.dumps(self.semente, sort_keys=True, ensure_ascii=False)),
               "externos_sha256": C.sha(self.arq_externos.read_text(encoding="utf-8")),
               "convertidas_sha256": C.sha(self.arq_convertidas.read_text(encoding="utf-8")),
               "docs_sha256": {i: C.sha(read_json(self.docs_dir / i / "documento.json")) for i in sorted(self.todos)}}
        arq = self.saida / "config.json"
        if arq.exists():
            antigo = {k: v for k, v in read_json(arq).items() if k != "criado_em"}
            if json.loads(json.dumps(antigo)) != json.loads(json.dumps(cfg)):
                diff = sorted(k for k in set(antigo) | set(cfg)
                              if json.dumps(antigo.get(k), sort_keys=True) != json.dumps(cfg.get(k), sort_keys=True))
                raise ValueError(f"Configuração diferente da pasta existente ({', '.join(diff)}); use outra saída")
            return
        atomic_json(arq, {**cfg, "criado_em": datetime.now(timezone.utc).isoformat()})

    # -------------------------------------------------------------- infraestrutura
    def cliente(self, papel: str):
        with self._trava:
            if papel not in self._clientes:
                modelo = {"geracao": GERADOR, "auditoria": AUDITOR, "sustentacao": C.SUSTENTACAO,
                          "dedup_juiz": self.cal["juiz"]}[papel]
                self._clientes[papel] = C.cliente_llm(modelo, self.saida, papel)
            return self._clientes[papel]

    @property
    def embedder(self):
        with self._trava:
            if self._embedder is None:
                self._embedder = C.embedder(self.cal["embedding"], self.saida)
            return self._embedder

    @property
    def busca(self) -> Busca:
        with self._trava:
            if self._busca is None:
                self._busca = Busca(self.todos, self._embedder_sem_trava())
            return self._busca

    def _embedder_sem_trava(self):
        if self._embedder is None:
            self._embedder = C.embedder(self.cal["embedding"], self.saida)
        return self._embedder

    def _falha(self, nome: str, exc: Exception) -> None:
        atomic_json(self.saida / "falhas" / f"{nome}.json",
                    {"erro": type(exc).__name__, "mensagem": str(exc)[:2000], "em": datetime.now(timezone.utc).isoformat()})

    def _ok(self, nome: str) -> None:
        (self.saida / "falhas" / f"{nome}.json").unlink(missing_ok=True)

    def _paralelo(self, tarefas: list, funcao, rotulo: str) -> int:
        if not tarefas:
            return 0
        falhas = 0
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            for k, ok in enumerate(pool.map(funcao, tarefas), 1):
                falhas += 0 if ok else 1
                if k % 100 == 0 or k == len(tarefas):
                    self.progress(f"[ablação v3] {rotulo}: {k}/{len(tarefas)} ({falhas} falhas)", flush=True)
        return falhas

    def _tema(self, item: str) -> str:
        t = self.temas[item]
        return (f"<tema>\nÁrea: {t['area']}\nTema: {t['tema']}\n</tema>\n\n"
                f"<escopo_orientador>\n{t['escopo']}\n</escopo_orientador>")

    # -------------------------------------------------------------- arquivos
    def _arq_ger(self, c: str, u: dict) -> Path:
        return self.saida / c / "geracao" / f"{u['item']}_{u['foco']:03d}_v{u['visita']}.json"

    def _arq_aud(self, c: str, uid: str) -> Path:
        return self.saida / c / "auditoria" / f"{_nome_arq(uid)}.json"

    def _arq_sust(self, uid: str) -> Path:
        return self.saida / "sustentacao" / f"{_nome_arq(uid)}.json"

    def _janela(self, u: dict):
        jan = janela(self.docs[u["item"]], u["foco"])
        txt = "\n\n".join(f"[{r}] {b['titulo_capitulo']} / {b['subtitulo']}\n{b['texto']}" for r, b in jan)
        return jan, txt

    def _contexto(self, c: str, u: dict, q: dict) -> list[dict]:
        """Blocos com que a questão é auditada e sustentada: a janela da geração ou, sem documento, a busca no corpus."""
        if CONFIGS[c]["documento"]:
            jan, _ = self._janela(u)
            return [{"id": r, "item": u["item"], "texto": b["texto"], "titulo": f"{b['titulo_capitulo']} / {b['subtitulo']}",
                     "indice_documento": b["indice"]} for r, b in jan]
        sel = self.busca.buscar(f"{q['pergunta']} {q['resposta']}")
        return [{"id": f"B{k}", "item": b["item"], "texto": b["texto"], "titulo": f"{b['titulo_capitulo']} / {b['subtitulo']}",
                 "indice_documento": b["indice"]} for k, b in enumerate(sel, 1)]

    @staticmethod
    def _blocos_txt(ctx: list[dict]) -> str:
        return "\n\n".join(f"[{b['id']}] {b['titulo']}\n{b['texto']}" for b in ctx)

    # -------------------------------------------------------------- estado julgado (retroalimentação)
    def _questoes_unidade(self, c: str, u: dict) -> list[dict]:
        arq = self._arq_ger(c, u)
        if not arq.exists():
            return []
        d = read_json(arq)
        out = []
        for k, q in enumerate(d["questoes"], 1):
            uid = f"{c}:{u['id']}:{k}"
            aud = self._arq_aud(c, uid)
            out.append({**q, "uid": uid, "k": k, "auditoria": read_json(aud) if aud.exists() else None})
        return out

    @staticmethod
    def _julgamento(q: dict) -> tuple[bool | None, str]:
        a = q.get("auditoria")
        if not a:
            return None, ""
        if len(str(q["resposta"]).split()) > TETO_RESPOSTA:
            return False, f"resposta longa demais ({len(str(q['resposta']).split())} palavras)"
        if a["aprovada"]:
            return True, ""
        extra = f" Resposta alternativa apontada: {a['resposta_alternativa']}" if "varias_respostas" in a["falhas"] else ""
        return False, f"{a['motivo']}: {a['justificativa']}{extra}"

    def _julgadas(self, c: str, ate_onda: int) -> list[dict]:
        out = []
        for u in self.unidades:
            if u["onda"] < ate_onda:
                for q in self._questoes_unidade(c, u):
                    ok, motivo = self._julgamento(q)
                    if ok is not None:
                        out.append({**q, "item": u["item"], "foco": u["foco"], "visita": u["visita"], "boa": ok,
                                    "defeito": motivo})
        return out

    def _semente(self, item: str) -> tuple[list, list, list, list]:
        boas, ruins = selecionar_exemplos(self.semente, item)
        resto_b = boas[FIXAS[0]:] + [r for r in self.semente["reservas"]
                                     if r["item"] != item and r["id"] not in {e["id"] for e in boas}]
        return boas[:FIXAS[0]], ruins[:FIXAS[1]], resto_b, ruins[FIXAS[1]:]

    def sistema(self, c: str, item: str) -> str:
        s = sistema_base(CONFIGS[c])
        if CONFIGS[c]["retro"]:
            fb, fr, _, _ = self._semente(item)
            s += "\n\n" + bloco_fixas(fb, fr)
        return s

    def _retro(self, c: str, u: dict, julgadas: list[dict]) -> list[str]:
        doc = [q for q in julgadas if q["item"] == u["item"]]
        cob = "\n".join(f"- {q.get('conhecimento') or q['pergunta']} (resposta: {q['resposta']})" for q in doc if q["boa"])
        foco = [q for q in doc if q["foco"] == u["foco"] and q["visita"] < u["visita"]]
        hist = "\n".join(f"- [{'aprovada' if q['boa'] else 'reprovada (' + q['defeito'] + ')'}] {q['pergunta']} → "
                         f"{q['resposta']}" for q in foco)
        _, _, sb, sr = self._semente(u["item"])
        outras = [q for q in julgadas if q["item"] != u["item"]]
        pool_b = sb + [q for q in outras if q["boa"]]
        pool_r = sr + [q for q in outras if not q["boa"]]
        rng = _rng("retro", c, u["id"])
        boas = rng.sample(pool_b, min(SORTEIO[0], len(pool_b)))
        ruins = rng.sample(pool_r, min(SORTEIO[1], len(pool_r)))
        return [f"<conhecimentos_cobertos>\n{cob or 'Nenhum ainda.'}\n</conhecimentos_cobertos>",
                f"<questoes_deste_foco>\n{hist or 'Nenhuma.'}\n</questoes_deste_foco>",
                "<boas_ja_avaliadas>\n" + ("\n\n".join(_boa(e) for e in boas) or "Nenhuma ainda.") + "\n</boas_ja_avaliadas>",
                "<ruins_ja_avaliadas>\n" + ("\n\n".join(_ruim(e) for e in ruins) or "Nenhuma ainda.") + "\n</ruins_ja_avaliadas>"]

    def _forma(self, u: dict) -> str:
        rng = _rng("forma", u["id"])
        ex = []
        for fonte, n in MISTURA_EXTERNOS.items():
            pool = self.pools.get(fonte) or [r for v in self.pools.values() for r in v]
            ex += rng.sample(pool, min(n, len(pool)))
        outras = [q for q in self.convertidas if q.get("item") != u["item"]] or self.convertidas
        ex += rng.sample(outras, min(N_CONVERTIDAS, len(outras)))
        rng.shuffle(ex)
        return bloco_forma(ex)

    def usuario(self, c: str, u: dict, julgadas: list[dict] | None = None) -> str:
        cfg = CONFIGS[c]
        partes = [self._tema(u["item"])]
        if cfg["retro"]:
            partes += self._retro(c, u, julgadas if julgadas is not None else self._julgadas(c, u["onda"]))
        if cfg["externos"]:
            partes.append(self._forma(u))
        if cfg["documento"]:
            partes.append(f"<janela>\n{self._janela(u)[1]}\n</janela>")
        partes.append(f"Pedido: {u['id']}")      # cada chamada é independente (o cache do cliente é por conteúdo)
        return "\n\n".join(partes)

    # -------------------------------------------------------------- geração e auditoria
    def _gerar(self, c: str, u: dict, julgadas: list[dict] | None) -> bool:
        arq, nome = self._arq_ger(c, u), f"geracao_{c}_{u['item']}_{u['foco']:03d}_v{u['visita']}"
        if arq.exists():
            return True
        cfg = CONFIGS[c]
        chaves = CHAVES_REGRAS if cfg["regras"] else CHAVES_NAIVE
        try:
            d = self.cliente("geracao").json(self.sistema(c, u["item"]), self.usuario(c, u, julgadas), tag=f"abl3_{c}",
                                             max_tokens=16000, item=u["item"], validate=lambda d: validar_geracao(d, chaves))
        except Exception as exc:  # noqa: BLE001
            if not _filtrado(exc):
                self._falha(nome, exc)
                return False
            d = {"questoes": [], "motivo": "bloqueado pelo filtro de conteúdo"}
        atomic_json(arq, {**u, "config": c, "motivo": d["motivo"], "questoes": d["questoes"]})
        self._ok(nome)
        return True

    def _auditar(self, c: str, u: dict, q: dict) -> bool:
        arq = self._arq_aud(c, q["uid"])
        if arq.exists():
            return True
        nome = f"auditoria_{_nome_arq(q['uid'])}"
        ctx = self._contexto(c, u, q)
        tipo = q.get("tipo") if CONFIGS[c]["regras"] and q.get("tipo") in TIPOS else "nao_declarado"
        user = json.dumps({"tipo_declarado": tipo, "pergunta": q["pergunta"], "resposta_referencia": q["resposta"],
                           "explicacao_do_autor": q.get("explicacao") or "(não informada)",
                           "blocos": self._blocos_txt(ctx)}, ensure_ascii=False)
        try:
            d = self.cliente("auditoria").json(C.prompt("auditoria_v23"), user, tag="abl3_auditoria", max_tokens=6000,
                                               item=u["item"], validate=validar_auditoria)
            rec = veredito(d, tipo)
        except Exception as exc:  # noqa: BLE001
            if not _filtrado(exc):
                self._falha(nome, exc)
                return False
            rec = {"aprovada": False, "motivo": "bloqueio", "falhas": ["bloqueio"], "tipo_sugerido": tipo,
                   "justificativa": "bloqueada pelo filtro de conteúdo", "resposta_alternativa": "-"}
        atomic_json(arq, {**rec, "contexto": ctx})
        self._ok(nome)
        return True

    def gerar(self) -> int:
        falhas = 0
        for w in range(self.visitas * ONDAS_POR_VISITA):
            us = [u for u in self.unidades if u["onda"] == w]
            julg = {c: self._julgadas(c, w) for c in self.configs if CONFIGS[c]["retro"]}
            falhas += self._paralelo([(c, u) for c in self.configs for u in us if not self._arq_ger(c, u).exists()],
                                     lambda x: self._gerar(x[0], x[1], julg.get(x[0])), f"onda {w + 1}: geração")
            tarefas = [(c, u, q) for c in self.configs for u in us for q in self._questoes_unidade(c, u)
                       if q["auditoria"] is None]
            falhas += self._paralelo(tarefas, lambda x: self._auditar(*x), f"onda {w + 1}: auditoria")
            if falhas and any(CONFIGS[c]["retro"] for c in self.configs):
                return falhas         # a próxima onda depende desta estar completa
        return falhas

    # -------------------------------------------------------------- questões finais (todas contam)
    def finais(self, c: str) -> list[dict]:
        out = []
        for u in self.unidades:
            for q in self._questoes_unidade(c, u):
                a = q["auditoria"] or {}
                sust = self._arq_sust(q["uid"])
                s = read_json(sust)["status"] if sust.exists() else None
                aprov = bool(a.get("aprovada"))
                curta = len(str(q["resposta"]).split()) <= TETO_RESPOSTA
                intr = bool(a) and all(f in ("fora_da_fonte",) for f in a.get("falhas", [])) and a.get("motivo") != "bloqueio"
                ctx = a.get("contexto", [])
                out.append({"uid": q["uid"], "config": c, "item": u["item"], "foco": u["foco"], "visita": u["visita"],
                            "onda": u["onda"] + 1, "k": q["k"],
                            "tipo": q.get("tipo") if CONFIGS[c]["regras"] else a.get("tipo_sugerido"),
                            "pergunta": q["pergunta"], "resposta": q["resposta"], "explicacao": q.get("explicacao"),
                            "conhecimento": q.get("conhecimento"), "resposta_padrao": q.get("resposta_padrao"),
                            "formato_ok": formato_ok(q, CONFIGS[c]), "auditoria": {k: v for k, v in a.items() if k != "contexto"},
                            "aprovada_auditor": aprov, "valida_intrinseca": intr and curta, "resposta_curta": curta,
                            "sustentacao": s, "valida": aprov and curta and s == "totalmente_sustentado",
                            "blocos_contexto": [{"id": b["id"], "texto": b["texto"], "indice_documento": b["indice_documento"],
                                                 "item": b["item"]} for b in ctx],
                            "fonte_texto": "\n".join(b["texto"] for b in ctx)})
        return out

    # -------------------------------------------------------------- sustentação (das aprovadas pelo auditor)
    def sustentar(self) -> int:
        qs = [q for c in self.configs for q in self.finais(c) if q["aprovada_auditor"] and q["resposta_curta"]
              and not self._arq_sust(q["uid"]).exists()]

        def um(q):
            arq, nome = self._arq_sust(q["uid"]), "sustentacao_" + _nome_arq(q["uid"])
            blocos_ = [{"id": b["id"], "texto": b["texto"]} for b in q["blocos_contexto"]]
            bmap = {b["id"]: b["texto"] for b in blocos_}
            try:
                d = self.cliente("sustentacao").json(
                    C.prompt_gap("faithfulness"), json.dumps(dict(pergunta=q["pergunta"], gabarito=q["resposta"],
                                                                 blocos=blocos_), ensure_ascii=False),
                    tag="abl3_faithfulness", max_tokens=12000, item=q["item"],
                    validate=lambda d: validar_faithfulness(d, bmap))
                rec = {"uid": q["uid"], **resumo_faithfulness(d)}
            except Exception as exc:  # noqa: BLE001
                if not _filtrado(exc):
                    self._falha(nome, exc)
                    return False
                rec = {"uid": q["uid"], "status": "bloqueio_provedor"}
            atomic_json(arq, rec)
            self._ok(nome)
            return True
        return self._paralelo(qs, um, "sustentação")

    # -------------------------------------------------------------- quase-duplicatas (medida, não filtro)
    def _dedup(self, c: str) -> DedupIncremental:
        from .geracao import _Preguicoso
        return DedupIncremental(self.saida / c / "dedup", self.embedder, self.media, self.cal["limiar_auto"],
                                self.cal["limiar_juiz"], _Preguicoso(lambda: self.cliente("dedup_juiz")),
                                progress=self.progress)

    def deduplicar(self) -> int:
        falhas = 0
        for c in self.configs:
            dd = self._dedup(c)
            por_item = defaultdict(list)
            for q in sorted(self.finais(c), key=lambda q: (q["onda"], q["foco"], q["k"])):
                por_item[q["item"]].append({**q, "conhecimento": q.get("conhecimento") or q["pergunta"],
                                            "explicacao": q.get("explicacao") or ""})
            for item, lst in sorted(por_item.items()):
                falhas += dd.processar(item, lst, falha=self._falha, ok=self._ok)
        return falhas

    def redundantes(self, c: str) -> dict:
        dd = self._dedup(c)
        out = {}
        for item in self.itens:
            out.update(dd.redundantes(item))
        return out

    # -------------------------------------------------------------- dificuldade (amostra, válidas e inválidas)
    def amostra_dificuldade(self, n: int = AMOSTRA_DIFICULDADE) -> list[dict]:
        out = []
        for c in self.configs:
            qs = self.finais(c)
            por_item = defaultdict(list)
            for q in qs:
                por_item[q["item"]].append(q)
            m = min(n, len(qs))
            cota = {i: m * len(v) / len(qs) for i, v in por_item.items()} if qs else {}
            base = {i: int(x) for i, x in cota.items()}
            for i in sorted(cota, key=lambda i: (-(cota[i] - base[i]), i))[: m - sum(base.values())]:
                base[i] += 1
            for i in sorted(por_item):
                out += _rng("dificuldade", c, i).sample(sorted(por_item[i], key=lambda q: q["uid"]), base[i])
        return out

    def dificuldade(self, workers: int = 8, judge_workers: int = 2, clientes=None) -> int:
        from .completo import DatasetCompleto
        amostra = self.amostra_dificuldade()
        pasta = self.saida / "dificuldade"
        pasta.mkdir(parents=True, exist_ok=True)
        ds = [{"uid": q["uid"], "item": q["item"], "tipo": q["tipo"] or "nao_declarado", "fonte": q["config"],
               "composicao": "simples", "pergunta": q["pergunta"], "resposta": q["resposta"],
               "contexto_tecnico": q["fonte_texto"],
               "blocos_contexto": [{"id": b["id"], "texto": b["texto"], "indice_documento": b["indice_documento"]}
                                   for b in q["blocos_contexto"]]} for q in amostra]
        C.gravar_jsonl(pasta / "dataset.jsonl", ds)
        self.progress(f"[ablação v3] dificuldade: {len(ds)} questões x 2 condições x {len(PAINEL)} modelos", flush=True)
        d = DatasetCompleto(pasta, modelos=PAINEL, fontes_=[], progress=self.progress)
        return d.avaliar(workers=workers, judge_workers=judge_workers, clientes=clientes)

    def _vereditos(self) -> dict:
        """uid -> modelo -> {closed_book, open_book}: veredito do juiz (pares.csv da avaliação de dificuldade)."""
        arq = self.saida / "dificuldade" / "pares.csv"
        out = defaultdict(dict)
        if arq.exists():
            with arq.open(encoding="utf-8-sig") as f:
                for r in csv.DictReader(C.sem_nul(f)):
                    out[r["uid"]][r["modelo"]] = {a: r[f"veredito_{a}"] for a in ("closed_book", "open_book")}
        return out

    # -------------------------------------------------------------- execução
    def executar(self, etapas=ETAPAS, workers_avaliacao: int = 8, judge_workers: int = 2, clientes_avaliacao=None) -> int:
        etapas = tuple(etapas)
        falhas = 0
        if "geracao" in etapas:
            falhas += self.gerar()
        if "sustentacao" in etapas and not falhas:
            falhas += self.sustentar()
        if "dedup" in etapas and not falhas:
            falhas += self.deduplicar()
        if falhas:
            self.progress(f"[ablação v3] {falhas} unidades com falha (em {C.relativo(self.saida / 'falhas')}); repita o "
                          "mesmo comando", flush=True)
            return 2
        for c in self.configs:
            C.gravar_jsonl(self.saida / f"questoes_{c}.jsonl", self.finais(c))
        if "dificuldade" in etapas:
            st = self.dificuldade(workers_avaliacao, judge_workers, clientes_avaliacao)
            if st:
                return st
        if "relatorio" in etapas:
            self.relatorio()
        return 0

    # -------------------------------------------------------------- relatório
    def _custo(self) -> dict:
        out = defaultdict(lambda: {"chamadas": 0, "tokens_entrada": 0, "tokens_saida": 0})
        arq = self.saida / "chamadas" / "geracao.jsonl"
        for r in (C.linhas(arq) if arq.exists() else []):
            if r.get("ok") and str(r.get("tag", "")).startswith("abl3_"):
                c = r["tag"][5:]
                out[c]["chamadas"] += 1
                out[c]["tokens_entrada"] += int(r.get("prompt_tokens") or 0)
                out[c]["tokens_saida"] += int(r.get("completion_tokens") or 0)
        return dict(out)

    def relatorio(self) -> dict:
        finais = {c: (C.linhas(self.saida / f"questoes_{c}.jsonl") if (self.saida / f"questoes_{c}.jsonl").exists()
                      else self.finais(c)) for c in CONFIGS if (self.saida / c).exists()}
        df = Counter(t for bs in self.todos.values() for t in {t for b in bs for t in conteudo(b["texto"])})
        try:
            emb = self.embedder
            emb.encode(["teste"])
        except Exception as exc:  # noqa: BLE001
            self.progress(f"[ablação v3] embeddings indisponíveis ({type(exc).__name__}); sem diversidade semântica",
                          flush=True)
            emb = None
        ver, custo = self._vereditos(), self._custo()
        validas_n = [sum(q["valida"] for q in qs) for qs in finais.values()]
        m_ger = min(len(qs) for qs in finais.values()) if finais else 0
        m_val = min([v for v in validas_n if v >= 50] or [50])
        res = {"configs": {}, "comparacoes": {}, "unidades": len(self.unidades),
               "m_rarefacao": {"geradas": m_ger, "validas": m_val}}
        for c, qs in finais.items():
            red = self.redundantes(c) if (self.saida / c / "dedup").exists() else {}
            n = len(qs)
            chamadas = sum(1 for u in self.unidades if self._arq_ger(c, u).exists())
            val = [q for q in qs if q["valida"]]
            r = {"chamadas": chamadas, "geradas": n, "por_chamada": n / max(1, chamadas),
                 "chamadas_sem_questao": sum(1 for u in self.unidades if self._arq_ger(c, u).exists()
                                             and not read_json(self._arq_ger(c, u))["questoes"]),
                 "formato_ok": _pct(sum(q["formato_ok"] for q in qs), n),
                 "aprovadas_auditor": _taxa(qs, "aprovada_auditor"), "valida_intrinseca": _taxa(qs, "valida_intrinseca"),
                 "resposta_curta": _taxa(qs, "resposta_curta"), "validas": _taxa(qs, "valida"),
                 "validas_por_chamada": len(val) / max(1, chamadas),
                 "motivos_auditor": dict(Counter(f for q in qs for f in q["auditoria"].get("falhas", []))),
                 "tipos": dict(Counter(q["tipo"] or "?" for q in qs)),
                 "tipo_confere": _pct(sum(bool(q["auditoria"].get("tipo_confere")) for q in qs if q["aprovada_auditor"]),
                                      sum(q["aprovada_auditor"] for q in qs)) if CONFIGS[c]["regras"] else None,
                 "quase_duplicatas": _pct(sum(q["uid"] in red for q in qs), n),
                 "validas_unicas": sum(q["uid"] not in red for q in val),
                 "cobertura_focos_validos": _pct(len({(q["item"], q["foco"]) for q in val}),
                                                 len({(u["item"], u["foco"]) for u in self.unidades}))
                 if CONFIGS[c]["documento"] else None,
                 "palavras_pergunta": float(np.mean([len(q["pergunta"].split()) for q in qs])) if qs else None,
                 "palavras_resposta": float(np.mean([len(q["resposta"].split()) for q in qs])) if qs else None,
                 "vocabulario_geradas": vocabulario(qs, m_ger, df, len(self.todos), emb) if qs else {},
                 "vocabulario_validas": vocabulario(val, m_val, df, len(self.todos), emb) if val else {},
                 "custo": {**custo.get(c, {}), "tokens_por_valida": (custo.get(c, {}).get("tokens_entrada", 0)
                                                                     + custo.get(c, {}).get("tokens_saida", 0)) / max(1, len(val))},
                 "dificuldade": _dificuldade(qs, ver)}
            res["configs"][c] = r
        ordem = [c for c in CONFIGS if c in finais]
        for a, b in zip(ordem, ordem[1:]):
            res["comparacoes"][f"{b}_vs_{a}"] = {k: _diferenca(finais[b], finais[a], k)
                                                 for k in ("valida", "aprovada_auditor", "valida_intrinseca")}
        atomic_json(self.saida / "resultado.json", res)
        (self.saida / "ABLACAO.md").write_text(markdown(res), encoding="utf-8")
        return res


# ------------------------------------------------------------------ estatística
def _pct(k: int, n: int) -> float | None:
    return 100 * k / n if n else None


def _bootstrap_topico(qs: list[dict], chave: str, reps: int = 2000, semente: int = SEMENTE) -> tuple:
    """IC 95% da taxa por reamostragem de tópicos (as questões de um tópico não são independentes)."""
    por = defaultdict(list)
    for q in qs:
        por[q["item"]].append(bool(q[chave]))
    itens = sorted(por)
    if not itens:
        return (None, None)
    rng = np.random.default_rng(semente)
    k = np.array([sum(por[i]) for i in itens], dtype=float)
    n = np.array([len(por[i]) for i in itens], dtype=float)
    amostras = rng.integers(0, len(itens), (reps, len(itens)))
    taxas = 100 * k[amostras].sum(1) / n[amostras].sum(1)
    return (float(np.percentile(taxas, 2.5)), float(np.percentile(taxas, 97.5)))


def _taxa(qs: list[dict], chave: str) -> dict:
    k = sum(bool(q[chave]) for q in qs)
    return {"n": k, "pct": _pct(k, len(qs)), "ic95": _bootstrap_topico(qs, chave)}


def _diferenca(qa: list[dict], qb: list[dict], chave: str, reps: int = 2000, semente: int = SEMENTE) -> dict:
    """Diferença de taxas (a - b, pontos percentuais) com IC 95% e p bicaudal por bootstrap pareado de tópicos."""
    pa, pb = defaultdict(list), defaultdict(list)
    for q in qa:
        pa[q["item"]].append(bool(q[chave]))
    for q in qb:
        pb[q["item"]].append(bool(q[chave]))
    itens = sorted(set(pa) | set(pb))
    ka = np.array([sum(pa[i]) for i in itens], float)
    na = np.array([len(pa[i]) for i in itens], float)
    kb = np.array([sum(pb[i]) for i in itens], float)
    nb = np.array([len(pb[i]) for i in itens], float)
    obs = 100 * (ka.sum() / max(na.sum(), 1) - kb.sum() / max(nb.sum(), 1))
    rng = np.random.default_rng(semente)
    s = rng.integers(0, len(itens), (reps, len(itens)))
    d = 100 * (ka[s].sum(1) / np.maximum(na[s].sum(1), 1) - kb[s].sum(1) / np.maximum(nb[s].sum(1), 1))
    p = min(1.0, 2 * min((d <= 0).mean(), (d >= 0).mean()))
    return {"diferenca_pp": float(obs), "ic95": (float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))), "p": float(p)}


def _dificuldade(qs: list[dict], ver: dict) -> dict:
    """Acurácia média do painel (sem e com contexto) na amostra, nas válidas e nas inválidas."""
    def acc(grupo, cond):
        v = [ver[q["uid"]][m][cond] == "correta" for q in grupo for m in PAINEL if m in ver.get(q["uid"], {})]
        return 100 * float(np.mean(v)) if v else None

    def nenhum(grupo):
        v = [all(ver[q["uid"]][m]["closed_book"] != "correta" for m in PAINEL) for q in grupo
             if all(m in ver.get(q["uid"], {}) for m in PAINEL)]
        return 100 * float(np.mean(v)) if v else None
    am = [q for q in qs if q["uid"] in ver]
    out = {"amostra": len(am)}
    for nome, g in (("todas", am), ("validas", [q for q in am if q["valida"]]),
                    ("invalidas", [q for q in am if not q["valida"]])):
        out[nome] = {"n": len(g), "acerto_sem_contexto": acc(g, "closed_book"), "acerto_com_contexto": acc(g, "open_book"),
                     "nenhum_modelo_acerta_sem_contexto": nenhum(g),
                     "por_modelo_sem_contexto": {m: (100 * float(np.mean(x)) if (x := [ver[q["uid"]][m]["closed_book"] == "correta"
                                                                                         for q in g if m in ver.get(q["uid"], {})]) else None)
                                                 for m in PAINEL}}
    return out


def _f(x, casas=1):
    return "-" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{casas}f}".replace(".", ",")


def markdown(r: dict) -> str:
    cs = list(r["configs"])
    out = ["# Ablação da geração v3 (escada cumulativa, sem poda)", "",
           f"{r['unidades']} chamadas por configuração (focos x visitas), de 0 a {POR_CHAMADA} questões por chamada. Toda "
           "questão gerada é avaliada. Válida = aprovada pelo auditor v23 + resposta de até "
           f"{TETO_RESPOSTA} palavras + gabarito totalmente sustentado. IC 95% por reamostragem de tópicos.", "",
           "| Configuração | Geradas | Por chamada | Aprovadas pelo auditor | Válida intrínseca | Válidas | "
           "Válidas por chamada | Quase-duplicatas | Tokens por válida |", "|---|---|---|---|---|---|---|---|---|"]
    for c in cs:
        x = r["configs"][c]

        def t(k):
            return f"{_f(x[k]['pct'])}% ({_f(x[k]['ic95'][0])}–{_f(x[k]['ic95'][1])})"
        out.append(f"| {NOME[c]} | {x['geradas']} | {_f(x['por_chamada'], 2)} | {t('aprovadas_auditor')} | "
                   f"{t('valida_intrinseca')} | {t('validas')} | {_f(x['validas_por_chamada'], 2)} | "
                   f"{_f(x['quase_duplicatas'])}% | {_f(x['custo'].get('tokens_por_valida'), 0)} |")
    out += ["", "| Comparação (degrau) | Válidas: diferença (pp, IC 95%, p) | Aprovadas pelo auditor |", "|---|---|---|"]
    for k, v in r["comparacoes"].items():
        b, a = k.split("_vs_")
        f = lambda d: f"{_f(d['diferenca_pp'])} ({_f(d['ic95'][0])}–{_f(d['ic95'][1])}), p={d['p']:.3g}"  # noqa: E731
        out.append(f"| {NOME[a]} → {NOME[b]} | {f(v['valida'])} | {f(v['aprovada_auditor'])} |")
    out += ["", "## Diversidade (geradas, amostras do mesmo tamanho)", "",
            f"m = {r['m_rarefacao']['geradas']} questões por amostra.", "",
            "| Configuração | Self-BLEU por tópico | Distinct-2 | MATTR | MTLD | Vocabulário | Cosseno médio no tópico | Vendi relativo |",
            "|---|---|---|---|---|---|---|---|"]
    for c in cs:
        v = r["configs"][c]["vocabulario_geradas"]
        out.append(f"| {NOME[c]} | {_f(v.get('self_bleu_por_topico'), 3)} | {_f(v.get('distinct_2'), 3)} | "
                   f"{_f(v.get('mattr'), 3)} | {_f(v.get('mtld'), 1)} | {_f(v.get('vocabulario_conteudo'), 0)} | "
                   f"{_f(v.get('cosseno_medio_por_topico'), 3)} | {_f(v.get('vendi_relativo_por_topico'), 3)} |")
    out += ["", "## Dificuldade (amostra, painel sem e com contexto)", "",
            "| Configuração | Amostra | Acerto sem contexto (todas / válidas / inválidas) | Com contexto (todas) | "
            "Nenhum modelo acerta (válidas) |", "|---|---|---|---|---|"]
    for c in cs:
        d = r["configs"][c]["dificuldade"]
        if not d.get("amostra"):
            continue
        out.append(f"| {NOME[c]} | {d['amostra']} | {_f(d['todas']['acerto_sem_contexto'])} / "
                   f"{_f(d['validas']['acerto_sem_contexto'])} / {_f(d['invalidas']['acerto_sem_contexto'])} | "
                   f"{_f(d['todas']['acerto_com_contexto'])} | {_f(d['validas']['nenhum_modelo_acerta_sem_contexto'])} |")
    out += ["", "Motivos de reprovação do auditor:", ""]
    for c in cs:
        out.append(f"- {NOME[c]}: {r['configs'][c]['motivos_auditor']}")
    return "\n".join(out) + "\n"


def exemplos_prompts(ab: AblacaoV3, pasta: Path | None = None) -> Path:
    """Grava o prompt de sistema e um exemplo de mensagem de cada configuração (1ª unidade), para revisão."""
    pasta = Path(pasta or ab.saida / "prompts")
    pasta.mkdir(parents=True, exist_ok=True)
    u = ab.unidades[0]
    u2 = next((x for x in ab.unidades if x["item"] == u["item"] and x["foco"] == u["foco"] and x["visita"] == 2), u)
    for c in ab.configs:
        (pasta / f"{c}_sistema.md").write_text(ab.sistema(c, u["item"]) + "\n", encoding="utf-8")
        (pasta / f"{c}_usuario_onda1.md").write_text(ab.usuario(c, u, []) + "\n", encoding="utf-8")
        if CONFIGS[c]["retro"]:
            (pasta / f"{c}_usuario_visita2.md").write_text(ab.usuario(c, u2) + "\n", encoding="utf-8")
    return pasta
