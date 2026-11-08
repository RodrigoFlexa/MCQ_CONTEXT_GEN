"""Estudo de ablação da geração: quanto cada componente do pipeline rende em questões aceitas e em vocabulário.

Pedido: 1000 questões por braço, a partir de 1000 "vagas" sorteadas do banco final v1 (petroquest_banco_v1), e a
mesma aceitação para todos os braços. Cada vaga é (documento, bloco foco, tipo) de uma questão do banco gerada por
janela nos documentos base (v23c, variada, conceitos e as três gerações por tipo), estratificada por tópico x tipo.

Braços (mesmo gerador, GPT-5.4 high, uma questão por vaga):
  naive         só o pedido: "gere N questões sobre <tema/escopo do especialista>", sem documento, exemplos,
                regras ou retroalimentação; uma chamada por tópico com N = vagas do tópico;
  documento     janela de 3 blocos + regras (prompt ablacao_slot, com as 9 ruins da v23), uma tentativa;
  sem_externos  documento + retroalimentação (até 3 tentativas; nas novas, as tentativas recusadas com o motivo e os
                conhecimentos já aceitos no documento), sem exemplos de forma;
  sem_retro     documento + exemplos de forma (8 de datasets externos ou, em 1/4 das vagas, 6 do dataset de múltipla
                escolha convertido), uma tentativa;
  completo      documento + exemplos de forma + retroalimentação.
A 1ª tentativa de sem_externos é a de documento, e a de completo é a de sem_retro (mesmo prompt, mesmo cache):
o ganho da retroalimentação é medido nas mesmas vagas.

Aceitação (igual para todos): auditor v23 (5 verificações, com os blocos da janela; no naive, os 3 blocos do
documento do tópico mais parecidos com a questão por TF-IDF) + resposta de até 20 palavras + sustentação total
(faithfulness) + deduplicação calibrada dentro do braço. A régua determinística só decide novas tentativas.
Métricas de vocabulário e diversidade: distinct-1/2 e vocabulário rarefeitos, MATTR, MTLD, termos especializados,
Self-BLEU por tópico, diversidade de embeddings (cosseno médio e Vendi por tópico), aberturas e cópia do documento.
Saída: relatorios/ablacao_geracao_v1 (ABLACAO.md, resultado.json, questoes_<braço>.jsonl).
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import re
import threading
import unicodedata
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
from .dedup import DedupIncremental, carregar_calibracao, centrar
from .tipo_unico import CENARIO as CENARIO_TIPO, DEFINICOES as DEFINICOES_TIPO
from .v22 import validar_auditoria, veredito
from .v23 import CHAVES_V23, carregar_exemplos, regua_v23
from .variada import (CONVERTIDAS, bloco_forma, bloco_ruins, carregar_convertidas, carregar_externos,
                      sortear_convertidas, sortear_externos)

SAIDA = C.QA / "relatorios" / "ablacao_geracao_v1"
BANCO = C.QA / "relatorios" / "petroquest_banco_v1" / "banco.jsonl"
FONTES_BASE = ("v23c", "variada", "conceitos", "tipo_decisao", "tipo_diagnostico", "tipo_procedimento")
N_VAGAS = 1000
SEMENTE = 20261108
TENTATIVAS = 3
TETO_RESPOSTA = 20
FRACAO_CONVERTIDAS = 0.25
GERADOR = "gpt-5-4-petrobras:high"
AUDITOR = "gpt-5-4-petrobras:high"
BRACOS = {
    "naive": {"documento": False, "exemplos": False, "retro": False},
    "documento": {"documento": True, "exemplos": False, "retro": False},
    "sem_externos": {"documento": True, "exemplos": False, "retro": True},
    "sem_retro": {"documento": True, "exemplos": True, "retro": False},
    "completo": {"documento": True, "exemplos": True, "retro": True},
}
NOME_BRACO = {"naive": "Naive (só o tópico)", "documento": "Documento + regras", "sem_externos": "Sem datasets externos",
              "sem_retro": "Sem retroalimentação", "completo": "Pipeline completo", "banco": "Banco final (referência)"}
DEFINICOES = {
    **DEFINICOES_TIPO,
    "conceito": ("Pergunta de nomeação: o enunciado descreve a função, a propriedade, o efeito ou o papel de um "
                 "componente, material, fenômeno, grandeza, método ou prática, e a resposta é o nome técnico "
                 "(até 6 palavras), sem que o termo ou sua raiz apareça no enunciado."),
    "mecanismo": ("Por que ou como algo acontece: a resposta é o mecanismo físico, químico ou operacional que liga a "
                  "causa ao efeito, não o efeito nem uma categoria de falha."),
    "consequencia": ("Dada uma condição, mudança ou falha, qual o efeito técnico específico: a resposta é a "
                     "consequência direta mais relevante, com a direção quando houver (aumenta, reduz, desloca)."),
}
CENARIO = {**CENARIO_TIPO, "conceito": "sempre false: conceito é pergunta direta, de até 35 palavras.",
           "mecanismo": "true quando o enunciado descreve uma situação; false na pergunta direta.",
           "consequencia": "true quando o enunciado descreve uma situação; false na pergunta direta."}
STOP = set("""a o e é as os um uma uns umas de da do das dos em no na nos nas num numa por pelo pela pelos pelas para
pra com sem sob sobre entre até após ante que qual quais quando onde como porque por que se ser são foi era está estão
ou mas nem não sim mais menos muito muita muitos muitas pouco já ainda também só apenas ao aos à às isso isto esse essa
esses essas este esta estes estas aquele aquela seu sua seus suas deve devem pode podem há tem têm ter sendo sido cada
outro outra outros outras mesmo mesma lhe the of and to in is for on what which why how""".split())
ABERTURA = re.compile(r"^(em (um|uma)|num|numa|após|durante|ao)\b", re.I)


# ------------------------------------------------------------------ vagas
def _h(*p) -> int:
    return int(hashlib.sha256("|".join(map(str, p)).encode()).hexdigest()[:12], 16)


def selecionar(banco: Path = BANCO, n: int = N_VAGAS, semente: int = SEMENTE) -> list[dict]:
    """n vagas (documento, foco, tipo) distintas, proporcionais a tópico x tipo no banco (maiores restos)."""
    elegiveis, vistos = [], set()
    for q in sorted(C.linhas(banco), key=lambda q: q["id"]):
        fonte, item, origem, *resto = q["uid"].split(":")
        chave = (item, int(resto[1]), q["tipo"]) if origem == "j" else None
        if fonte in FONTES_BASE and origem == "j" and chave not in vistos:
            vistos.add(chave)
            elegiveis.append({**q, "foco": chave[1]})
    if len(elegiveis) < n:
        raise ValueError(f"Só {len(elegiveis)} vagas elegíveis no banco ({n} pedidas)")
    estratos = defaultdict(list)
    for q in elegiveis:
        estratos[(q["item"], q["tipo"])].append(q)
    cota = {k: n * len(v) / len(elegiveis) for k, v in estratos.items()}
    base = {k: int(c) for k, c in cota.items()}
    for k in sorted(cota, key=lambda k: (-(cota[k] - base[k]), k))[: n - sum(base.values())]:
        base[k] += 1
    rng = random.Random(semente)
    out = []
    for k in sorted(estratos):
        out += rng.sample(sorted(estratos[k], key=lambda q: q["id"]), base[k])
    out.sort(key=lambda q: (q["item"], q["foco"], q["tipo"]))
    return [{"vaga": f"V{k:04d}", "item": q["item"], "foco": q["foco"], "tipo": q["tipo"], "ref_id": q["id"],
             "ref_uid": q["uid"], "ref_pergunta": q["pergunta"], "ref_resposta": q["resposta"]}
            for k, q in enumerate(out, 1)]


# ------------------------------------------------------------------ validações
def validar_slot(d: dict) -> None:
    if not isinstance(d, dict) or set(d) != {"questoes", "motivo"}:
        raise ValueError("Use exatamente as chaves questoes e motivo.")
    if not isinstance(d["questoes"], list) or len(d["questoes"]) != 1 or not isinstance(d["questoes"][0], dict):
        raise ValueError("questoes deve ser uma lista com exatamente 1 objeto.")


def validar_naive(d: dict, n: int) -> None:
    if not isinstance(d, dict) or set(d) != {"questoes"} or not isinstance(d["questoes"], list):
        raise ValueError("Use exatamente a chave questoes, com uma lista.")
    if len(d["questoes"]) != n:
        raise ValueError(f"Entregue exatamente {n} questões (vieram {len(d['questoes'])}).")
    for q in d["questoes"]:
        if not isinstance(q, dict) or set(q) != {"pergunta", "resposta"} or not all(
                isinstance(q[k], str) and q[k].strip() for k in q):
            raise ValueError("Cada questão tem exatamente pergunta e resposta, ambas preenchidas.")


# ------------------------------------------------------------------ métricas de vocabulário
def _sem_acento(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def tokens(texto: str) -> list[str]:
    return re.findall(r"[a-zà-ÿ0-9]+(?:-[a-zà-ÿ0-9]+)*", texto.lower())


def conteudo(texto: str) -> list[str]:
    return [t for t in tokens(texto) if t not in STOP and not t.isdigit() and len(t) > 2]


def distinct(textos: list[str], n: int) -> float:
    grams = [tuple(ts[i:i + n]) for t in textos for ts in [tokens(t)] for i in range(len(ts) - n + 1)]
    return len(set(grams)) / len(grams) if grams else 0.0


def mattr(toks: list[str], janela_: int = 50) -> float:
    if len(toks) <= janela_:
        return len(set(toks)) / max(1, len(toks))
    cont = Counter(toks[:janela_])
    soma = len(cont)
    for i in range(janela_, len(toks)):
        cont[toks[i]] += 1
        cont[toks[i - janela_]] -= 1
        if not cont[toks[i - janela_]]:
            del cont[toks[i - janela_]]
        soma += len(cont)
    return soma / (janela_ * (len(toks) - janela_ + 1))      # média da razão tipos/tokens por janela


def mtld(toks: list[str], limiar: float = 0.72) -> float:
    def um_sentido(seq):
        fatores, tipos_, n = 0.0, set(), 0
        for t in seq:
            n += 1
            tipos_.add(t)
            if len(tipos_) / n <= limiar:
                fatores, tipos_, n = fatores + 1, set(), 0
        if n:
            fatores += (1 - len(tipos_) / n) / (1 - limiar)
        return len(seq) / fatores if fatores else float(len(seq))
    return (um_sentido(toks) + um_sentido(toks[::-1])) / 2 if toks else 0.0


def self_bleu(textos: list[str]) -> float:
    from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
    ts = [tokens(t) for t in textos]
    if len(ts) < 2:
        return float("nan")
    sm = SmoothingFunction().method1
    return float(np.mean([sentence_bleu(ts[:i] + ts[i + 1:], ts[i], smoothing_function=sm) for i in range(len(ts))]))


def vendi(V: np.ndarray) -> float:
    """Vendi score (número efetivo de questões distintas) de vetores normalizados."""
    if len(V) < 2:
        return float(len(V))
    w = np.clip(np.linalg.eigvalsh(V @ V.T / len(V)), 0, None)
    w = w[w > 1e-12]
    return float(math.exp(-(w * np.log(w)).sum()))


def _ngrams(ts, n):
    return {tuple(ts[i:i + n]) for i in range(len(ts) - n + 1)}


def vocabulario(qs: list[dict], m: int, df_docs: dict, n_docs: int, embed=None, reps: int = 30,
                semente: int = 7) -> dict:
    """Métricas das perguntas de um conjunto; as dependentes do tamanho são rarefeitas a m questões."""
    if not qs:
        return {"n": 0}
    perg = [q["pergunta"] for q in qs]
    rng = random.Random(semente)
    rare = defaultdict(list)
    m = min(m, len(qs))
    for _ in range(reps):
        amostra = rng.sample(qs, m)
        tx = [q["pergunta"] for q in amostra]
        cont = [t for x in tx for t in conteudo(x)]
        rare["distinct_1"].append(distinct(tx, 1))
        rare["distinct_2"].append(distinct(tx, 2))
        rare["vocabulario_conteudo"].append(len(set(cont)))
        rare["termos_especializados"].append(len({t for t in cont if 0 < df_docs.get(t, 0) <= max(1, n_docs // 4)}))
        rare["aberturas_distintas"].append(len({" ".join(tokens(x)[:2]) for x in tx}) / m)
    out = {"n": len(qs), "m_rarefeito": m, **{k: float(np.mean(v)) for k, v in rare.items()}}
    seq = [t for p in rng.sample(perg, len(perg)) for t in tokens(p)]
    cont_all = [t for p in perg for t in conteudo(p)]
    out.update(mattr=mattr(seq), mtld=mtld(seq),
               fracao_tokens_especializados=float(np.mean(
                   [0 < df_docs.get(t, 0) <= max(1, n_docs // 4) for t in cont_all])) if cont_all else 0.0,
               abertura_cliche=float(np.mean([bool(ABERTURA.match(_sem_acento(p).strip())) for p in perg])),
               palavras_pergunta=float(np.mean([len(p.split()) for p in perg])),
               palavras_resposta=float(np.mean([len(q["resposta"].split()) for q in qs])))
    por_item = defaultdict(list)
    for q in qs:
        por_item[q["item"]].append(q)
    sb = [self_bleu([q["pergunta"] for q in v]) for v in por_item.values() if len(v) >= 2]
    out["self_bleu_por_topico"] = float(np.nanmean(sb)) if sb else float("nan")
    copias = []
    for q in qs:
        ts = conteudo(q["pergunta"])
        g = _ngrams(ts, 3)
        if g and q.get("fonte_texto"):
            copias.append(len(g & _ngrams(conteudo(q["fonte_texto"]), 3)) / len(g))
    out["copia_3gramas_do_documento"] = float(np.mean(copias)) if copias else float("nan")
    if embed is not None:
        V = np.asarray(embed.encode([q["pergunta"] for q in qs]), dtype=float)
        V = V / np.clip(np.linalg.norm(V, axis=1, keepdims=True), 1e-12, None)
        pos = defaultdict(list)
        for k, q in enumerate(qs):
            pos[q["item"]].append(k)
        cos, ven = [], []
        for ks in pos.values():
            if len(ks) >= 2:
                S = V[ks] @ V[ks].T
                cos.append(float(S[np.triu_indices(len(ks), 1)].mean()))
                ven.append(vendi(V[ks]) / len(ks))
        out.update(cosseno_medio_por_topico=float(np.mean(cos)) if cos else float("nan"),
                   vendi_relativo_por_topico=float(np.mean(ven)) if ven else float("nan"))
    return out


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if not n:
        return (0.0, 0.0)
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    d = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (100 * (c - d), 100 * (c + d))


def mcnemar(a: list[bool], b: list[bool]) -> dict:
    """Teste exato de McNemar (bicaudal) entre dois braços nas mesmas vagas."""
    so_a = sum(x and not y for x, y in zip(a, b))
    so_b = sum(y and not x for x, y in zip(a, b))
    n = so_a + so_b
    p = min(1.0, 2 * sum(math.comb(n, k) for k in range(0, min(so_a, so_b) + 1)) / 2 ** n) if n else 1.0
    return {"so_primeiro": so_a, "so_segundo": so_b, "p": p}


# ------------------------------------------------------------------ estudo
class Ablacao:
    def __init__(self, saida: Path = SAIDA, *, banco: Path = BANCO, exp: Path = C.EXPERIMENTO, docs: Path = DOCS,
                 n: int = N_VAGAS, bracos=None, externos: Path | None = None, convertidas: Path = CONVERTIDAS,
                 workers: int = 8, clientes: dict | None = None, embedder=None, progress=print):
        self.saida, self.banco, self.docs_dir = Path(saida), Path(banco), Path(docs)
        self.n, self.workers, self.progress = int(n), max(1, int(workers)), progress
        self.bracos = list(bracos or BRACOS)
        if any(b not in BRACOS for b in self.bracos):
            raise ValueError(f"braços válidos: {', '.join(BRACOS)}")
        cal_arq = Path(exp) / "calibracao" / "calibracao.json"
        if not cal_arq.exists():
            raise ValueError(f"Falta a calibração da deduplicação ({C.relativo(cal_arq)})")
        self.cal = carregar_calibracao(cal_arq)
        self.media = np.asarray(read_json(cal_arq.parent / self.cal["media"]), dtype=float)
        self.pools, self.arq_externos = carregar_externos(externos)
        self.arq_convertidas = Path(convertidas)
        self.convertidas = carregar_convertidas(self.arq_convertidas)
        self.ruins = carregar_exemplos()["ruins"]
        self._clientes, self._embedder = dict(clientes or {}), embedder
        self._trava = threading.Lock()
        self._tfidf: dict = {}
        self.saida.mkdir(parents=True, exist_ok=True)
        arq = self.saida / "vagas.jsonl"
        if not arq.exists():
            C.gravar_jsonl(arq, selecionar(self.banco, self.n))
        self.vagas = C.linhas(arq)
        if len(self.vagas) != self.n:
            raise ValueError(f"{C.relativo(arq)} tem {len(self.vagas)} vagas, não {self.n}; use outra saída")
        self.itens = sorted({v["item"] for v in self.vagas})
        self.docs = {i: blocos(i, self.docs_dir)[1] for i in self.itens}
        self.temas = {i: tema(i) for i in self.itens}
        self._config()

    # -------------------------------------------------------------- infraestrutura
    def _config(self) -> None:
        cfg = {"schema": "ablacao-geracao-v1", "n": self.n, "semente": SEMENTE, "banco_sha256": C.sha(self.banco.read_text(
            encoding="utf-8")), "fontes_base": list(FONTES_BASE), "tentativas": TENTATIVAS, "teto_resposta": TETO_RESPOSTA,
            "fracao_convertidas": FRACAO_CONVERTIDAS, "gerador": GERADOR, "auditor": AUDITOR,
            "sustentacao": C.SUSTENTACAO, "dedup": {k: self.cal[k] for k in ("embedding", "limiar_auto", "limiar_juiz", "juiz")},
            "prompts_sha256": {p: C.sha(C.prompt(p)) for p in ("ablacao_naive", "ablacao_slot", "auditoria_v23")},
            "externos_sha256": C.sha(self.arq_externos.read_text(encoding="utf-8")),
            "convertidas_sha256": C.sha(self.arq_convertidas.read_text(encoding="utf-8")),
            "docs_sha256": {i: C.sha(read_json(self.docs_dir / i / "documento.json")) for i in self.itens}}
        arq = self.saida / "config.json"
        if arq.exists():
            antigo = {k: v for k, v in read_json(arq).items() if k != "criado_em"}
            if antigo != cfg:
                diff = sorted(k for k in set(antigo) | set(cfg) if antigo.get(k) != cfg.get(k))
                raise ValueError(f"Configuração diferente da pasta existente ({', '.join(diff)}); use outra saída")
            return
        atomic_json(arq, {**cfg, "criado_em": datetime.now(timezone.utc).isoformat()})

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

    def _falha(self, nome: str, exc: Exception) -> None:
        atomic_json(self.saida / "falhas" / f"{nome}.json",
                    {"erro": type(exc).__name__, "mensagem": str(exc)[:2000], "em": datetime.now(timezone.utc).isoformat()})

    def _ok(self, nome: str) -> None:
        f = self.saida / "falhas" / f"{nome}.json"
        if f.exists():
            f.unlink()

    def _paralelo(self, tarefas: list, funcao, rotulo: str) -> int:
        if not tarefas:
            return 0
        falhas = 0
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            for k, ok in enumerate(pool.map(funcao, tarefas), 1):
                falhas += 0 if ok else 1
                if k % 50 == 0 or k == len(tarefas):
                    self.progress(f"[ablação] {rotulo}: {k}/{len(tarefas)} ({falhas} falhas)", flush=True)
        return falhas

    def _tema(self, item: str) -> str:
        t = self.temas[item]
        return (f"<tema>\nÁrea: {t['area']}\nTema: {t['tema']}\n</tema>\n\n"
                f"<escopo_orientador>\n{t['escopo']}\n</escopo_orientador>")

    # -------------------------------------------------------------- auditor (comum a todos os braços)
    def _auditar(self, arq: Path, q: dict, tipo: str, blocos_txt: str) -> bool:
        if arq.exists():
            return True
        nome = "auditoria_" + arq.parent.parent.name + "_" + arq.stem
        user = json.dumps({"tipo_declarado": tipo, "pergunta": q["pergunta"], "resposta_referencia": q["resposta"],
                           "explicacao_do_autor": q.get("explicacao") or "(não informada)", "blocos": blocos_txt},
                          ensure_ascii=False)
        try:
            d = self.cliente("auditoria").json(C.prompt("auditoria_v23"), user, tag="ablacao_auditoria",
                                               max_tokens=6000, item=q.get("item"), validate=validar_auditoria)
            rec = veredito(d, tipo)
        except Exception as exc:  # noqa: BLE001 - isolada por questão
            if not _filtrado(exc):
                self._falha(nome, exc)
                return False
            rec = {"aprovada": False, "motivo": "bloqueio", "falhas": ["bloqueio"], "tipo_sugerido": tipo,
                   "justificativa": "bloqueada pelo filtro de conteúdo"}
        atomic_json(arq, rec)
        self._ok(nome)
        return True

    # -------------------------------------------------------------- braço naive
    def _recuperar(self, item: str, texto: str, k: int = 3) -> list[dict]:
        """Os k blocos do documento do tópico mais parecidos com a questão (TF-IDF), na ordem do documento."""
        from sklearn.feature_extraction.text import TfidfVectorizer
        bs = self.docs[item]
        with self._trava:
            if item not in self._tfidf:
                V = TfidfVectorizer(sublinear_tf=True).fit([f"{b['subtitulo']} {b['texto']}" for b in bs])
                self._tfidf[item] = (V, V.transform([f"{b['subtitulo']} {b['texto']}" for b in bs]))
            V, M = self._tfidf[item]
        s = (M @ V.transform([texto]).T).toarray().ravel()
        return [bs[i] for i in sorted(np.argsort(-s, kind="stable")[:k])]

    def _naive_lote(self, item: str) -> bool:
        arq = self.saida / "naive" / "lotes" / f"{item}.json"
        if arq.exists():
            return True
        n = sum(v["item"] == item for v in self.vagas)
        nome = f"naive_{item}"
        try:
            d = self.cliente("geracao").json(C.prompt("ablacao_naive"), self._tema(item) + f"\n\nQuantidade: {n} questões.",
                                             tag="ablacao_naive", max_tokens=24000, item=item,
                                             validate=lambda d: validar_naive(d, n))
            qs = d["questoes"]
        except Exception as exc:  # noqa: BLE001
            if not _filtrado(exc):
                self._falha(nome, exc)
                return False
            qs = []
        atomic_json(arq, {"item": item, "pedidas": n, "questoes": qs})
        self._ok(nome)
        return True

    def _naive_questoes(self) -> list[dict]:
        out = []
        for item in self.itens:
            arq = self.saida / "naive" / "lotes" / f"{item}.json"
            if not arq.exists():
                continue
            d = read_json(arq)
            for k in range(d["pedidas"]):
                q = d["questoes"][k] if k < len(d["questoes"]) else None
                out.append({"uid": f"naive:{item}:{k + 1:03d}", "braco": "naive", "item": item, "tipo": None,
                            "tentativa": 1, **({"pergunta": q["pergunta"], "resposta": q["resposta"]} if q else
                                               {"pergunta": None, "resposta": None})})
        return out

    def naive(self) -> int:
        falhas = self._paralelo([i for i in self.itens], self._naive_lote, "naive: geração")
        qs = [q for q in self._naive_questoes() if q["pergunta"]]

        def auditar(q):
            sel = self._recuperar(q["item"], q["pergunta"] + " " + q["resposta"])
            txt = "\n\n".join(f"[B{k}] {b['titulo_capitulo']} / {b['subtitulo']}\n{b['texto']}"
                              for k, b in enumerate(sel, 1))
            return self._auditar(self.saida / "naive" / "auditoria" / f"{_nome_arq(q['uid'])}.json", q,
                                 "nao_declarado", txt)
        return falhas + self._paralelo(qs, auditar, "naive: auditoria")

    # -------------------------------------------------------------- braços com documento
    def _arq(self, braco: str, vaga: str, t: int, pasta: str = "tentativas") -> Path:
        # 1ª tentativa compartilhada: sem_externos usa a de documento e completo a de sem_retro
        if t == 1 and braco in ("sem_externos", "completo"):
            braco = {"sem_externos": "documento", "completo": "sem_retro"}[braco]
        return self.saida / braco / pasta / f"{vaga}_t{t}.json"

    def _janela(self, v: dict):
        jan = janela(self.docs[v["item"]], v["foco"])
        txt = "\n\n".join(f"[{r}] {b['titulo_capitulo']} / {b['subtitulo']}\n{b['texto']}" for r, b in jan)
        return jan, {r: b["texto"] for r, b in jan}, txt

    def _exemplos(self, v: dict, t: int) -> str:
        if _h("conv", v["vaga"]) % 1000 < 1000 * FRACAO_CONVERTIDAS:
            return bloco_forma(sortear_convertidas(self.convertidas, v["item"], v["foco"] * 10 + t, (v["tipo"],)))
        return bloco_forma(sortear_externos(self.pools, v["item"], v["foco"], 10 * t + _h(v["tipo"]) % 7))

    def sistema(self, tipo: str, item: str) -> str:
        s = (C.prompt("ablacao_slot").replace("<<TIPO>>", tipo).replace("<<DEFINICAO>>", DEFINICOES[tipo])
             .replace("<<CENARIO>>", CENARIO[tipo]))
        return s + "\n\n" + bloco_ruins([e for e in self.ruins if e["item"] != item])

    def _estado(self, braco: str, v: dict, t: int) -> dict | None:
        """Tentativa t da vaga: questão, régua e auditoria (None se ainda não gerada)."""
        arq = self._arq(braco, v["vaga"], t)
        if not arq.exists():
            return None
        d = read_json(arq)
        aud = self._arq(braco, v["vaga"], t, "auditoria")
        d["auditoria"] = read_json(aud) if aud.exists() else None
        return d

    @staticmethod
    def _recusa(d: dict) -> str | None:
        """Motivo de recusa que uma nova tentativa pode corrigir; None se aprovada (ou bloqueada)."""
        if d["regua"]:
            return "recusada pela régua: " + "; ".join(d["regua"][:3])
        a = d["auditoria"]
        if a and not a["aprovada"] and a["motivo"] != "bloqueio":
            extra = f" Resposta alternativa apontada: {a['resposta_alternativa']}" if "varias_respostas" in a["falhas"] else ""
            return f"recusada pelo auditor ({a['motivo']}): {a['justificativa']}{extra}"
        return None

    def _cobertos(self, braco: str, item: str, ate: int) -> str:
        linhas = []
        for v in self.vagas:
            if v["item"] != item:
                continue
            for t in range(1, ate):
                d = self._estado(braco, v, t)
                if d and d.get("questao") and not d["regua"] and d["auditoria"] and d["auditoria"]["aprovada"]:
                    linhas.append(f"- {d['questao']['conhecimento']} (resposta: {d['questao']['resposta']})")
        return "\n".join(linhas[:60]) or "Nenhum ainda."

    def _tentar(self, braco: str, v: dict, t: int) -> bool:
        cfg = BRACOS[braco]
        arq, nome = self._arq(braco, v["vaga"], t), f"{braco}_{v['vaga']}_t{t}"
        jan, textos, txt = self._janela(v)
        if not arq.exists():
            partes = [self._tema(v["item"])]
            if t > 1:
                ant = []
                for k in range(1, t):
                    d = self._estado(braco, v, k)
                    q = d.get("questao") or {}
                    ant.append(f"- {q.get('pergunta', '(sem questão)')} → {q.get('resposta', '-')}\n  {self._recusa(d)}")
                partes += ["<tentativas_anteriores>\n" + "\n".join(ant) + "\n</tentativas_anteriores>",
                           f"<conhecimentos_cobertos>\n{self._cobertos(braco, v['item'], t)}\n</conhecimentos_cobertos>"]
            if cfg["exemplos"]:
                partes.append(self._exemplos(v, t))
            partes.append(f"<janela>\n{txt}\n</janela>")
            try:
                d = self.cliente("geracao").json(self.sistema(v["tipo"], v["item"]), "\n\n".join(partes),
                                                 tag="ablacao_slot", max_tokens=12000, item=v["item"], validate=validar_slot)
                q = d["questoes"][0]
                rec = {"vaga": v["vaga"], "tentativa": t, "questao": q, "regua": regua_v23(q, textos, (v["tipo"],), "F")}
            except Exception as exc:  # noqa: BLE001
                if not _filtrado(exc):
                    self._falha(nome, exc)
                    return False
                rec = {"vaga": v["vaga"], "tentativa": t, "questao": None, "regua": ["bloqueado pelo filtro de conteúdo"]}
            atomic_json(arq, rec)
            self._ok(nome)
        d = read_json(arq)
        q = d["questao"]
        ultima = t == TENTATIVAS or not cfg["retro"]
        # a régua decide a nova tentativa; a última (ou única) tentativa é sempre auditada, para a aceitação comum
        if self._tem_questao(d) and (not d["regua"] or ultima):
            return self._auditar(self._arq(braco, v["vaga"], t, "auditoria"), {**q, "item": v["item"]}, v["tipo"], txt)
        return True

    @staticmethod
    def _tem_questao(d: dict) -> bool:
        q = d.get("questao")
        return isinstance(q, dict) and isinstance(q.get("pergunta"), str) and isinstance(q.get("resposta"), str)

    def _proxima(self, braco: str, v: dict) -> int | None:
        """Próxima tentativa a fazer na vaga (None = vaga encerrada). Uma tentativa gerada mas ainda sem a auditoria
        devida volta a ser feita (só a auditoria é paga)."""
        retro = BRACOS[braco]["retro"]
        for t in range(1, TENTATIVAS + 1):
            d = self._estado(braco, v, t)
            if d is None:
                return t
            ultima = t == TENTATIVAS or not retro
            if self._tem_questao(d) and (not d["regua"] or ultima) and d["auditoria"] is None:
                return t
            if ultima or self._recusa(d) is None:
                return None
        return None

    def documento(self, bracos: list[str]) -> int:
        falhas = 0
        for t in range(1, TENTATIVAS + 1):
            for b in bracos:              # 1ª tentativa: os braços base primeiro (os com retro reaproveitam)
                tarefas = [v for v in self.vagas if self._proxima(b, v) == t]
                falhas += self._paralelo(tarefas, lambda v, b=b, t=t: self._tentar(b, v, t), f"{b}: tentativa {t}")
        return falhas

    # -------------------------------------------------------------- questão final de cada vaga
    def finais(self, braco: str) -> list[dict]:
        if braco == "naive":
            out = []
            for q in self._naive_questoes():
                aud = self.saida / "naive" / "auditoria" / f"{_nome_arq(q['uid'])}.json"
                a = read_json(aud) if aud.exists() and q["pergunta"] else None
                sel = self._recuperar(q["item"], q["pergunta"] + " " + q["resposta"]) if q["pergunta"] else []
                out.append({**q, "auditoria": a, "regua": [], "tipo": a["tipo_sugerido"] if a else None,
                            "blocos_contexto": [{"id": f"B{k}", "texto": b["texto"], "indice_documento": b["indice"]}
                                                for k, b in enumerate(sel, 1)],
                            "fonte_texto": "\n".join(b["texto"] for b in sel)})
            return out
        out = []
        for v in self.vagas:
            ds = [d for t in range(1, TENTATIVAS + 1) if (d := self._estado(braco, v, t))]
            if not ds:
                continue
            fim = next((d for d in ds if not d["regua"] and d["auditoria"] and d["auditoria"]["aprovada"]), ds[-1])
            q = fim["questao"] or {}
            jan, _, _ = self._janela(v)
            out.append({"uid": f"{braco}:{v['vaga']}", "braco": braco, "vaga": v["vaga"], "item": v["item"],
                        "tipo": v["tipo"], "tentativa": fim["tentativa"], "tentativas": len(ds),
                        "pergunta": q.get("pergunta"), "resposta": q.get("resposta"), "conhecimento": q.get("conhecimento"),
                        "regua": fim["regua"], "auditoria": fim["auditoria"],
                        "blocos_contexto": [{"id": f"B{k}", "texto": b["texto"], "indice_documento": b["indice"]}
                                            for k, (_, b) in enumerate(jan, 1)],
                        "fonte_texto": "\n".join(b["texto"] for _, b in jan)})
        return out

    @staticmethod
    def aprovada_auditor(q: dict) -> bool:
        return bool(q.get("pergunta") and q.get("auditoria") and q["auditoria"]["aprovada"]
                    and len(str(q["resposta"]).split()) <= TETO_RESPOSTA)

    # -------------------------------------------------------------- sustentação e deduplicação
    def _arq_sust(self, q: dict) -> Path:
        return self.saida / "sustentacao" / f"{_nome_arq(q['uid'])}.json"

    def sustentar(self, qs: list[dict]) -> int:
        def um(q):
            arq = self._arq_sust(q)
            if arq.exists():
                return True
            nome = "sustentacao_" + _nome_arq(q["uid"])
            bmap = {b["id"]: b["texto"] for b in q["blocos_contexto"]}
            try:
                d = self.cliente("sustentacao").json(
                    C.prompt_gap("faithfulness"), json.dumps(dict(pergunta=q["pergunta"], gabarito=q["resposta"],
                                                                 blocos=q["blocos_contexto"]), ensure_ascii=False),
                    tag="ablacao_faithfulness", max_tokens=12000, item=q["item"],
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
        return self._paralelo([q for q in qs if not self._arq_sust(q).exists()], um, "sustentação")

    def sustentada(self, q: dict) -> bool:
        arq = self._arq_sust(q)
        return arq.exists() and read_json(arq)["status"] == "totalmente_sustentado"

    def _dedup(self, braco: str) -> DedupIncremental:
        from .geracao import _Preguicoso
        return DedupIncremental(self.saida / braco / "dedup", self.embedder, self.media, self.cal["limiar_auto"],
                                self.cal["limiar_juiz"], _Preguicoso(lambda: self.cliente("dedup_juiz")),
                                progress=self.progress)

    def deduplicar(self, braco: str, qs: list[dict]) -> tuple[int, dict]:
        dd, falhas, red = self._dedup(braco), 0, {}
        por_item = defaultdict(list)
        for q in qs:
            por_item[q["item"]].append({**q, "conhecimento": q.get("conhecimento") or q["pergunta"],
                                        "explicacao": q.get("explicacao", "")})
        for item, lst in sorted(por_item.items()):
            falhas += dd.processar(item, lst, falha=self._falha, ok=self._ok)
            red.update(dd.redundantes(item))
        return falhas, red

    # -------------------------------------------------------------- execução
    def executar(self) -> int:
        falhas = 0
        if "naive" in self.bracos:
            falhas += self.naive()
        doc = [b for b in ("documento", "sem_retro", "sem_externos", "completo") if b in self.bracos]
        falhas += self.documento(doc)
        finais = {b: self.finais(b) for b in self.bracos}
        falhas += self.sustentar([q for b in self.bracos for q in finais[b] if self.aprovada_auditor(q)])
        for b in self.bracos:
            sust = [q for q in finais[b] if self.aprovada_auditor(q) and self.sustentada(q)]
            f, red = self.deduplicar(b, sust)
            falhas += f
            for q in finais[b]:
                q["sustentada"] = self.aprovada_auditor(q) and self.sustentada(q)
                decidida = (self.saida / b / "dedup" / q["item"] / (q["uid"].replace(":", "_") + ".json")).exists()
                q["redundante"] = q["uid"] in red
                q["aceita"] = bool(q["sustentada"] and decidida and not q["redundante"])
            C.gravar_jsonl(self.saida / f"questoes_{b}.jsonl", finais[b])
        if falhas:
            self.progress(f"[ablação] {falhas} unidades com falha (em {C.relativo(self.saida / 'falhas')}); repita o "
                          "mesmo comando", flush=True)
            return 2
        self.relatorio(finais)
        return 0

    # -------------------------------------------------------------- relatório
    def _referencia(self) -> list[dict]:
        out = []
        for v in self.vagas:
            jan, _, _ = self._janela(v)
            out.append({"uid": v["ref_uid"], "item": v["item"], "tipo": v["tipo"], "pergunta": v["ref_pergunta"],
                        "resposta": v["ref_resposta"], "fonte_texto": "\n".join(b["texto"] for _, b in jan)})
        return out

    def relatorio(self, finais: dict | None = None) -> dict:
        finais = finais or {b: C.linhas(self.saida / f"questoes_{b}.jsonl") for b in self.bracos
                            if (self.saida / f"questoes_{b}.jsonl").exists()}
        todos = {i: blocos(i, self.docs_dir)[1] for i in sorted({p.name for p in self.docs_dir.iterdir()
                                                                  if (p / "documento.json").exists()})}
        df = Counter(t for bs in todos.values() for t in {t for b in bs for t in conteudo(b["texto"])})
        try:
            emb = self.embedder
            emb.encode(["teste"])
        except Exception as exc:  # noqa: BLE001 - sem embeddings, as métricas lexicais continuam
            self.progress(f"[ablação] embeddings indisponíveis ({type(exc).__name__}); sem diversidade semântica",
                          flush=True)
            emb = None
        res = {"n_vagas": self.n, "bracos": {}, "pareados": {}}
        aceitas = {b: [q for q in qs if q.get("aceita")] for b, qs in finais.items()}
        ref = self._referencia()
        m_ger = min([len([q for q in qs if q.get("pergunta")]) for qs in finais.values()] + [len(ref)])
        # rarefação das aceitas: o menor conjunto com pelo menos 50 questões (um braço menor fica com o próprio n)
        m_ac = min([len(v) for v in aceitas.values() if len(v) >= 50] or [50])
        for b, qs in finais.items():
            n = self.n
            ger = [q for q in qs if q.get("pergunta")]
            aud = [q for q in qs if self.aprovada_auditor(q)]
            sus = [q for q in qs if q.get("sustentada")]
            ac = aceitas[b]
            r = {"pedidas": n, "geradas": len(ger), "aprovadas_auditor": len(aud), "sustentadas": len(sus),
                 "aceitas": len(ac), "taxa_aceite": 100 * len(ac) / n, "ic95": wilson(len(ac), n),
                 "motivos_auditor": dict(Counter(q["auditoria"]["motivo"] for q in qs if q.get("auditoria")
                                                 and not q["auditoria"]["aprovada"])),
                 "regua_ok": sum(not q["regua"] for q in ger),
                 "aceitas_por_tentativa": dict(sorted(Counter(q["tentativa"] for q in ac).items())),
                 "aceitas_por_tipo": dict(sorted(Counter(q["tipo"] or "?" for q in ac).items())),
                 "vocabulario_geradas": vocabulario(ger, m_ger, df, len(todos), emb),
                 "vocabulario_aceitas": vocabulario(ac, m_ac, df, len(todos), emb)}
            if b == "naive":
                criterio = ("sem_documento", "alternativa_excluida", "elemento_unico")
                r["validas_sem_exigir_fonte"] = sum(
                    1 for q in ger if q.get("auditoria") and all(q["auditoria"].get(k) for k in criterio)
                    and not q["auditoria"].get("atalho") and len(q["resposta"].split()) <= TETO_RESPOSTA)
            else:
                r["tipo_confere"] = sum(1 for q in aud if q["auditoria"].get("tipo_confere"))
            res["bracos"][b] = r
        res["referencia_banco"] = {"vocabulario": vocabulario(ref, m_ger, df, len(todos), emb),
                                   "vocabulario_rarefeito_aceitas": vocabulario(ref, m_ac, df, len(todos), emb)}
        pares = (("completo", "sem_retro"), ("sem_externos", "documento"), ("completo", "sem_externos"),
                 ("sem_retro", "documento"))
        for a, b in pares:
            if a in finais and b in finais:
                va = {q["vaga"]: bool(q.get("aceita")) for q in finais[a]}
                vb = {q["vaga"]: bool(q.get("aceita")) for q in finais[b]}
                ks = sorted(set(va) & set(vb))
                res["pareados"][f"{a}_vs_{b}"] = mcnemar([va[k] for k in ks], [vb[k] for k in ks])
        res["observacional_banco"] = observacional(self.banco)
        atomic_json(self.saida / "resultado.json", res)
        (self.saida / "ABLACAO.md").write_text(markdown(res), encoding="utf-8")
        return res


def observacional(banco: Path = BANCO) -> dict:
    """No banco final: questões aceitas na 1ª visita do foco x nas revisitas (retroalimentação e exemplos novos)."""
    c = Counter({k: 0 for k in ("primeira_visita", "revisitas", "composta_1a_tentativa", "composta_2a_tentativa")})
    for q in C.linhas(banco):
        p = q["uid"].split(":")
        if p[2] == "j":
            c["primeira_visita" if p[3] == "r1" else "revisitas"] += 1
        else:
            c["composta_2a_tentativa" if ":t2" in q["uid"] else "composta_1a_tentativa"] += 1
    tot = sum(c.values())
    return {**c, "total": tot,
            "pct_vindas_de_retroalimentacao": 100 * (c["revisitas"] + c["composta_2a_tentativa"]) / max(1, tot)}


def _f(x, casas=1):
    return "-" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{casas}f}".replace(".", ",")


def markdown(r: dict) -> str:
    bs = list(r["bracos"])
    out = ["# Ablação da geração de questões", "",
           f"{r['n_vagas']} vagas (documento, bloco foco, tipo) sorteadas do banco final v1; cada braço gera uma questão "
           "por vaga (o naive, o mesmo número por tópico). Aceita = auditor v23 + resposta de até 20 palavras + "
           "sustentação total + não redundante dentro do braço.", "",
           "## Taxa de aceite", "", "| Braço | Geradas | Auditor | Sustentadas | Aceitas | Taxa (IC 95%) |",
           "|---|---|---|---|---|---|"]
    for b in bs:
        x = r["bracos"][b]
        out.append(f"| {NOME_BRACO[b]} | {x['geradas']} | {x['aprovadas_auditor']} | {x['sustentadas']} | {x['aceitas']} | "
                   f"{_f(x['taxa_aceite'])}% ({_f(x['ic95'][0])}–{_f(x['ic95'][1])}) |")
    if "naive" in r["bracos"]:
        out += ["", f"Naive sem exigir a fonte (auditor sem a verificação de sustentação): "
                    f"{r['bracos']['naive']['validas_sem_exigir_fonte']} válidas."]
    out += ["", "Aceitas por tentativa (ganho da retroalimentação nas mesmas vagas):", ""]
    for b in bs:
        out.append(f"- {NOME_BRACO[b]}: {r['bracos'][b]['aceitas_por_tentativa']}")
    if r["pareados"]:
        out += ["", "| Comparação pareada (McNemar exato) | Só o 1º aceita | Só o 2º aceita | p |", "|---|---|---|---|"]
        for k, v in r["pareados"].items():
            a, b = k.split("_vs_")
            out.append(f"| {NOME_BRACO[a]} x {NOME_BRACO[b]} | {v['so_primeiro']} | {v['so_segundo']} | {v['p']:.3g} |")
    out += ["", "Motivos de recusa do auditor:", ""]
    for b in bs:
        out.append(f"- {NOME_BRACO[b]}: {r['bracos'][b]['motivos_auditor']}")
    metr = [("distinct_1", "Distinct-1", 3), ("distinct_2", "Distinct-2", 3), ("vocabulario_conteudo", "Vocabulário (palavras de conteúdo)", 0),
            ("termos_especializados", "Termos especializados", 0), ("fracao_tokens_especializados", "Fração de tokens especializados", 3),
            ("mattr", "MATTR (50)", 3), ("mtld", "MTLD", 1), ("self_bleu_por_topico", "Self-BLEU por tópico (menor = mais variado)", 3),
            ("cosseno_medio_por_topico", "Cosseno médio por tópico (menor = mais variado)", 3),
            ("vendi_relativo_por_topico", "Vendi relativo por tópico", 3), ("aberturas_distintas", "Aberturas distintas", 3),
            ("abertura_cliche", "Abertura \"Em um/Num/Após...\"", 3), ("copia_3gramas_do_documento", "Trigramas copiados do documento", 3),
            ("palavras_pergunta", "Palavras na pergunta", 1), ("palavras_resposta", "Palavras na resposta", 1)]
    for chave, titulo, ref in (("vocabulario_aceitas", "aceitas", "vocabulario_rarefeito_aceitas"),
                               ("vocabulario_geradas", "todas as geradas", "vocabulario")):
        out += ["", f"## Vocabulário e diversidade: {titulo}", "",
                "Distinct, vocabulário, termos especializados e aberturas: rarefeitos ao mesmo número de questões "
                "(média de 30 sorteios). Termos especializados: "
                "palavras de conteúdo que aparecem em até 1/4 dos 40 documentos.", "",
                "| Métrica | " + " | ".join(NOME_BRACO[b] for b in bs) + " | Banco |", "|---|" + "---|" * (len(bs) + 1)]
        out.append("| Questões no conjunto | " + " | ".join(str(r["bracos"][b][chave].get("n", 0)) for b in bs)
                   + f" | {r['referencia_banco'][ref].get('n', 0)} |")
        out.append("| Rarefeito a | " + " | ".join(str(r["bracos"][b][chave].get("m_rarefeito", "-")) for b in bs)
                   + f" | {r['referencia_banco'][ref].get('m_rarefeito', '-')} |")
        for k, nome, c in metr:
            out.append(f"| {nome} | " + " | ".join(_f(r["bracos"][b][chave].get(k), c) for b in bs)
                       + f" | {_f(r['referencia_banco'][ref].get(k), c)} |")
    o = r["observacional_banco"]
    out += ["", "## Observacional: banco final v1", "",
            f"{o['revisitas']} questões do banco vieram de revisitas do foco e {o.get('composta_2a_tentativa', 0)} da "
            f"2ª tentativa de compostas: {_f(o['pct_vindas_de_retroalimentacao'])}% das {o['total']} (a revisita "
            "também troca os exemplos de forma, então mede retroalimentação e exemplos juntos)."]
    return "\n".join(out) + "\n"
