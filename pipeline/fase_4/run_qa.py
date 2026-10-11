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
    p.add_argument("--effort", choices=["low", "medium", "high"], default="medium")
    corpus = p.add_mutually_exclusive_group()
    corpus.add_argument("--corpus-dir", type=Path)
    corpus.add_argument("--corpus-txt", type=Path, nargs="+")
    corpus.add_argument("--corpus-zip", type=Path)
    corpus.add_argument('--corpus-manifest',type=Path,help='Manifesto instalado com Petrolês + ANP + HSE + BSEE + REGIS')
    p.add_argument('--allow-sample-corpus',action='store_true',help='Permite explicitamente um corpus de teste, sem confundir com instalação completa')
    p.add_argument('--lexical-candidates-per-collection',type=int,default=60)
    p.add_argument("--output", type=Path, default=QAConfig.output)
    p.add_argument("--external-examples", type=Path, default=QAConfig.external_examples)
    p.add_argument("--reviewed-seeds", type=Path, default=QAConfig.reviewed_seeds)
    p.add_argument("--human-ratings", type=Path, default=QAConfig.human_ratings)
    p.add_argument("--topics", nargs="+")
    p.add_argument("--limit-per-topic", type=int, default=100)
    p.add_argument("--batch-size", type=int, default=QAConfig.batch_size)
    p.add_argument("--max-attempts-per-topic", type=int, default=QAConfig.max_attempts_per_topic)
    p.add_argument("--max-calls", type=int, default=5000, help="Pedidos lógicos, somados entre todos os papéis")
    p.add_argument("--max-consecutive-api-failures", type=int, default=3)
    p.add_argument("--max-refinements", type=int, default=2)
    p.add_argument("--minimum-quality", type=float, default=QAConfig.minimum_quality)
    p.add_argument('--minimum-technical',type=float,default=QAConfig.minimum_technical)
    p.add_argument('--minimum-domain',type=float,default=QAConfig.minimum_domain)
    p.add_argument("--minimum-fewshot-quality", type=float, default=.85)
    p.add_argument("--format-examples", type=int, default=8)
    p.add_argument("--cross-topic-examples", type=int, default=4)
    p.add_argument("--embedding-model", default=QAConfig.embedding_model)
    p.add_argument("--clusters", type=int, default=24)
    p.add_argument("--similarity-threshold", type=float, default=.85,
                   help="Limiar observado; só filtra com --enable-cosine-filter")
    p.add_argument("--enable-cosine-filter", action="store_true", help="Experimento FUTURO: ativa rejeição por cosine")
    p.add_argument("--enable-saturation-stop", action="store_true", help="Ativa parada por cobertura, novidade e recuperação")
    p.add_argument('--enable-redundancy-filter',dest='filter_redundancy',action='store_true',help='Descarta redundância confirmada pelo avaliador do par')
    p.add_argument('--redundancy-neighbors',type=int,default=QAConfig.redundancy_neighbors)
    p.add_argument('--redundancy-confidence',type=float,default=QAConfig.redundancy_confidence)
    p.add_argument('--embedding-overlap-tokens',type=int,default=QAConfig.embedding_overlap_tokens)
    p.add_argument('--coverage-fraction',type=float,default=QAConfig.coverage_fraction)
    p.add_argument('--minimum-subtopic-candidates',type=int,default=QAConfig.minimum_subtopic_candidates)
    p.add_argument('--novelty-window',type=int,default=QAConfig.novelty_window)
    p.add_argument('--novelty-patience',type=int,default=QAConfig.novelty_patience)
    p.add_argument('--minimum-novelty-yield',type=float,default=QAConfig.minimum_novelty_yield)
    p.add_argument('--recovery-candidates',type=int,default=QAConfig.recovery_candidates)
    p.add_argument("--entropy-gain-threshold", type=float, default=QAConfig.entropy_gain_threshold)
    p.add_argument("--entropy-patience", type=int, default=QAConfig.entropy_patience)
    p.add_argument("--entropy-warmup", type=int, default=12)
    p.add_argument("--observe-only", action="store_true", help="Explicita que cosine e saturação ficam desligados")
    p.add_argument("--no-embeddings", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--resume", action="store_true")
    p.add_argument("--prepare-only", action="store_true")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--list-topics", action="store_true")
    p.add_argument("--print-prompt", action="store_true")
    p.add_argument('--print-difficulty-prompt',action='store_true')
    p.add_argument('--print-judge-prompt',action='store_true')
    p.add_argument('--print-source-audit-prompt',action='store_true')
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
    for name in ('minimum_technical','minimum_domain','filter_redundancy','redundancy_neighbors','redundancy_confidence',
                 'embedding_overlap_tokens','coverage_fraction','minimum_subtopic_candidates','novelty_window',
                 'novelty_patience','minimum_novelty_yield','recovery_candidates'):
        setattr(cfg,name,getattr(args,name))
    cfg.preparation_deployment = args.preparation_deployment or args.deployment
    cfg.judge_deployment = args.judge_deployment or args.deployment
    cfg.corpus_manifest=args.corpus_manifest
    cfg.allow_sample_corpus=args.allow_sample_corpus
    cfg.lexical_candidates_per_collection=args.lexical_candidates_per_collection
    if args.corpus_manifest is not None:cfg.corpus_dir=None
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
    if args.observe_only and (args.enable_cosine_filter or args.enable_saturation_stop or args.filter_redundancy):
        p.error("--observe-only não pode ser combinado com os filtros ativos")
    if args.list_topics:
        for topic in TOPICOS:
            print(topic)
        return
    if args.print_difficulty_prompt:
        from pipeline.fase_4.difficulty import SYSTEM_PROMPT as prompt
        print(prompt);return
    if args.print_source_audit_prompt:
        from pipeline.fase_4.source_audit import SYSTEM_PROMPT as prompt
        print(prompt);return
    if args.print_judge_prompt:
        from pipeline.fase_4.prompts_qa import judge_prompt
        print(judge_prompt([],{'topic':'{topic}','subtopic':'{subtopic}','scope':'{scope}',
                              'document':'{audited_document}','chunks':[],'source_audit':{}})[0]);return
    if args.print_prompt:
        print(SYSTEM_PROMPT)
        print(build_prompt(topic="{topic}", subtopic="{subtopic}", difficulty="{difficulty}",
              scope="{scope}", focus="{focus}", document="{document}",
              chunks=[{"chunk_id": "{chunk_id}", "texto": "{original_domain_text}"}],
              format_examples=[{"question": "{external_question}", "answer": "{external_answer}"}],
              quality_examples=[{"question": "{best_rated_question}", "answer": "{best_rated_answer}"}],
              previous_questions=["{previous_questions}"], used_concepts=["{used_concepts}"],
              count="{count}", batch_id="{batch_id}",
              source_audit={'claims':'{supported_claims}','limitations':'{application_limits}'},
              generation_targets=[{'target_id':'{target_id}','description':'{audited_knowledge_target}'}]))
        return
    cfg = config_from_args(args)
    print(f"Fluxo QA v3: auditoria -> exploração -> QA -> Judge/refino -> dificuldade -> novidade", flush=True)
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
