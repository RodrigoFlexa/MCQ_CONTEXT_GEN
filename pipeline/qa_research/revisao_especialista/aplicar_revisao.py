"""Aplica a revisão do especialista ao primeiro lote de questões e aos documentos.

Entradas (nesta pasta):
  respostas/*.xlsx          planilhas do Google Forms, uma por tópico principal
  edicoes_questoes.json     versões editadas das questões aprovadas com ressalvas
  edicoes_documentos.json   edições nos documentos de contexto (antes/depois)

Saídas:
  pareceres.json                                   pareceres consolidados das 60 questões
  ../repositorio_definitivo/questoes.jsonl|.csv    aprovadas + aprovadas com ressalvas editadas
  ../relatorios/dez_areas_final_v2/                documentos revisados (v1 permanece intacta)

Reprovadas não entram no repositório definitivo; ficam registradas apenas em
pareceres.json, como origem das edições nos documentos.

Uso, na raiz do repositório:
  python pipeline/qa_research/revisao_especialista/aplicar_revisao.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
QA = HERE.parent
ROOT = QA.parent.parent
V1 = QA / "relatorios" / "dez_areas_final_v1"
V2 = QA / "relatorios" / "dez_areas_final_v2"
REPO = QA / "repositorio_definitivo"
MAPA = QA / "formulario_especialista" / "mapa_questoes_formulario.csv"
SELECAO = QA / "formulario_especialista" / "selecao.json"
LOTE = "especialista_2026-10-21"

PARECERES = {"APROVADA": "aprovada", "APROVADA COM RESSALVAS": "aprovada_com_ressalvas",
             "REPROVADA": "reprovada"}


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def dump_crlf(path: Path, data) -> None:
    """Mesmo formato dos snapshots v1: indent 2, UTF-8 sem escape, CRLF, sem quebra final."""
    text = json.dumps(data, ensure_ascii=False, indent=2).replace("\n", "\r\n")
    path.write_bytes(text.encode("utf-8"))


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_bytes(text.encode("utf-8"))


# ---------------------------------------------------------------- pareceres
def ler_respostas() -> dict:
    out, pseudonimos = {}, {}
    for xlsx in sorted((HERE / "respostas").glob("*.xlsx")):
        ws = openpyxl.load_workbook(xlsx, read_only=True).worksheets[0]
        rows = [r for r in ws.iter_rows(values_only=True) if any(v not in (None, "") for v in r)]
        if len(rows) != 2:
            raise ValueError(f"{xlsx.name}: esperada exatamente uma resposta, há {len(rows) - 1}")
        header, row = rows
        meta = dict(zip(header, row))
        por_codigo: dict[str, dict] = {}
        for h, v in zip(header, row):
            m = re.match(r"(Q\d{3}) · (.+)", str(h or ""))
            if not m:
                continue
            campo = m.group(2)
            chave = ("parecer" if campo.startswith("Parecer") else
                     "motivos" if campo.startswith("Motivos") else
                     "comentario" if campo.startswith("Comentário") else None)
            if chave is None:
                raise ValueError(f"{xlsx.name}: coluna inesperada {h!r}")
            por_codigo.setdefault(m.group(1), {})[chave] = (str(v).strip() if v not in (None, "") else "")
        for codigo, d in por_codigo.items():
            if codigo in out:
                raise ValueError(f"{codigo} aparece em mais de uma planilha")
            if d.get("parecer") not in PARECERES:
                raise ValueError(f"{codigo}: parecer ausente ou inválido: {d.get('parecer')!r}")
            out[codigo] = {
                "parecer": PARECERES[d["parecer"]],
                "motivos": [s.strip() for s in d.get("motivos", "").split(",") if s.strip()],
                "comentario": d.get("comentario", ""),
                # Repositório público: o nome e o e-mail do avaliador não saem das planilhas locais.
                "avaliador": pseudonimos.setdefault(str(meta.get("E-mail", "")).strip().lower(),
                                                    f"especialista_{len(pseudonimos) + 1:02d}"),
                "data": str(meta.get("Carimbo de data/hora", "")),
                "planilha": f"respostas/{xlsx.name}",
            }
    return out


# ---------------------------------------------------------------- documentos
def render(doc: dict) -> str:
    """Mesmo layout de document/export.py."""
    lines = ["# " + doc["titulo"], ""]
    group = None
    for chapter in doc["capitulos"]:
        if chapter["grupo"] != group:
            group = chapter["grupo"]
            lines.extend(["## " + group, ""])
        lines.extend(["### " + chapter["titulo"], ""])
        for block in chapter["blocos"]:
            lines.extend(["#### " + block["subtitulo"], "", block["texto"], ""])
    return "\n".join(lines)


def palavras(doc: dict) -> int:
    return sum(len(b["texto"].split()) for c in doc["capitulos"] for b in c["blocos"])


def substituir_uma_vez(texto: str, antes: str, depois: str, onde: str) -> str:
    n = texto.count(antes)
    if n != 1:
        raise ValueError(f"{onde}: trecho ocorre {n} vezes (esperado 1): {antes[:90]!r}")
    return texto.replace(antes, depois)


def jesc(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)[1:-1]


def aplicar_documentos(edicoes: list[dict]) -> dict:
    if V2.exists():
        shutil.rmtree(V2)
    shutil.copytree(V1, V2)
    registro: dict[str, list] = {}
    por_item: dict[str, list] = {}
    for e in edicoes:
        por_item.setdefault(e["item"], []).append(e)

    areas_json = {a: read_text(V2 / "areas" / f"{a}.json") for a in {i[:2] for i in por_item}}
    areas_md = {a: read_text(V2 / "areas" / f"{a}.md") for a in areas_json}

    for item, lista in sorted(por_item.items()):
        pasta = V2 / item
        doc = json.loads(read_text(pasta / "documento.json"))
        raw_json = read_text(pasta / "documento.json")
        raw_md = read_text(pasta / "documento.md")
        if render(doc) != raw_md.replace("\r\n", "\n"):
            raise ValueError(f"{item}: documento.md da v1 não corresponde ao documento.json")
        for e in lista:
            locais = [(ci, bi) for ci, c in enumerate(doc["capitulos"])
                      for bi, b in enumerate(c["blocos"]) if e["antes"] in b["texto"]]
            if len(locais) != 1:
                raise ValueError(f"{item}: trecho em {len(locais)} blocos: {e['antes'][:90]!r}")
            ci, bi = locais[0]
            bloco = doc["capitulos"][ci]["blocos"][bi]
            bloco["texto"] = substituir_uma_vez(bloco["texto"], e["antes"], e["depois"], f"{item} bloco")
            raw_json = substituir_uma_vez(raw_json, jesc(e["antes"]), jesc(e["depois"]), f"{item} json")
            raw_md = substituir_uma_vez(raw_md, e["antes"], e["depois"], f"{item} md")
            a = item[:2]
            areas_json[a] = substituir_uma_vez(areas_json[a], jesc(e["antes"]), jesc(e["depois"]), f"areas/{a}.json")
            areas_md[a] = substituir_uma_vez(areas_md[a], e["antes"], e["depois"], f"areas/{a}.md")
            registro.setdefault(item, []).append({
                "capitulo": ci, "bloco": bi,
                "subtitulo": bloco["subtitulo"],
                "questoes": e["questoes"], "motivo": e["motivo"],
                "antes": e["antes"], "depois": e["depois"]})
        if json.loads(raw_json) != doc:
            raise ValueError(f"{item}: edição textual do JSON divergiu da edição estruturada")
        if render(doc) != raw_md.replace("\r\n", "\n"):
            raise ValueError(f"{item}: documento.md editado diverge do documento.json")
        write_text(pasta / "documento.json", raw_json)
        write_text(pasta / "documento.md", raw_md)

        resumo = json.loads(read_text(pasta / "resumo.json"))
        blocos_alt = sorted({(r["capitulo"], r["bloco"]) for r in registro[item]})
        resumo["revisao_especialista"] = {
            "lote": LOTE,
            "questoes_motivadoras": sorted({q for r in registro[item] for q in r["questoes"]}),
            "edicoes": len(registro[item]),
            "blocos_ajustados": len(blocos_alt),
            "versao_anterior": f"pipeline/qa_research/relatorios/dez_areas_final_v1/{item}/documento.json",
            "versao_anterior_sha256": sha_file(V1 / item / "documento.json"),
            "registro": "pipeline/qa_research/relatorios/dez_areas_final_v2/revisao_especialista.json",
        }
        dump_crlf(pasta / "resumo.json", resumo)

    for a in areas_json:
        json.loads(areas_json[a])
        write_text(V2 / "areas" / f"{a}.json", areas_json[a])
        write_text(V2 / "areas" / f"{a}.md", areas_md[a])
    return registro


def finalizar_v2(registro: dict, pareceres: dict) -> None:
    # Manifestos por documento: o gerador de QA verifica documento.json e resumo.json.
    for pasta in sorted(p for p in V2.iterdir() if p.is_dir() and re.fullmatch(r"\d\d_\d\d", p.name)):
        man = json.loads(read_text(pasta / "manifest_resultados.json"))
        man["files"] = {n: sha_file(pasta / n) for n in ("documento.json", "documento.md", "resumo.json")}
        if pasta.name in registro:
            man["origem"] = "revisao_especialista"
        dump_crlf(pasta / "manifest_resultados.json", man)

    indice = json.loads(read_text(V2 / "indice.json"))
    for linha in indice:
        if linha["id"] in registro:
            doc = json.loads(read_text(V2 / linha["id"] / "documento.json"))
            linha["palavras_final"] = palavras(doc)
            linha["revisao_especialista"] = {
                "edicoes": len(registro[linha["id"]]),
                "blocos_ajustados": len({(r["capitulo"], r["bloco"]) for r in registro[linha["id"]]}),
                "questoes_motivadoras": sorted({q for r in registro[linha["id"]] for q in r["questoes"]}),
            }
    dump_crlf(V2 / "indice.json", indice)

    dump_crlf(V2 / "revisao_especialista.json", {
        "schema": "expert-document-revision-v1",
        "lote": LOTE,
        "versao_anterior": "pipeline/qa_research/relatorios/dez_areas_final_v1",
        "fonte_pareceres": "pipeline/qa_research/revisao_especialista/pareceres.json",
        "documentos": registro,
    })

    indice_md = read_text(V2 / "INDICE.md").replace(
        "Registro editorial e referências auxiliares: [REVISAO.md](REVISAO.md).",
        "Registro editorial e referências auxiliares: [REVISAO.md](REVISAO.md). "
        "Revisão a partir dos pareceres do especialista: [REVISAO_ESPECIALISTA.md](REVISAO_ESPECIALISTA.md).")
    write_text(V2 / "INDICE.md", indice_md)

    titulos = {l["id"]: l["titulo"] for l in indice}
    nl = "\r\n"
    out = ["# Revisão dos documentos a partir dos pareceres do especialista", "",
           "Versão derivada de `dez_areas_final_v1`, que permanece intacta. As edições corrigem, "
           "nos documentos de contexto, a origem dos problemas apontados pelo especialista nas questões "
           "aprovadas com ressalvas e reprovadas do primeiro lote (formulários respondidos em 21/10/2026), "
           "para que não se repitam em novas gerações. Os demais documentos são cópias byte a byte da v1.", "",
           f"Totais: {len(registro)} documentos editados; "
           f"{sum(len(v) for v in registro.values())} trechos alterados; "
           f"{sum(len({(r['capitulo'], r['bloco']) for r in v}) for v in registro.values())} blocos ajustados.", "",
           "Registro estruturado (antes/depois): [revisao_especialista.json](revisao_especialista.json). "
           "Pareceres consolidados: `pipeline/qa_research/revisao_especialista/pareceres.json`.", ""]
    for item in sorted(registro):
        out += [f"## {item} — [{titulos[item]}]({item}/documento.md)", ""]
        for r in registro[item]:
            qs = ", ".join(f"{q} ({pareceres[q]['parecer'].replace('_', ' ')})" for q in r["questoes"])
            out += [f"**{r['subtitulo']}** · {qs}", "", f"Motivo: {r['motivo']}", "",
                    f"- Antes: {r['antes'] or '(vazio)'}", f"- Depois: {r['depois'] or '(trecho removido)'}", ""]
    write_text(V2 / "REVISAO_ESPECIALISTA.md", nl.join(out))

    man = json.loads(read_text(V2 / "manifest_revisao.json"))
    man["metodo"] = "revisao_editorial_manual_do_assistente + revisao_especialista"
    man["versao_anterior"] = "dez_areas_final_v1"
    man["files"] = {p.relative_to(V2).as_posix(): sha_file(p)
                    for p in sorted(V2.rglob("*")) if p.is_file() and p.name != "manifest_revisao.json"}
    dump_crlf(V2 / "manifest_revisao.json", man)


# ---------------------------------------------------------------- repositório
def montar_repositorio(pareceres: dict, edq: dict, registro: dict) -> list[dict]:
    selecao = json.loads(read_text(SELECAO))
    mapa = list(csv.DictReader(MAPA.open(encoding="utf-8-sig")))
    if len(mapa) != 60 or set(pareceres) != {r["codigo"] for r in mapa}:
        raise ValueError("Pareceres não cobrem exatamente as 60 questões do formulário")
    ressalvas = {c for c, p in pareceres.items() if p["parecer"] == "aprovada_com_ressalvas"}
    if set(edq["edicoes"]) != ressalvas:
        raise ValueError(f"Edições de questões divergem das ressalvas: {sorted(set(edq['edicoes']) ^ ressalvas)}")
    cobertas = {q for v in registro.values() for r in v for q in r["questoes"]}
    faltam = {c for c, p in pareceres.items() if p["parecer"] != "aprovada"} - cobertas
    if faltam:
        raise ValueError(f"Ressalvas/reprovações sem edição de documento: {sorted(faltam)}")

    REPO.mkdir(parents=True, exist_ok=True)
    linhas = []
    for r in mapa:
        c = r["codigo"]
        p = pareceres[c]
        if p["parecer"] == "reprovada":
            continue
        e = edq["edicoes"].get(c, {})
        item = {
            "id": f"PQ-{r['item']}-{int(r['id']):02d}",
            "tipo": "qa_resposta_curta",
            "status": "aprovada" if p["parecer"] == "aprovada" else "aprovada_com_ressalvas_editada",
            "area_id": r["area_id"], "topico": r["topico"],
            "item": r["item"], "subtopico": r["subtopico"],
            "dificuldade": r["dificuldade"],
            "pergunta": e.get("pergunta", r["pergunta"]),
            "resposta": e.get("resposta", r["resposta"]),
        }
        if e:
            item["pergunta_original"] = r["pergunta"]
            item["resposta_original"] = r["resposta"]
            item["justificativa_edicao"] = e["justificativa"]
        item["parecer_especialista"] = {k: p[k] for k in ("parecer", "motivos", "comentario", "avaliador", "data")}
        obs = edq.get("observacoes_aprovadas", {}).get(c)
        if obs:
            item["observacao"] = obs
        item["contexto"] = {
            "documento_v1": f"pipeline/qa_research/relatorios/dez_areas_final_v1/{r['item']}/documento.json",
            "contexto_sha256_v1": r["contexto_sha256"],
            "documento_vigente": f"pipeline/qa_research/relatorios/dez_areas_final_v2/{r['item']}/documento.json",
            "documento_revisado_pelo_especialista": r["item"] in registro,
        }
        item["origem"] = {"lote": LOTE, "codigo_formulario": c, "selecao_id": selecao["selecao_id"],
                          "candidatas": r["origem"], "auditoria": r["auditoria"]}
        linhas.append(item)

    with (REPO / "questoes.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for it in linhas:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    campos = ["id", "status", "area_id", "topico", "item", "subtopico", "dificuldade", "pergunta", "resposta",
              "pergunta_original", "resposta_original", "parecer", "motivos", "comentario", "observacao",
              "codigo_formulario"]
    with (REPO / "questoes.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for it in linhas:
            w.writerow({**{k: it.get(k, "") for k in campos},
                        "parecer": it["parecer_especialista"]["parecer"],
                        "motivos": "; ".join(it["parecer_especialista"]["motivos"]),
                        "comentario": it["parecer_especialista"]["comentario"],
                        "codigo_formulario": it["origem"]["codigo_formulario"]})
    return linhas


def main() -> None:
    pareceres = ler_respostas()
    edd = json.loads(read_text(HERE / "edicoes_documentos.json"))
    edq = json.loads(read_text(HERE / "edicoes_questoes.json"))

    mapa = {r["codigo"]: r for r in csv.DictReader(MAPA.open(encoding="utf-8-sig"))}
    consolidado = {c: {"item": mapa[c]["item"], "id": int(mapa[c]["id"]), "dificuldade": mapa[c]["dificuldade"],
                       "pergunta": mapa[c]["pergunta"], "resposta": mapa[c]["resposta"], **pareceres[c]}
                   for c in sorted(pareceres)}
    with (HERE / "pareceres.json").open("w", encoding="utf-8", newline="\n") as f:
        json.dump({"schema": "expert-review-v1", "lote": LOTE,
                   "contagem": {k: sum(p["parecer"] == k for p in pareceres.values())
                                for k in PARECERES.values()},
                   "questoes": consolidado}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    registro = aplicar_documentos(edd["edicoes"])
    finalizar_v2(registro, pareceres)
    linhas = montar_repositorio(pareceres, edq, registro)
    cont = {k: sum(p["parecer"] == k for p in pareceres.values()) for k in PARECERES.values()}
    print(f"Pareceres: {cont}")
    print(f"Repositório definitivo: {len(linhas)} questões em {rel(REPO)}")
    print(f"Documentos editados: {len(registro)} em {rel(V2)}")


if __name__ == "__main__":
    main()
