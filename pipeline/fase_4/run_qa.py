"""CLI do fluxo QA completo. Cosine e saturação são observacionais por padrão."""
import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.fase_4.config import QAConfig
from pipeline.fase_4.domain import TOPICOS
from pipeline.fase_4.engine import execute
from pipeline.fase_4.prompts_qa import SYSTEM_PROMPT, build_prompt


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--deployment", default=os.getenv("AOAI_DEFAULT_DEPLOYMENT", "gpt-5-4-petrobras"))
    p.add_argument("--preparation-deployment")
    p.add_argument("--judge-deployment")
    p.add_argument("--effort", choices=["minimal", "low", "medium", "high"], default="high")
    corpus = p.add_mutually_exclusive_group()
    corpus.add_argument("--corpus-dir", type=Path)
    corpus.add_argument("--corpus-txt", type=Path, nargs="+")
    corpus.add_argument("--corpus-zip", type=Path)
    p.add_argument("--output", type=Path, default=QAConfig.output)
    p.add_argument("--external-examples", type=Path, default=QAConfig.external_examples)
    p.add_argument("--reviewed-seeds", type=Path, default=QAConfig.reviewed_seeds)
    p.add_argument("--human-ratings", type=Path, default=QAConfig.human_ratings)
    p.add_argument("--topics", nargs="+")
    p.add_argument("--limit-per-topic", type=int, default=100)
    p.add_argument("--batch-size", type=int, default=5)
    p.add_argument("--max-attempts-per-topic", type=int, default=500)
    p.add_argument("--max-calls", type=int, default=5000, help="Pedidos lógicos, somados entre todos os papéis")
    p.add_argument("--max-consecutive-api-failures", type=int, default=3)
    p.add_argument("--max-refinements", type=int, default=2)
    p.add_argument("--minimum-quality", type=float, default=.75)
    p.add_argument("--minimum-fewshot-quality", type=float, default=.85)
    p.add_argument("--format-examples", type=int, default=8)
    p.add_argument("--cross-topic-examples", type=int, default=4)
    p.add_argument("--embedding-model", default=QAConfig.embedding_model)
    p.add_argument("--clusters", type=int, default=24)
    p.add_argument("--similarity-threshold", type=float, default=.50,
                   help="Limiar observado; só filtra com --enable-cosine-filter")
    p.add_argument("--enable-cosine-filter", action="store_true", help="Experimento FUTURO: ativa rejeição por cosine")
    p.add_argument("--enable-saturation-stop", action="store_true", help="Experimento FUTURO: ativa parada por entropia")
    p.add_argument("--entropy-gain-threshold", type=float, default=.010)
    p.add_argument("--entropy-patience", type=int, default=3)
    p.add_argument("--entropy-warmup", type=int, default=12)
    p.add_argument("--observe-only", action="store_true", help="Explicita que cosine e saturação ficam desligados")
    p.add_argument("--no-embeddings", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--resume", action="store_true")
    p.add_argument("--prepare-only", action="store_true")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--list-topics", action="store_true")
    p.add_argument("--print-prompt", action="store_true")
    return p


def config_from_args(args):
    cfg = QAConfig()
    for name in ("output", "external_examples", "reviewed_seeds", "human_ratings", "deployment", "effort",
                 "topics", "limit_per_topic", "batch_size", "max_attempts_per_topic", "max_calls",
                 "max_consecutive_api_failures", "max_refinements", "minimum_quality", "minimum_fewshot_quality",
                 "format_examples", "cross_topic_examples", "embedding_model", "clusters",
                 "similarity_threshold", "enable_cosine_filter", "enable_saturation_stop",
                 "entropy_gain_threshold", "entropy_patience", "entropy_warmup", "resume", "prepare_only", "seed"):
        setattr(cfg, name, getattr(args, name))
    cfg.preparation_deployment = args.preparation_deployment or args.deployment
    cfg.judge_deployment = args.judge_deployment or args.deployment
    if args.corpus_dir is not None:
        cfg.corpus_dir = args.corpus_dir
    if args.corpus_txt:
        cfg.corpus_txt, cfg.corpus_dir = args.corpus_txt, None
    if args.corpus_zip:
        cfg.corpus_zip, cfg.corpus_dir = args.corpus_zip, None
    return cfg


def main():
    p = parser()
    args = p.parse_args()
    if args.no_embeddings:
        p.error("Embeddings são necessários para recuperar o domínio e medir entropia; não há fallback sem corpus vetorizado.")
    if args.observe_only and (args.enable_cosine_filter or args.enable_saturation_stop):
        p.error("--observe-only não pode ser combinado com os filtros ativos")
    if args.list_topics:
        for topic in TOPICOS:
            print(topic)
        return
    if args.print_prompt:
        print(SYSTEM_PROMPT)
        print(build_prompt(topic="{topic}", subtopic="{subtopic}", difficulty="{difficulty}",
              scope="{scope}", focus="{focus}", document="{document}",
              chunks=[{"chunk_id": "{chunk_id}", "texto": "{original_domain_text}"}],
              format_examples=[{"question": "{external_question}", "answer": "{external_answer}"}],
              quality_examples=[{"question": "{best_rated_question}", "answer": "{best_rated_answer}"}],
              previous_questions=["{previous_questions}"], used_concepts=["{used_concepts}"],
              count="{count}", batch_id="{batch_id}"))
        return
    cfg = config_from_args(args)
    print(f"Fluxo QA v2: domínio -> geração -> Scorer/Refiner -> Judge -> QA", flush=True)
    print(f"Cosine filtra: {cfg.enable_cosine_filter}; saturação para: {cfg.enable_saturation_stop}; "
          f"deployment={cfg.deployment}; effort={cfg.effort}; saída={cfg.output}", flush=True)
    try:
        store = execute(cfg)
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        raise SystemExit(str(exc)) from exc
    print(f"Status: {store.meta['status']}; aceitas={len(store.accepted)}; "
          f"pedidos Azure={store.state['api_calls']}", flush=True)


if __name__ == "__main__":
    main()
