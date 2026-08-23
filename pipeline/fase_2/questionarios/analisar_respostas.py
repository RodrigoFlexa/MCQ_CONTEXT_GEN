#!/usr/bin/env python3
"""Agrega as respostas do formulário comparativo e decodifica A/B.

Lê o CSV exportado do Google Forms e o mapa interno (que guarda qual
condição ocupou a posição A em cada par), e reporta:

  - preferência por condição, no agregado e por avaliador;
  - teste binomial bilateral sobre os pares decididos (empates excluídos);
  - preferência por POSIÇÃO, que é o confundidor a descartar antes de ler
    qualquer diferença entre condições como efeito do método;
  - concordância entre avaliadores nos pares que ambos decidiram.

    python analisar_respostas.py [respostas.csv]
"""
import csv
import re
import sys
from collections import Counter, defaultdict
from math import comb
from pathlib import Path

CSV_RESP = Path(sys.argv[1] if len(sys.argv) > 1 else
                "Avaliação Comparativa de Questões (respostas) - "
                "Respostas ao formulário 1.csv")
CSV_MAPA = Path("mcq_output/mapa_avaliacao_comparativa_v2.csv")

CTX, INS, EMP = "context-grounded", "instruction-only", "empate"


def binom_2sided(k, n):
    """p-valor bilateral do teste de sinais (H0: p=0.5)."""
    if n == 0:
        return 1.0
    k = max(k, n - k)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n)


mapa = {int(r["pair_id"]): r for r in
        csv.DictReader(open(CSV_MAPA, encoding="utf-8-sig"))}
respostas = list(csv.DictReader(open(CSV_RESP, encoding="utf-8-sig")))

# escolhas[avaliador][pair_id] = (posicao, condicao)
escolhas = {}
justificativas = defaultdict(Counter)
for r in respostas:
    nome = r.get("Nome do avaliador", "?").strip()
    d = {}
    for k, v in r.items():
        m = re.match(r"^(\d+)\.1 ", k or "")
        if not m or not v:
            continue
        pid = int(m.group(1))
        mp = mapa[pid]
        if v.startswith("Opção A"):
            d[pid] = ("A", mp["opcao_A_condition"])
        elif v.startswith("Opção B"):
            d[pid] = ("B", mp["opcao_B_condition"])
        else:
            d[pid] = (None, EMP)
        for j in (r.get(f"{pid}.2 Justifique sua escolha", "") or "").split(", "):
            if j:
                justificativas[d[pid][1]][j] += 1
    escolhas[nome] = d

print(f"{len(respostas)} avaliador(es) · {len(mapa)} pares\n")

# ------------------------------------------------------- por avaliador ---
print(f"{'avaliador':<18}{'ctx':>5}{'ins':>5}{'emp':>5}{'decid.':>8}"
      f"{'p':>8}{'  posição A/B':>14}")
for nome, d in escolhas.items():
    c = Counter(cond for _, cond in d.values())
    pos = Counter(p for p, _ in d.values() if p)
    n = c[CTX] + c[INS]
    print(f"{nome:<18}{c[CTX]:>5}{c[INS]:>5}{c[EMP]:>5}{n:>8}"
          f"{binom_2sided(c[CTX], n):>8.3f}"
          f"{f'{pos[chr(65)]}/{pos[chr(66)]}':>14}")

# ----------------------------------------------------------- agregado ---
tot = Counter()
pos_tot = Counter()
for d in escolhas.values():
    for p, cond in d.values():
        tot[cond] += 1
        if p:
            pos_tot[p] += 1
n_dec = tot[CTX] + tot[INS]
n_all = sum(tot.values())

print(f"\n{'AGREGADO':<18}{tot[CTX]:>5}{tot[INS]:>5}{tot[EMP]:>5}{n_dec:>8}"
      f"{binom_2sided(tot[CTX], n_dec):>8.3f}"
      f"{f'{pos_tot[chr(65)]}/{pos_tot[chr(66)]}':>14}")
print(f"\n  empates: {tot[EMP]}/{n_all} ({100*tot[EMP]/n_all:.0f}%)")
print(f"  viés de posição (H0: sem preferência A/B): "
      f"p={binom_2sided(pos_tot['A'], sum(pos_tot.values())):.3f}")

# cruzamento posição × condição: separa efeito do método de viés posicional
cross = Counter()
for d in escolhas.values():
    for p, cond in d.values():
        if p:
            cross[(p, cond)] += 1
print("\n  posição escolhida × condição vencedora:")
print(f"    {'':<4}{'ctx':>5}{'ins':>5}")
for p in "AB":
    print(f"    {p:<4}{cross[(p, CTX)]:>5}{cross[(p, INS)]:>5}")

# ------------------------------------------------------- por assunto ---
por_assunto = defaultdict(Counter)
for d in escolhas.values():
    for pid, (_, cond) in d.items():
        por_assunto[mapa[pid]["topic"]][cond] += 1
print(f"\n{'por assunto':<30}{'ctx':>5}{'ins':>5}{'emp':>5}")
for t, c in sorted(por_assunto.items()):
    print(f"  {t:<28}{c[CTX]:>5}{c[INS]:>5}{c[EMP]:>5}")

# --------------------------------------------------- concordância ---
nomes = list(escolhas)
if len(nomes) >= 2:
    print("\nconcordância entre avaliadores:")
    for i in range(len(nomes)):
        for j in range(i + 1, len(nomes)):
            a, b = escolhas[nomes[i]], escolhas[nomes[j]]
            comuns = set(a) & set(b)
            ig = sum(1 for p in comuns if a[p][1] == b[p][1])
            # só onde AMBOS decidiram (empate não informa direção)
            dec = [p for p in comuns if a[p][1] != EMP and b[p][1] != EMP]
            ig_dec = sum(1 for p in dec if a[p][1] == b[p][1])
            print(f"  {nomes[i]} × {nomes[j]}: "
                  f"{ig}/{len(comuns)} idênticas ({100*ig/max(len(comuns),1):.0f}%) · "
                  f"nos {len(dec)} decididos por ambos: {ig_dec} "
                  f"({100*ig_dec/max(len(dec),1):.0f}%)")

# ------------------------------------------------------ justificativas ---
print("\njustificativas mais citadas por condição vencedora:")
for cond in (CTX, INS, EMP):
    top = justificativas[cond].most_common(4)
    if top:
        print(f"  {cond}:")
        for j, n in top:
            print(f"     {n:>3}x  {j[:66]}")
