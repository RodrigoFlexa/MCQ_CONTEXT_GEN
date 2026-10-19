"""Snapshots portáteis: textos, proveniência, BM25 e FAISS, sem corpus bruto.

O manifesto é publicado por último. Hashes são verificados uma vez por instalação;
o recibo local é invalidado se o manifesto ou os atributos dos arquivos mudarem.
"""
import os
import shutil
import sqlite3
import tempfile
import time
from contextlib import closing
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json, sha
from .corpus import CorpusIndex, _file_hash

SCHEMA = "qa-research-pack-v1"
FILES = {"corpus.sqlite3", "index.faiss", "selection.json", "selection.jsonl"}


def inspect_pack(directory):
    root = Path(directory).resolve()
    data = read_json(root / "pack.json")
    if not isinstance(data, dict) or data.get("schema") != SCHEMA or data.get("ready") is not True:
        raise ValueError("Pacote ausente, incompleto ou de versão desconhecida")
    files = data.get("files")
    if (not isinstance(files, dict) or "corpus.sqlite3" not in files or
            not set(files).issubset(FILES)):
        raise ValueError("Lista de arquivos do pacote inválida")
    if bool(data.get("vector")) != ("index.faiss" in files):
        raise ValueError("Manifesto e arquivos vetoriais divergem")
    if data.get("mode") != ("hybrid" if data.get("vector") else "bm25"):
        raise ValueError("Modo do pacote diverge de seu conteúdo")
    for name, record in files.items():
        path = root / name
        if (path.is_symlink() or not path.is_file() or path.stat().st_size != record.get("bytes")
                or not isinstance(record.get("sha256"), str) or len(record["sha256"]) != 64):
            raise ValueError(f"Arquivo ausente/alterado no pacote: {name}")
    if data.get("vector"):
        vector = data["vector"]
        if (vector["sha256"] != files["index.faiss"]["sha256"] or
                vector["protocol"]["corpus"] != data["corpus"]["signature"] or
                vector["chunks"] != data["corpus"]["chunks"]):
            raise ValueError("Vetores pertencem a outro corpus")
    return data


def verify_pack(directory, cache_dir, force=False, progress=print):
    root = Path(directory).resolve()
    with output_lock(Path(cache_dir) / "verified-packs" / sha(str(root), 40)):
        return _verify_pack(root, cache_dir, force, progress)


def _verify_pack(directory, cache_dir, force, progress):
    root = Path(directory).resolve()
    data = inspect_pack(root)
    signature = sha((root / "pack.json").read_text(encoding="utf-8"), 64)
    def state():
        result = {}
        for name in data["files"]:
            s = (root / name).stat()
            result[name] = [s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_ino, s.st_dev]
        return result
    stamp = state()
    # Nunca transportar este recibo com o pacote. O caminho/local de instalação
    # também entra na chave para forçar a verificação após cada transferência.
    receipt = Path(cache_dir) / "verified-packs" / (sha(str(root), 40) + ".json")
    expected = {"signature": signature, "stat": stamp}
    if force or read_json(receipt) != expected:
        progress("Verificando integridade do pacote nesta instalação (uma vez)")
        for name, record in data["files"].items():
            if _file_hash(root / name) != record["sha256"]:
                raise ValueError(f"Hash inválido no pacote: {name}")
        with closing(sqlite3.connect((root / "corpus.sqlite3").as_uri() + "?mode=ro", uri=True)) as db:
            fingerprint = db.execute("SELECT value FROM metadata WHERE key='fingerprint'").fetchone()
            if not fingerprint or fingerprint[0] != data["corpus"]["signature"]:
                raise ValueError("SQLite pertence a outro corpus")
            if db.execute("SELECT count(*) FROM chunks").fetchone()[0] != data["corpus"]["chunks"]:
                raise ValueError("Contagem de trechos do pacote inválida")
            if data.get("vector"):
                import faiss
                import numpy as np
                index = faiss.read_index(str(root / "index.faiss"))
                if (index.ntotal != data["corpus"]["chunks"] or
                        index.d != data["vector"]["dimensions"]):
                    raise ValueError("FAISS incompleto/incompatível")
                # A ligação IDs SQLite/FAISS é auditada na instalação, incluindo
                # subconjuntos com IDs esparsos. Igual ntotal não seria suficiente.
                if hasattr(index, "id_map"):
                    ids = faiss.vector_to_array(index.id_map)
                elif hasattr(index, "invlists"):
                    parts = []
                    for i in range(index.nlist):
                        size = index.invlists.list_size(i)
                        pointer = index.invlists.get_ids(i)
                        try:
                            parts.append(faiss.rev_swig_ptr(pointer, size).copy())
                        finally:
                            index.invlists.release_ids(i, pointer)
                    ids = np.concatenate(parts) if parts else np.empty(0, dtype=np.int64)
                else:
                    raise ValueError("Tipo FAISS sem mapeamento auditável de IDs")
                actual = np.sort(ids)
                offset = 0
                # Cursor explícito mantém o custo proporcional ao número de IDs,
                # sem materializar textos ou uma segunda cópia de todos os IDs.
                cursor = db.execute("SELECT id FROM chunks ORDER BY id")
                while rows := cursor.fetchmany(4096):
                    if not np.array_equal(actual[offset:offset + len(rows)], [r[0] for r in rows]):
                        raise ValueError("IDs FAISS não correspondem ao SQLite do pacote")
                    offset += len(rows)
                del index
        if state() != stamp:
            raise ValueError("Pacote mudou durante a verificação")
        atomic_json(receipt, expected)
    else:
        progress("Pacote já verificado; reutilizando índices sem percorrer o corpus bruto")
    return data, signature


class PreparedCorpusIndex(CorpusIndex):
    is_prepared = True

    def __init__(self, directory, cache_dir, force=False, progress=print):
        super().__init__(directory)
        data, signature = verify_pack(directory, cache_dir, force, progress)
        self.path = self.directory / "corpus.sqlite3"
        self.info = {**data["corpus"], "index_path": str(self.path),
                     "portable_pack": {"signature": signature, "mode": data["mode"],
                                       "selection": data.get("selection")}}
        self.prepared_vector = ({"path": self.directory / "index.faiss", "info": data["vector"]}
                                if data.get("vector") else None)

    def build(self):
        return self.info


def _publish(staging, destination):
    # OneDrive/antivírus podem manter um handle sem FILE_SHARE_DELETE por alguns
    # milissegundos, mesmo após fechar SQLite/JSON. Não refaça uma cópia grande
    # por causa desse bloqueio transitório; nunca substitua um pacote existente.
    for attempt in range(6):
        if destination.exists():
            raise FileExistsError("Destino do pacote já existe")
        try:
            os.rename(staging, destination)
            return
        except PermissionError as exc:
            if getattr(exc, "winerror", None) not in {5, 32} or attempt == 5 or destination.exists():
                raise
            time.sleep(.05 * 2 ** attempt)


def write_pack(lexical, destination, vector=None, selection_files=(), progress=print):
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError("Destino já existe; use outro nome para preservar o pacote publicado")
    if destination == lexical.directory or destination in lexical.path.parents:
        raise ValueError("Destino deve ficar separado do índice de origem")
    destination.parent.mkdir(parents=True, exist_ok=True)
    # O staging fica no mesmo volume para a publicação por rename ser atômica.
    staging = Path(tempfile.mkdtemp(prefix=".pack-", dir=destination.parent))
    try:
        progress("Copiando textos e proveniência para pacote portátil")
        with closing(sqlite3.connect(lexical.path.as_uri() + "?mode=ro", uri=True)) as source:
            with closing(sqlite3.connect(staging / "corpus.sqlite3")) as target:
                source.backup(target)
        names = ["corpus.sqlite3"]
        if vector:
            vector_path = Path(vector.config.index_dir) / "dense" / vector.info["signature"] / "index.faiss"
            # Também permite reempacotar um snapshot já preparado.
            if getattr(lexical, "prepared_vector", None):
                vector_path = lexical.prepared_vector["path"]
            shutil.copyfile(vector_path, staging / "index.faiss")
            names.append("index.faiss")
        for path in selection_files:
            path = Path(path)
            if path.name not in {"selection.json", "selection.jsonl"}:
                raise ValueError("Nome de relatório de seleção inválido")
            shutil.copyfile(path, staging / path.name)
            names.append(path.name)
        files = {name: {"bytes": (staging / name).stat().st_size,
                        "sha256": _file_hash(staging / name)} for name in names}
        data = {"schema": SCHEMA, "ready": True, "mode": "hybrid" if vector else "bm25",
                "corpus": {k: v for k, v in lexical.info.items() if k not in {"index_path", "portable_pack"}},
                "vector": vector.info if vector else None, "files": files,
                "selection": read_json(staging / "selection.json")}
        if vector and files["index.faiss"]["sha256"] != vector.info["sha256"]:
            raise ValueError("FAISS mudou durante a preparação")
        atomic_json(staging / "pack.json", data)
        _publish(staging, destination)
        return data
    finally:
        if staging.exists() and staging.resolve().parent == destination.parent and staging.name.startswith(".pack-"):
            shutil.rmtree(staging)
