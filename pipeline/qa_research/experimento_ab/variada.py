"""Geração variada: conceito, mecanismo e consequência, com exemplos de forma que mudam a cada visita.

Motivação: as questões da v23 têm a mesma cara (cenário longo, abertura "Em um...", exemplos fixos dominando o prompt)
e o banco tem poucas questões de conceito, mecanismo e consequência novas. Aqui:
  - não há exemplos bons fixos: só os defeitos (as 9 ruins da v23) ficam no prompt de sistema;
  - cada foco é visitado até 4 vezes. Nas visitas 1 a 3, o prompt traz 8 pares de pergunta e resposta de datasets
    externos (Pirá, MMMLU PT-BR, ARC-Challenge e QASC, já limpos e revisados em pipeline/qa_references/data), sorteados
    por documento, foco e visita; na visita 4, 6 questões do dataset de múltipla escolha convertido para QA e
    aprovado (relatorios/especialista_revisadas_v3, gabarito de até 15 palavras, de outros documentos);
  - o foco só fecha antes da 4ª visita se o gerador disser que não há mais nada (lista vazia);
  - sem compostas nem inventário. Régua, auditor v23, deduplicação calibrada e retomada são os da v23.
"""
from __future__ import annotations

import hashlib
import random
import re
from pathlib import Path

from pipeline.inventario.textutil import read_json

from . import comum as C
from .v23 import GeracaoV23

EXTERNOS_REVISADOS = C.ROOT / "pipeline" / "qa_references" / "data" / "qa_examples_revisados.jsonl"
EXTERNOS_LIMPOS = C.ROOT / "pipeline" / "qa_references" / "data" / "qa_examples_limpos.jsonl"
CONVERTIDAS = C.QA / "relatorios" / "especialista_revisadas_v3" / "aprovadas.jsonl"
MISTURA = {"pira_ptbr": 3, "mmmlu_ptbr": 2, "arc_challenge": 2, "qasc": 1}
N_CONVERTIDAS = 6
VISITAS_EXTERNOS = 3          # visitas 1..3 com externos; a seguinte, com as convertidas
TETO_RESPOSTA_CONVERTIDA = 15
# enunciados que dependem de algo fora deles ("no cenário descrito") não servem de exemplo
DEPENDE = re.compile(r"cen[aá]rio descrito|descrit[oa] acima|situa[cç][aã]o descrita|no texto|do texto|conforme o texto",
                     re.I)
COMANDO_PREPARAR = "python -m pipeline.qa_references.preparar_exemplos --revisao-llm"


def _rng(*partes) -> random.Random:
    return random.Random(int(hashlib.sha256("|".join(map(str, partes)).encode()).hexdigest()[:16], 16))


def carregar_externos(caminho: Path | None = None) -> tuple[dict, Path]:
    caminho = Path(caminho) if caminho else (EXTERNOS_REVISADOS if EXTERNOS_REVISADOS.exists() else EXTERNOS_LIMPOS)
    if not caminho.exists():
        raise ValueError(f"Exemplos externos ausentes em {C.relativo(caminho)}. No servidor, rode antes:\n  {COMANDO_PREPARAR}")
    pools: dict = {f: [] for f in MISTURA}
    for r in C.linhas(caminho):
        if r.get("source") in pools and r.get("question") and r.get("answer"):
            pools[r["source"]].append({"id": r["id"], "pergunta": r["question"].strip(), "resposta": r["answer"].strip()})
    if not any(pools.values()):
        raise ValueError(f"{C.relativo(caminho)} não tem exemplos de {', '.join(MISTURA)}")
    for v in pools.values():
        v.sort(key=lambda r: r["id"])
    return pools, caminho


def carregar_convertidas(caminho: Path = CONVERTIDAS) -> list[dict]:
    if not Path(caminho).exists():
        raise ValueError(f"Questões convertidas do dataset de múltipla escolha ausentes em {C.relativo(Path(caminho))}")
    out = [{"id": q["uid"], "item": q.get("item"), "tipo": q["tipo"], "pergunta": q["pergunta"], "resposta": q["resposta"]}
           for q in C.linhas(Path(caminho))
           if q.get("aprovada", True) and len(q["resposta"].split()) <= TETO_RESPOSTA_CONVERTIDA
           and not DEPENDE.search(q["pergunta"])]
    if not out:
        raise ValueError(f"{C.relativo(Path(caminho))} sem questões convertidas com gabarito curto")
    return sorted(out, key=lambda q: q["id"])


def sortear_externos(pools: dict, item: str, foco: int, rodada: int) -> list[dict]:
    rng = _rng("externos", item, foco, rodada)
    disponiveis = [f for f in MISTURA if pools.get(f)]
    plano = [f for f, n in MISTURA.items() for _ in range(n)]
    out, vistos = [], set()
    for k, fonte in enumerate(plano):
        fonte = fonte if pools.get(fonte) else disponiveis[k % len(disponiveis)]
        opcoes = [r for r in pools[fonte] if r["id"] not in vistos] or pools[fonte]
        r = rng.choice(opcoes)
        vistos.add(r["id"])
        out.append(r)
    rng.shuffle(out)
    return out


def sortear_convertidas(banco: list, item: str, foco: int, tipos: tuple, n: int = N_CONVERTIDAS) -> list[dict]:
    """De outros documentos; metade (ou mais) dos tipos desta geração, quando houver."""
    rng = _rng("convertidas", item, foco)
    outros = [q for q in banco if q["item"] != item] or banco
    alvo = [q for q in outros if q["tipo"] in tipos]
    resto = [q for q in outros if q["tipo"] not in tipos]
    escolha = rng.sample(alvo, min(len(alvo), (n + 1) // 2 + 1))
    escolha += rng.sample(resto, min(len(resto), n - len(escolha)))
    if len(escolha) < n:
        sobra = [q for q in outros if q not in escolha]
        escolha += rng.sample(sobra, min(len(sobra), n - len(escolha)))
    rng.shuffle(escolha)
    return escolha


def bloco_forma(exemplos: list) -> str:
    pares = "\n\n".join(f"Pergunta: {e['pergunta']}\nResposta: {e['resposta']}" for e in exemplos)
    return f"<exemplos_de_forma>\n{pares}\n</exemplos_de_forma>"


def bloco_ruins(ruins: list) -> str:
    return "<questoes_ruins>\n" + "\n\n".join(
        f"[{e['tipo']}] Pergunta: {e['pergunta']}\nResposta: {e['resposta']}\nDefeito: {e['defeito']}" for e in ruins
    ) + "\n</questoes_ruins>"


class GeracaoVariada(GeracaoV23):
    VERSAO = "v23var"
    TIPOS_FOCO = ("conceito", "mecanismo", "consequencia")
    COMPOSTAS = False
    VISITAS = VISITAS_EXTERNOS + 1

    def __init__(self, *a, externos: Path | None = None, convertidas: Path = CONVERTIDAS, saturacao=None, **kw):
        sat = {"max_rodadas": self.VISITAS, "paciencia": self.VISITAS, **(saturacao or {})}
        sat["max_rodadas"] = min(sat["max_rodadas"], self.VISITAS)
        self.pools, self.arq_externos = carregar_externos(externos)
        self.arq_convertidas = Path(convertidas)
        self.convertidas = carregar_convertidas(self.arq_convertidas)
        super().__init__(*a, saturacao=sat, **kw)

    def prompt_nome(self, papel: str) -> str:
        return {"foco": "foco_v23var", "auditoria": "auditoria_v23"}.get(papel, "composta_v23")

    def extra_config(self) -> dict:
        return {**super().extra_config(), "externos_sha256": C.sha(self.arq_externos.read_text(encoding="utf-8")),
                "convertidas_sha256": C.sha(self.arq_convertidas.read_text(encoding="utf-8")),
                "mistura_externos": MISTURA, "visitas_externos": VISITAS_EXTERNOS, "n_convertidas": N_CONVERTIDAS}

    def inventario(self) -> int:
        return 0

    def sistema(self, papel: str, item: str) -> str:
        base = super(GeracaoV23, self).sistema(papel, item)       # sem as boas fixas da v23
        if papel != "foco":
            return base
        return base + "\n\n" + bloco_ruins([e for e in self.banco_v23["ruins"] if e["item"] != item])

    def _exemplos(self, item: str, semente: str, composta: bool) -> str:
        _, foco, rodada = semente.split(":")
        foco, rodada = int(foco), int(rodada.lstrip("r"))
        if rodada <= VISITAS_EXTERNOS:
            return bloco_forma(sortear_externos(self.pools, item, foco, rodada))
        return bloco_forma(sortear_convertidas(self.convertidas, item, foco, self.TIPOS_FOCO))

    def focos_abertos(self, item: str, rodada: int) -> list[int]:
        """Até 4 visitas por foco; fecha antes só quando o gerador devolve zero questões."""
        if rodada == 1:
            return list(range(len(self.docs[item])))
        vis, out = self._visitas(item), []
        for f in range(len(self.docs[item])):
            v = [r for r in vis.get(f, []) if r < rodada]
            if not v or v[-1] != rodada - 1 or len(v) >= self.sat["max_rodadas"]:
                continue
            if not self._completo(item, rodada - 1, f):
                continue
            if read_json(self._arq_foco(item, rodada - 1, f))["questoes"]:
                out.append(f)
        return out

