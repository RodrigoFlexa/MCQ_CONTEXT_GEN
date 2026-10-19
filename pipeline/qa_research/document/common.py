"""Contratos de arquivo compartilhados; somente biblioteca padrão no servidor."""
import hashlib
import json
import re
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json, sha

ROOT = Path(__file__).resolve().parents[3]
PLACEHOLDER = re.compile(r"<\s*(?:number|num|valor|value)\s*>|\[(?:ilegível|redacted)\]", re.I)


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def absolute(path):
    p = Path(path)
    return p.resolve() if p.is_absolute() else (ROOT / p).resolve()


def load_profile(path):
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if data.get("schema") != "document-profile-v2":
        raise ValueError("Perfil documental desconhecido")
    if not data.get("topic", {}).get("escopo") or not data.get("facets"):
        raise ValueError("Informe tópico e recortes de cobertura")
    ids = [f["id"] for f in data["facets"]]
    if len(ids) != len(set(ids)):
        raise ValueError("IDs de recortes repetidos")
    for f in data["facets"]:
        if not all(f.get(k) for k in ("id", "titulo", "grupo", "foco", "consultas", "termos")):
            raise ValueError("Recorte incompleto")
    return data


def source_record(row):
    if row.get("source_kind") not in {"saved_selection", "verified_manifest"}:
        raise ValueError("Somente passagens originais com procedência verificável entram no pacote")
    text = row.get("texto", row.get("text", ""))
    if not isinstance(text, str) or not text.strip() or not row.get("chunk_id"):
        raise ValueError("Fonte sem texto ou ID original")
    source = {k: v for k, v in row.items() if k not in {"neighbor_chunks", "text", "retrieval"}}
    source.update(texto=text, texto_sha256=sha(text, 64), id="E" + sha(row["chunk_id"] + "\n" + text, 16))
    known = (source.get("source_boundary") == "known_document" or
             isinstance(source.get("page_ini"), int))
    source["qualidade"] = {"marcadores_numericos": len(PLACEHOLDER.findall(text)),
        "documento_identificado": known, "pagina_identificada": isinstance(source.get("page_ini"), int),
        "idioma_declarado": source.get("language"),
        "idioma_verificado": False, "independencia_documental": "identificavel" if known else "indeterminada"}
    return source


def citations_for(source, size=700):
    """Particiona todo o texto sem perder caracteres; IDs incluem os offsets reais."""
    text, start, rows = source["texto"], 0, []
    while start < len(text):
        end = min(len(text), start + size)
        if end < len(text):
            split = text.rfind(" ", start + size // 2, end)
            if split > start:
                end = split + 1
        rows.append({"id": source["id"] + f":{start}:{end}", "fonte": source["id"], "inicio": start, "fim": end})
        start = end
    return rows


class Packet:
    """Carrega um pacote pequeno, verificando hashes, fontes e citações sem modelos."""
    def __init__(self, path):
        self.path = Path(path).resolve()
        self.manifest = read_json(self.path / "manifest.json")
        if not self.manifest or self.manifest.get("schema") != "document-packet-v2":
            raise ValueError("Pacote documental ausente/incompatível")
        expected = {"profile.json", "sources.jsonl", "citations.jsonl", "facets.json", "preparation.json"}
        if set(self.manifest.get("files", {})) != expected:
            raise ValueError("Arquivos inesperados no manifesto")
        for name, digest in self.manifest["files"].items():
            if (self.path / name).is_symlink() or file_hash(self.path / name) != digest:
                raise ValueError("Pacote alterado: " + name)
        self.signature = sha(canonical(self.manifest), 64)
        self.profile = load_profile(self.path / "profile.json")
        self.facets = read_json(self.path / "facets.json")
        self.preparation = read_json(self.path / "preparation.json")
        self.sources = {}
        for line in (self.path / "sources.jsonl").read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            checked = source_record(row)
            if row["id"] in self.sources or any(row[k] != checked[k] for k in ("id", "texto_sha256")):
                raise ValueError("Identidade de fonte inválida/repetida")
            self.sources[row["id"]] = row
        self.citations = {}
        for line in (self.path / "citations.jsonl").read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            source = self.sources.get(row["fonte"])
            if (not source or type(row["inicio"]) is not int or type(row["fim"]) is not int
                    or not 0 <= row["inicio"] < row["fim"] <= len(source["texto"])
                    or row["id"] != source["id"] + f":{row['inicio']}:{row['fim']}"
                    or row["id"] in self.citations):
                raise ValueError("Citação por intervalo inválida")
            self.citations[row["id"]] = row
        self.by_source = {}
        for row in self.citations.values():
            self.by_source.setdefault(row["fonte"], []).append(row["id"])
        if set(self.by_source) != set(self.sources):
            raise ValueError("Há fontes sem catálogo de citações")
        for sid, ids in self.by_source.items():
            ranges = sorted((self.citations[c]["inicio"], self.citations[c]["fim"]) for c in ids)
            if ranges[0][0] != 0 or ranges[-1][1] != len(self.sources[sid]["texto"]) or any(
                    a[1] != b[0] for a, b in zip(ranges, ranges[1:])):
                raise ValueError("Catálogo não preserva todo o texto")
        if [f["id"] for f in self.facets] != [f["id"] for f in self.profile["facets"]]:
            raise ValueError("Recortes e perfil divergem")
        for f in self.facets:
            ids = f["fontes"]
            if len(ids) != len(set(ids)) or not set(ids) <= set(self.sources):
                raise ValueError("Fonte desconhecida/repetida em recorte")

    def quote(self, cid):
        row = self.citations[cid]
        return self.sources[row["fonte"]]["texto"][row["inicio"]:row["fim"]]

    def views(self, source_ids):
        return [{"id": sid, "titulo": self.sources[sid].get("title"),
                 "colecao": self.sources[sid].get("collection"), "qualidade": self.sources[sid]["qualidade"],
                 "metadados": {k: self.sources[sid].get(k) for k in
                     ("document_id", "source_boundary", "jurisdiction", "page_ini", "page_fim", "year", "edition", "url")},
                 "trechos": [{"id": cid, "texto": self.quote(cid)} for cid in self.by_source[sid]]}
                for sid in source_ids]

    def support(self, ids):
        return [{"evidencia_id": self.citations[cid]["fonte"], "trecho_id": cid,
                 "citacao": self.quote(cid)} for cid in dict.fromkeys(ids)]
