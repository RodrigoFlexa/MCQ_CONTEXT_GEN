import csv
from pathlib import Path

OUT_DIR = Path("mcq_output")
SRC = OUT_DIR / "selecao_questoes.csv"
DST = OUT_DIR / "questionario_final_30.csv"

TARGET_SNIPPET = "Considerando a aplicação da norma API 521:2007"

with open(SRC, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

idx = next(i for i, r in enumerate(rows) if TARGET_SNIPPET in r["stem"])
norma_q = rows.pop(idx)
rows.insert(0, norma_q)

assert len(rows) == 30

out_fields = ["numero_questao"] + fieldnames
with open(DST, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=out_fields)
    writer.writeheader()
    for n, r in enumerate(rows, start=1):
        row = {"numero_questao": n}
        row.update(r)
        writer.writerow(row)

print(f"Salvo: {DST}")
print(f"Questão 1 (movida para o topo): {norma_q['stem'][:100]}...")
print(f"Condição: {norma_q['condition']} | Tópico: {norma_q['topic']} | Dificuldade: {norma_q['difficulty']} | Gabarito: {norma_q['gabarito']}")
