"""Prepare o trabalho pesado uma vez; transfira o diretório pronto ao servidor."""
import argparse
import json
import sqlite3
from contextlib import closing
from dataclasses import replace
from pathlib import Path

from pipeline.inventario.locking import output_lock
from .corpus import CorpusIndex
from .portable import PreparedCorpusIndex, verify_pack, write_pack
from .run import load_config
from .runtime import PersistentBudget
from .selection import LocalE5, materialize_selection, select_topic, validate_profile


def open_snapshot(directory):
    """Exportação explícita de índice existente, sem ler novamente o corpus bruto."""
    root = Path(directory).resolve()
    info = json.loads((root / "indice.json").read_text(encoding="utf-8"))
    index = CorpusIndex(root)
    index.path, index.info = root / "corpus.sqlite3", info
    with closing(sqlite3.connect(index.path.as_uri() + "?mode=ro", uri=True)) as db:
        stored = db.execute("SELECT value FROM metadata WHERE key='fingerprint'").fetchone()
        if (not stored or stored[0] != info["signature"] or
                db.execute("SELECT count(*) FROM chunks").fetchone()[0] != info["chunks"]):
            raise ValueError("Snapshot lexical inconsistente")
    return index


def prepare(config, destination, profile=None, local_semantic=False, lexical_only=False,
            source_pack=None, offline=True, device="cpu", progress=print, embedder_factory=None,
            snapshot=None):
    if config.prepared_pack and not source_pack:
        source_pack = config.prepared_pack
    if snapshot and source_pack:
        raise ValueError("Use snapshot ou source_pack")
    if local_semantic and profile is None:
        raise ValueError("--local-semantic exige perfil de tópico; o modo completo não faz triagem")
    if profile is not None:
        validate_profile(profile, config.topic)
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError("Destino já existe. Use outro nome; pacotes publicados são imutáveis")
    protected = [Path(config.index_dir).resolve(), *[Path(p).resolve() for p in config.origins]]
    if config.manifest:
        protected.append(Path(config.manifest).resolve().parent)
    if source_pack:
        protected.append(Path(source_pack).resolve())
    if snapshot:
        protected.append(Path(snapshot).resolve())
    if any(destination == p or destination in p.parents or p in destination.parents for p in protected):
        raise ValueError("Destino do pacote deve ficar separado das entradas e do cache de índices")
    work = destination.parent / (".prepare-" + destination.name)
    prepared_config = replace(config, output=str(work), prepared_pack=None)
    prepared_config.validate()
    with output_lock(work):
        lexical = (PreparedCorpusIndex(source_pack, config.index_dir, progress=progress) if source_pack else
                   open_snapshot(snapshot) if snapshot else
                   CorpusIndex(config.index_dir, config.origins, config.manifest))
        progress("Preparando/reutilizando textos e BM25 na máquina de preparação")
        if not snapshot:
            lexical.build()
        selected_topic = lexical.info.get("topic_selection", {}).get("profile", {}).get("topic")
        if selected_topic and selected_topic != config.topic:
            raise ValueError("Pacote de origem já foi filtrado para outro tópico; não permite recuperar o acervo excluído")
        selection_files = []
        if source_pack:
            selection_files = [Path(source_pack) / name for name in ("selection.json", "selection.jsonl")
                               if (Path(source_pack) / name).exists()]
        if profile:
            semantic = LocalE5(config.index_dir, offline=offline, threads=config.vector_threads,
                               device=device) if local_semantic else None
            try:
                reasons, report = select_topic(lexical, profile, config.topic, semantic, progress)
                lexical, selection_files = materialize_selection(lexical, reasons, report, config.index_dir)
            finally:
                if semantic:
                    semantic.close()
            progress(f"Acervo temático: {lexical.info['chunks']} trechos; cobertura parcial registrada")
        embedder, vector = None, None
        try:
            if not lexical_only:
                from .embeddings import AzureEmbedder
                from .hybrid import VectorIndex
                # Finalizar um pacote BM25 acontece explicitamente nesta máquina,
                # nunca como efeito de executar a pesquisa no servidor.
                if getattr(lexical, "is_prepared", False):
                    if lexical.prepared_vector is None:
                        lexical.is_prepared = False
                budget = PersistentBudget(work / "orcamento_embeddings.json", config.embedding_max_calls)
                embedder = (embedder_factory or AzureEmbedder)(prepared_config, budget)
                vector = VectorIndex(prepared_config, lexical, embedder, progress)
                vector.build()
            data = write_pack(lexical, destination, vector, selection_files, progress)
            verify_pack(destination, config.index_dir, force=True, progress=progress)
            return {"directory": str(destination), "mode": data["mode"],
                    "chunks": data["corpus"]["chunks"], "selection": data["selection"],
                    "bytes": sum(row["bytes"] for row in data["files"].values()),
                    "complete_corpus": data["corpus"]["complete_corpus"]}
        finally:
            if embedder:
                embedder.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--destination", required=True)
    parser.add_argument("--manifest", help="Manifesto do corpus bruto completo")
    parser.add_argument("--source-pack", help="Partir de textos/BM25 de um pacote, sem corpus bruto")
    parser.add_argument("--snapshot", help="Pasta de índice existente com corpus.sqlite3 e indice.json; exporta sem reler originais")
    parser.add_argument("--profile", help="JSON de consultas de triagem; ausente conserva todo o acervo")
    parser.add_argument("--local-semantic", action="store_true", help="União BM25 + E5 multilíngue local na triagem")
    parser.add_argument("--allow-model-download", action="store_true", help="Por padrão só usa modelo já no cache")
    parser.add_argument("--device", default="cpu", choices=("cpu", "cuda"))
    parser.add_argument("--lexical-only", action="store_true", help="Sem Azure; exige finalização posterior para pesquisa híbrida")
    parser.add_argument("--verify", action="store_true", help="Só verificar integralmente um pacote existente")
    args = parser.parse_args(argv)
    config = load_config(args.config, manifest=args.manifest)
    if args.verify:
        data, signature = verify_pack(args.destination, config.index_dir, force=True)
        print(json.dumps({"verified": True, "signature": signature, "mode": data["mode"]}, indent=2))
        return 0
    profile = json.loads(Path(args.profile).read_text(encoding="utf-8-sig")) if args.profile else None
    result = prepare(config, args.destination, profile, args.local_semantic, args.lexical_only,
                     args.source_pack, not args.allow_model_download, args.device, snapshot=args.snapshot)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
