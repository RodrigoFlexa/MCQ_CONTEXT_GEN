"""Exemplos de forma para o experimento de condições A, B, C e D.

A: sem exemplos.
B: 3 exemplos de datasets externos, um por dificuldade, de fontes diferentes:
   fácil = Pirá (português), média = ARC-Challenge, difícil = HotpotQA.
C: 3 questões aprovadas sem ressalvas pelo especialista, uma por dificuldade, todas de áreas
   diferentes entre si e diferentes da área da janela.
D: B + C (6 exemplos).

A dificuldade nunca é informada ao modelo e a ordem é embaralhada. O sorteio é determinístico por
janela: B e D recebem os mesmos externos; C e D, as mesmas questões do especialista.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
from pathlib import Path

from .core import QA, ROOT

CONDICOES = ("A", "B", "C", "D")
EXTERNOS = ROOT / "pipeline" / "qa_references" / "data" / "qa_examples.jsonl"
ESPECIALISTA = QA / "repositorio_definitivo" / "questoes.jsonl"
FONTE_POR_DIFICULDADE = {"facil": "pira_ptbr", "media": "arc_challenge", "dificil": "hotpotqa"}
COMANDO_DOWNLOAD = ("python pipeline/qa_references/download_qa_examples.py "
                    "--only pira_ptbr arc_challenge hotpotqa --max-per-dataset 1000")
CABECALHO = ("Os pares abaixo mostram apenas a forma de perguntas e de respostas curtas. São de outros "
             "assuntos e não servem como fonte de conhecimento. Não copie assunto, cenário, estrutura "
             "nem vocabulário.")
SIM_NAO = re.compile(r"^(yes|no|sim|não|nao)\.?$", re.I)


def _rng(*partes) -> random.Random:
    return random.Random(int(hashlib.sha256("|".join(map(str, partes)).encode()).hexdigest()[:16], 16))


def carregar_externos(caminho: Path = EXTERNOS) -> dict[str, list[dict]]:
    if not caminho.exists():
        raise FileNotFoundError(f"Exemplos externos ausentes em {caminho}. No servidor, rode:\n  {COMANDO_DOWNLOAD}")
    pools: dict[str, list[dict]] = {f: [] for f in FONTE_POR_DIFICULDADE.values()}
    with caminho.open(encoding="utf-8") as f:
        for linha in f:
            r = json.loads(linha)
            fonte = r["id"].split(":", 1)[0]
            if fonte not in pools:
                continue
            q, a = r["question"].strip(), r["answer"].strip()
            if SIM_NAO.match(a) or len(a.split()) > 50 or len(q.split()) < 4:
                continue
            pools[fonte].append({"id": r["id"], "fonte": fonte, "pergunta": q, "resposta": a,
                                 "licenca": r.get("source_license", "")})
    vazias = [f for f, v in pools.items() if not v]
    if vazias:
        raise ValueError(f"Sem exemplos externos utilizáveis para {', '.join(vazias)}. Rode:\n  {COMANDO_DOWNLOAD}")
    for v in pools.values():
        v.sort(key=lambda r: r["id"])
    return pools


def carregar_especialista(caminho: Path = ESPECIALISTA) -> list[dict]:
    out = []
    with caminho.open(encoding="utf-8") as f:
        for linha in f:
            r = json.loads(linha)
            if r["status"] == "aprovada":
                out.append({"id": r["id"], "fonte": "especialista", "area_id": r["area_id"], "item": r["item"],
                            "dificuldade": r["dificuldade"], "pergunta": r["pergunta"], "resposta": r["resposta"]})
    return sorted(out, key=lambda r: r["id"])


def sortear_externos(pools: dict, item: str, foco: int) -> list[dict]:
    rng = _rng("externos", item, foco)
    return [{**rng.choice(pools[fonte]), "dificuldade": dif} for dif, fonte in FONTE_POR_DIFICULDADE.items()]


def sortear_especialista(banco: list[dict], item: str, foco: int) -> list[dict]:
    """Uma por dificuldade, com áreas distintas entre si e da área da janela."""
    rng = _rng("especialista", item, foco)
    area_janela = item[:2]
    por_dif = {d: [r for r in banco if r["dificuldade"] == d and r["area_id"] != area_janela]
               for d in ("facil", "media", "dificil")}
    for tentativa in range(200):
        escolha, areas = [], set()
        # Começa pela dificuldade com menos opções para não esgotar áreas.
        for d in sorted(por_dif, key=lambda d: len(por_dif[d])):
            opcoes = [r for r in por_dif[d] if r["area_id"] not in areas]
            if not opcoes:
                break
            r = rng.choice(opcoes)
            escolha.append(r)
            areas.add(r["area_id"])
        if len(escolha) == 3:
            return escolha
    raise ValueError(f"{item}: não há questões aprovadas suficientes em áreas distintas")


def exemplos_da_janela(condicao: str, item: str, foco: int, externos=None, especialista=None) -> list[dict]:
    if condicao not in CONDICOES:
        raise ValueError(f"Condição desconhecida: {condicao}")
    lista = []
    if condicao in ("B", "D"):
        lista += sortear_externos(externos, item, foco)
    if condicao in ("C", "D"):
        lista += sortear_especialista(especialista, item, foco)
    _rng("ordem", condicao, item, foco).shuffle(lista)
    return lista


def render(lista: list[dict]) -> str:
    if not lista:
        return ""
    pares = "\n\n".join(f"Pergunta: {e['pergunta']}\nResposta: {e['resposta']}" for e in lista)
    return f"<exemplos_de_forma>\n{CABECALHO}\n\n{pares}\n</exemplos_de_forma>"
