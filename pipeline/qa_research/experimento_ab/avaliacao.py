"""Avaliação de um braço: gap com/sem contexto (GPT-4.1 Nano, Mini e 4.1) e sustentação dos gabaritos.

Mesmo motor, prompts, juiz e limite de 100 palavras do benchmark_gap. A única diferença é o contexto, que é o mesmo
critério nos quatro braços: os capítulos inteiros tocados pelo contexto de geração da questão (comum.indices_avaliacao).
A sustentação é auditada contra esse mesmo contexto.
"""
from __future__ import annotations

from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research import benchmark_gap as G
from pipeline.qa_research.piloto_janela.core import blocos

from . import comum as C


def carregar(braco_dir: Path):
    cfg = read_json(Path(braco_dir) / "config.json")
    if not cfg or cfg.get("schema") != "experimento-ab-geracao-v1":
        raise ValueError(f"{braco_dir}: pasta sem geração do experimento")
    if not (Path(braco_dir) / "geracao_concluida.json").exists():
        raise ValueError(f"{braco_dir}: geração ainda não concluída (falhas pendentes); rode a geração de novo")
    docs, unidade = C.resolver(cfg["docs"]), cfg["unidade"]
    original = C.linhas(Path(braco_dir) / "aprovadas.jsonl")
    if not original or len({q["uid"] for q in original}) != len(original):
        raise ValueError("Banco vazio ou UIDs repetidos")
    cache = {i: blocos(i, docs)[1] for i in {q["item"] for q in original}}
    enriched, rows = [], []
    for q in original:
        bs = cache[q["item"]]
        selected = [bs[i] for i in C.indices_avaliacao(q, bs, unidade)]
        text = "\n\n".join(f"{b['titulo_capitulo']} / {b['subtitulo']}\n{b['texto']}" for b in selected)
        enriched.append({**q, "contexto_tecnico": text, "blocos_contexto": [
            dict(id=f"B{k}", texto=b["texto"], indice_documento=b["indice"]) for k, b in enumerate(selected, 1)]})
        for arm in G.ARMS:
            rows.append({**q, "uid_original": q["uid"], "uid": arm + ":" + q["uid"], "condicao": arm,
                         "contexto_tecnico": text if arm == "open_book" else None})
    return enriched, rows, cfg


def executar(braco_dir: Path, saida: Path, workers=8, judge_workers=2, mini=G.MODELS["gpt-4-1-mini"], clientes=None,
             progress=print) -> int:
    if workers < 1 or judge_workers < 1:
        raise ValueError("Workers positivos obrigatórios")
    original, rows, gcfg = carregar(braco_dir)
    saida = Path(saida)
    if G.prompt("juiz") != G.Q.prompt("juiz"):
        raise ValueError("Juiz congelado diverge do motor; não misturar protocolos")
    models = {**G.MODELS, "gpt-4-1-mini": mini}
    cfg = dict(schema="experimento-ab-avaliacao-v1", braco=gcfg["braco"], unidade_geracao=gcfg["unidade"],
               contexto="capitulos_tocados_pelo_contexto_de_geracao", n=len(original),
               dados_sha256=C.sha(original), questoes_sha256=C.sha(rows), modelos=models, juiz=G.Q.JUIZ,
               limite_palavras=100, lote_juiz=8,
               prompts={n: C.sha(G.prompt(n)) for n in ("respondente", "juiz", "faithfulness")})
    with output_lock(saida):
        old = read_json(saida / "config.json")
        if old is not None and old != cfg:
            raise ValueError("Protocolo ou questões mudaram em relação à avaliação existente; use outra saída")
        atomic_json(saida / "config.json", cfg)
        G.Q.C.GeracaoSemConteudo.jsonl(saida / "questoes.jsonl", rows)
        G.Q.C.GeracaoSemConteudo.jsonl(saida / "contextos.jsonl", original)
        directory = saida / "avaliacao"
        with output_lock(directory):
            atomic_json(directory / "protocolo_experimento.json", cfg)
            for m in models:
                for sub in ("respostas", "juiz"):
                    (directory / sub / m).mkdir(parents=True, exist_ok=True)
            (directory / "falhas").mkdir(exist_ok=True)
            marker = saida / "rodada_concluida.json"
            marker.unlink(missing_ok=True)
            (saida / "falha_execucao.json").unlink(missing_ok=True)
            e = G.AvaliacaoGap(saida, respondentes=models, juiz=G.Q.JUIZ, grupos=[tuple(models)], workers=workers,
                               judge_workers=judge_workers, lote_juiz=8, clientes=clientes, progress=progress)
            try:
                e.run()
                G.exportar_gap(saida, models)
                qa_done = all(len(e.vereditos[m]) == len(rows) for m in models)
                faithful_done = G.faithfulness(e, original)
                if qa_done and faithful_done:
                    atomic_json(marker, dict(status="concluida", questoes=len(original), casos_resposta=len(rows) * len(models)))
                return 0 if qa_done and faithful_done else 2
            except Exception as exc:  # noqa: BLE001
                atomic_json(saida / "falha_execucao.json", dict(erro=type(exc).__name__, mensagem=str(exc)[:1500]))
                progress(f"[INCOMPLETA] {type(exc).__name__}: {exc}", flush=True)
                return 2
            finally:
                for c in e.clientes.values():
                    if hasattr(c, "close"):
                        c.close()
