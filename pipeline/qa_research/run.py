"""Execute pesquisa e/ou QA; --plan só inspeciona entradas, sem modelos ou rede."""
import argparse
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from pipeline.inventario.llm import BudgetExceeded
from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json, sha
from . import VERSION
from .config import Config
from .corpus import CorpusIndex
from .engine import ResearchPipeline
from .export import export_run
from .runtime import PersistentBudget, make_clients

ROOT = Path(__file__).resolve().parents[2]


def load_config(path, output=None, manifest=None, pack=None):
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if output:
        data["output"] = output
    if manifest is not None:
        data["manifest"] = manifest
    if pack is not None:
        data["prepared_pack"] = pack
    if data.get("prepared_pack") and manifest is not None:
        raise ValueError("Use --pack ou --manifest; o pacote já contém o corpus")
    config = Config(**data)
    def absolute(value):
        p = Path(value)
        return str(p.resolve() if p.is_absolute() else (ROOT / p).resolve())
    config.output, config.index_dir = absolute(config.output), absolute(config.index_dir)
    config.origins = [absolute(p) for p in config.origins]
    if config.manifest:
        config.manifest = absolute(config.manifest)
    if config.prepared_pack:
        config.prepared_pack = absolute(config.prepared_pack)
    return config.validate()


def implementation_hash():
    digest = hashlib.sha256()
    for path in sorted(Path(__file__).parent.glob("*.py")):
        digest.update(path.name.encode())
        digest.update(path.read_text(encoding="utf-8").encode("utf-8"))
    return digest.hexdigest()


def inspect(config):
    result = {"topico": config.topic, "limites": config.identity(),
              "origens": [], "manifest": config.manifest,
              "observacao": "Sem chamada de modelo, download ou indexação. Recortes serão propostos na pesquisa."}
    if config.prepared_pack:
        from .portable import inspect_pack
        result["pacote"] = inspect_pack(config.prepared_pack)
        result["origens"] = []
        result["manifest"] = None
        return result
    for origin in config.origins:
        root = Path(origin)
        result["origens"].append({"path": origin, "existe": root.is_dir(),
                                 "selecoes": len(list(root.glob("subtopicos/*/selecao.json")))})
    if config.manifest and not Path(config.manifest).is_file():
        raise ValueError("Manifesto informado não existe")
    if not config.manifest and not any(r["selecoes"] for r in result["origens"]):
        raise ValueError("Nenhuma seleção original encontrada nas origens")
    return result


def execute(config, stage="completo", clients=None, index=None, progress=print):
    config.validate()
    if stage not in ("indice", "pesquisa", "qa", "completo"):
        raise ValueError("stage deve ser indice, pesquisa, qa ou completo")
    out = Path(config.output)
    with output_lock(out):
        supplied_index = index is not None
        if index is None:
            if config.prepared_pack:
                from .portable import PreparedCorpusIndex
                index = PreparedCorpusIndex(config.prepared_pack, config.index_dir, progress=progress)
            else:
                index = CorpusIndex(config.index_dir, config.origins, config.manifest)
        progress("Abrindo pacote preparado" if config.prepared_pack else
                 "Verificando corpus e preparando/reutilizando índice lexical")
        info = index.build()
        if (not supplied_index and config.retrieval_mode == "hybrid"
                and getattr(index, "is_prepared", False) and index.prepared_vector is None):
            raise ValueError("Pacote sem FAISS/Azure pronto. Finalize-o na máquina de preparação antes da pesquisa híbrida")
        selected_topic = info.get("topic_selection", {}).get("profile", {}).get("topic")
        if selected_topic and selected_topic != config.topic:
            raise ValueError("Acervo filtrado para outro tópico/escopo. Prepare um pacote compatível ou use o acervo completo")
        identity = {"version": VERSION, "implementation": implementation_hash(),
                    "config": config.identity(), "corpus_signature": info["signature"]}
        if info.get("portable_pack"):
            identity["pack_signature"] = info["portable_pack"]["signature"]
        fingerprint = sha(json.dumps(identity, sort_keys=True, ensure_ascii=False), 64)
        record = read_json(out / "execucao.json")
        if record and record["fingerprint"] != fingerprint:
            raise ValueError("Configuração, implementação ou corpus mudaram. Use nova saída para preservar a rastreabilidade.")
        atomic_json(out / "execucao.json", {**(record or {}), "fingerprint": fingerprint, **identity})
        atomic_json(out / "config.json", asdict(config))
        atomic_json(out / "indice.json", info)
        owned_clients = clients is None
        budget = PersistentBudget(out / "orcamento.json", config.max_calls)
        if stage == "qa" and not (out / "plano.json").exists():
            raise ValueError("Execute --stage pesquisa antes de --stage qa")
        interruption = None
        hybrid_index = None
        try:
            if clients is None and stage != "indice":
                clients = make_clients(config, budget)
            if not supplied_index and config.retrieval_mode == "hybrid":
                from .embeddings import AzureEmbedder
                from .hybrid import HybridCorpusIndex, LLMReranker
                embedding_budget = PersistentBudget(out / "orcamento_embeddings.json", config.embedding_max_calls)
                embedder = AzureEmbedder(config, embedding_budget)
                hybrid_index = HybridCorpusIndex(config, index, embedder,
                    LLMReranker(clients["reranqueador"]) if clients else None, progress=progress)
                retrieval_fingerprint = sha(json.dumps(embedder.protocol, sort_keys=True), 64)
                if record and record.get("retrieval_fingerprint", retrieval_fingerprint) != retrieval_fingerprint:
                    raise ValueError("Protocolo/endpoint dos embeddings mudou; use nova saída")
                atomic_json(out / "execucao.json", {"fingerprint": fingerprint, **identity,
                            "retrieval_fingerprint": retrieval_fingerprint})
                info = hybrid_index.build()
                index = hybrid_index
                atomic_json(out / "indice.json", info)
            completed = True
            if stage != "indice":
                engine = ResearchPipeline(config, index, clients, progress=progress)
                if stage in ("pesquisa", "completo"):
                    completed = engine.research()
                if completed and stage in ("qa", "completo"):
                    completed = engine.generate_qa()
            if not completed:
                interruption = "Orçamento cumulativo de chamadas atingido"
        except BudgetExceeded as exc:
            interruption = str(exc)
        except KeyboardInterrupt:
            interruption = "Execução interrompida pelo usuário"
            raise
        except Exception as exc:
            interruption = type(exc).__name__ + ": " + str(exc)
            raise
        finally:
            if hybrid_index is not None:
                hybrid_index.close()
            if owned_clients and clients:
                for client in clients.values():
                    client.close()
            summary = export_run(config, info, interruption)
        return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Arquivo JSON com tópico e limites")
    parser.add_argument("--output", help="Sobrescreve somente a pasta de saída")
    parser.add_argument("--manifest", help="Manifesto do corpus completo; sobrescreve o campo do JSON")
    parser.add_argument("--pack", help="Pacote preparado: não lê nem reindexa arquivos de origem")
    parser.add_argument("--stage", choices=("indice", "pesquisa", "qa", "completo"), default="completo")
    parser.add_argument("--plan", action="store_true")
    args = parser.parse_args(argv)
    config = load_config(args.config, args.output, args.manifest, args.pack)
    if args.plan:
        print(json.dumps(inspect(config), ensure_ascii=False, indent=2))
        return 0
    summary = execute(config, stage=args.stage)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 2 if summary["interrupcao"] or summary["pendencias_execucao"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
