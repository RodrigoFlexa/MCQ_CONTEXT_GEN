"""
seed_fase3.py — banco seed de questões, derivado do formulário da fase 2.

Na fase 2, 30 pares de questões (uma *context-grounded*, uma *instruction-only*)
foram submetidos a especialistas do domínio, que escolheram a melhor de cada par
justificando por: clareza do enunciado, qualidade das alternativas, correção
técnica e relevância para a operação de FPSOs.

As vencedoras viram o banco seed da fase 3: são elas que servem de few-shot nas
primeiras rodadas de geração, até que questões aprovadas pelo próprio pipeline
tomem o lugar delas (passo 8).

Regra de seleção (parametrizável em `construir_banco_seed`):

    nota_humana = (votos_vencedor - votos_perdedor) / n_avaliadores

Com 2 avaliadores: 1,0 = unânime, 0,5 = decidida por um voto. Empates e pares
sem voto ficam de fora. O default `min_nota_humana=0.5` aproveita todos os pares
com vencedor claro.

Arquivos de entrada (pasta `pipeline/fase_2/questionarios/respostas_questionario/`):
    pares_questoes_do_formulario.jsonl  — as 30 duplas completas, por pair_id
    mapa_origem_das_questoes_do_formulario.csv — qual condição ocupou A e B
    respostas_formulario.csv            — export do Google Forms
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

CTX = "context-grounded"
INS = "instruction-only"
EMP = "empate"

_COL_ESCOLHA = re.compile(r"^(\d+)\.1 ")


def _ler_mapa(caminho: Path) -> dict[int, dict[str, str]]:
    with open(caminho, encoding="utf-8-sig") as f:
        return {int(r["pair_id"]): r for r in csv.DictReader(f)}


def _ler_pares(caminho: Path) -> dict[int, dict[str, Any]]:
    pares = {}
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            if linha.strip():
                p = json.loads(linha)
                pares[int(p["pair_id"])] = p
    return pares


def apurar_votos(caminho_respostas: Path,
                 caminho_mapa: Path) -> tuple[dict[int, Counter], int]:
    """Conta, por par, quantos avaliadores preferiram cada condição.

    Devolve `({pair_id: Counter({condicao: votos})}, n_avaliadores)`.
    """
    mapa = _ler_mapa(caminho_mapa)
    with open(caminho_respostas, encoding="utf-8-sig") as f:
        respostas = list(csv.DictReader(f))

    votos: dict[int, Counter] = {pid: Counter() for pid in mapa}
    for r in respostas:
        for coluna, valor in r.items():
            m = _COL_ESCOLHA.match(coluna or "")
            if not m or not valor:
                continue
            pid = int(m.group(1))
            if pid not in mapa:
                continue
            if valor.startswith("Opção A"):
                votos[pid][mapa[pid]["opcao_A_condition"]] += 1
            elif valor.startswith("Opção B"):
                votos[pid][mapa[pid]["opcao_B_condition"]] += 1
            else:
                votos[pid][EMP] += 1
    return votos, len(respostas)


def construir_banco_seed(dir_respostas: str | Path,
                         min_nota_humana: float = 0.5,
                         verbose: bool = True) -> list[dict[str, Any]]:
    """Monta o banco seed a partir dos artefatos da fase 2.

    Cada item devolvido tem o formato canônico de questão do pipeline
    (`stem`, `alternatives`, `correct_answer_index`, `correct_reason`,
    `difficulty`) mais a proveniência (`origem`, `nota`, `pair_id`, `condicao`).
    """
    dir_respostas = Path(dir_respostas)
    votos, n_avaliadores = apurar_votos(
        dir_respostas / "respostas_formulario.csv",
        dir_respostas / "mapa_origem_das_questoes_do_formulario.csv",
    )
    pares = _ler_pares(dir_respostas / "pares_questoes_do_formulario.jsonl")

    banco: list[dict[str, Any]] = []
    descartados = Counter()
    for pid, c in sorted(votos.items()):
        if c[CTX] == c[INS]:
            descartados["empate ou sem voto decisivo"] += 1
            continue
        vencedor, perdedor = (CTX, INS) if c[CTX] > c[INS] else (INS, CTX)
        nota = (c[vencedor] - c[perdedor]) / max(n_avaliadores, 1)
        if nota < min_nota_humana:
            descartados[f"nota < {min_nota_humana}"] += 1
            continue

        chave = "context_grounded" if vencedor == CTX else "instruction_only"
        q = dict(pares[pid][chave])
        banco.append({
            "id": f"seed-{pid:02d}",
            "stem": q["stem"],
            "alternatives": q["alternatives"],
            "correct_answer_index": int(q["correct_answer_index"]),
            "correct_reason": q.get("correct_reason", ""),
            "difficulty": q.get("difficulty", "media"),
            "topico": pares[pid].get("topic_name", ""),
            "subtopico": "",
            "origem": "seed_fase2",
            "condicao": vencedor,
            "pair_id": pid,
            "nota": round(nota, 3),
            "votos": {"vencedor": c[vencedor], "perdedor": c[perdedor],
                      "empate": c[EMP]},
        })

    if verbose:
        print(f"banco seed: {len(banco)} questões de {len(votos)} pares "
              f"({n_avaliadores} avaliadores)")
        por_cond = Counter(q["condicao"] for q in banco)
        print(f"  por condição: {dict(por_cond)}")
        por_nota = Counter(q["nota"] for q in banco)
        print(f"  por nota humana: {dict(sorted(por_nota.items(), reverse=True))}")
        for motivo, n in descartados.items():
            print(f"  descartados ({motivo}): {n}")
    return banco


def salvar_banco_seed(banco: list[dict[str, Any]], caminho: str | Path) -> Path:
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        for q in banco:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")
    return caminho


__all__ = ["construir_banco_seed", "salvar_banco_seed", "apurar_votos"]
