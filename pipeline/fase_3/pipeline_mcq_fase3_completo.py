"""Executa o pipeline completo da fase 3 fora do Jupyter.

Uso, a partir da raiz do repositório:
    python pipeline/fase_3/pipeline_mcq_fase3_completo.py

Para validar o fluxo com poucos subtópicos:
    python pipeline/fase_3/pipeline_mcq_fase3_completo.py \
        --subtopico "nome exato do subtópico"
"""

from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(RAIZ))

import seed_fase3 as S
import utils_fase3 as U
from azure_openai_backend import AzureOpenAIBackend
from topicos import TOPICOS


def selecionar_subtopicos(nomes: list[str] | None) -> list[tuple[str, str]]:
    todos = [(topico, subtopico)
             for topico, subtopicos in TOPICOS.items()
             for subtopico in subtopicos]
    if not nomes:
        return todos

    por_nome = {subtopico: (topico, subtopico)
                for topico, subtopico in todos}
    desconhecidos = [nome for nome in nomes if nome not in por_nome]
    if desconhecidos:
        disponiveis = ", ".join(sorted(por_nome))
        raise ValueError(
            "Subtópico(s) desconhecido(s): " + ", ".join(desconhecidos)
            + "\nDisponíveis: " + disponiveis
        )
    return [por_nome[nome] for nome in nomes]


def construir_config(out_dir: Path) -> U.Config:
    return U.Config(
        raiz=RAIZ,
        corpus_dir=RAIZ / "dataset" / "corpus-SemProcessamento-publico-PetrolesCompleto",
        out_dir=out_dir,
        modelo_forte="gpt-5-4-petrobras",
        modelo_leve="gpt-5-mini-petrobras",
        pausa_entre_lotes=10.0,
        pausa_entre_etapas=2.0,
    )


def exportar(repo: U.Repositorio, cfg: U.Config) -> None:
    destino = cfg.out_dir / "questoes_fase3.jsonl"
    with destino.open("w", encoding="utf-8") as arquivo:
        for questao in repo.questoes:
            arquivo.write(json.dumps(questao, ensure_ascii=False) + "\n")

    print(f"{len(repo)} questões -> {destino}", flush=True)
    print(f"embeddings           -> {repo.caminho_emb}", flush=True)
    print(f"estado por subtópico -> {cfg.out_dir / 'estado'}", flush=True)
    print(f"log de rodadas       -> {cfg.out_dir / 'logs' / 'rodadas.jsonl'}",
          flush=True)


def executar(subtopicos: list[str] | None = None,
             out_dir: Path | None = None) -> None:
    cfg = construir_config(out_dir or AQUI / "saida_fase3")
    escopo = selecionar_subtopicos(subtopicos)

    print(f"raiz: {RAIZ}", flush=True)
    print(f"tópicos: {len(TOPICOS)} · subtópicos selecionados: {len(escopo)}",
          flush=True)
    print(cfg.resumo(), flush=True)

    llm_leve = AzureOpenAIBackend(
        deployment=cfg.modelo_leve,
        max_tokens=3000,
        request_timeout=300.0,
    )
    llm_gerador = AzureOpenAIBackend(
        deployment='gpt-5-2-petrobras',
        max_tokens=12000,
        reasoning_effort=cfg.gerador_reasoning_effort,
        request_timeout=300.0,
    )
    llm_judge = AzureOpenAIBackend(
        deployment='gpt-5-2-petrobras',
        max_tokens=8000,
        reasoning_effort=cfg.judge_reasoning_effort,
        request_timeout=300.0,
    )
    llm_leve.doctor()

    dir_fase2 = RAIZ / "pipeline" / "fase_2" / "questionarios" / "respostas_questionario"
    banco_seed = S.construir_banco_seed(dir_fase2, min_nota_humana=0.5)
    S.salvar_banco_seed(banco_seed, cfg.out_dir / "banco_seed.jsonl")
    print(f"{len(banco_seed)} questões no banco seed", flush=True)

    historicos = {}
    for caminho in glob.glob(str(cfg.out_dir / "estado" / "*.json")):
        estado = json.loads(Path(caminho).read_text(encoding="utf-8"))
        if len(estado.get("historico_entropia", [])) >= 3:
            historicos[estado["subtopico"]] = estado["historico_entropia"]
    if historicos:
        cfg.limiar_ganho_entropia = U.sugerir_limiar_entropia(
            historicos, percentil=75)
        print(f"adotando limiar calibrado: {cfg.limiar_ganho_entropia:.4f}",
              flush=True)
    else:
        print("nenhum estado de piloto encontrado; mantendo o default do Config: "
              f"{cfg.limiar_ganho_entropia:.4f}", flush=True)

    facetas = U.extrair_facetas(llm_leve, TOPICOS, cfg,
                                subtopicos_alvo=escopo)
    por_sub = U.agrupar_por_subtopico(facetas)
    print(f"{len(facetas)} facetas em {len(por_sub)} subtópicos", flush=True)

    U.descrever_corpus(cfg)
    U.varrer_corpus(facetas, cfg)
    candidatos = U.carregar_candidatos(cfg)
    print(f"{sum(len(v) for v in candidatos.values()):,} candidatos em "
          f"{len(candidatos)} facetas", flush=True)

    emb = U.Embedder(cfg)
    planos = {
        subtopico: U.plano_de_documentos(fs, candidatos, emb, cfg)
        for subtopico, fs in por_sub.items()
    }
    sugerido = U.calibrar_tolerancias(banco_seed, emb, cfg, percentil=75)
    cfg.tol_similaridade = sugerido["similaridade"]
    cfg.tol_comprimento = sugerido["comprimento"]
    cfg.tol_distratores = sugerido["distratores"]
    codebooks = {
        subtopico: U.codebook_do_subtopico(subtopico, fs, candidatos, emb, cfg)
        for subtopico, fs in por_sub.items()
    }

    repo = U.Repositorio(cfg, emb)
    pool = U.PoolFewShot(banco_seed, repo, cfg)
    print(f"repositório: {len(repo)} questões já armazenadas", flush=True)

    for topico, subtopico in escopo:
        U.executar_subtopico(
            subtopico=subtopico,
            topico=topico,
            facetas=por_sub[subtopico],
            plano=planos[subtopico],
            llm_leve=llm_leve,
            llm_forte=llm_gerador,
            llm_judge=llm_judge,
            pool=pool,
            repo=repo,
            emb=emb,
            codebook=codebooks[subtopico],
            cfg=cfg,
        )
        repo.salvar()
        print(f"concluído: {subtopico} · repositório: {len(repo)} questões",
              flush=True)

    exportar(repo, cfg)
    print("uso de tokens:", flush=True)
    for nome, llm in [("leve", llm_leve), ("gerador", llm_gerador),
                      ("judge", llm_judge)]:
        uso = llm.usage
        print(f"  {nome:<8} {uso.calls:>4} chamadas ({uso.cached_calls} de cache) · "
              f"{uso.prompt_tokens:>9,} in · {uso.completion_tokens:>8,} out",
              flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--subtopico",
        action="append",
        dest="subtopicos",
        help="Subtópico exato a processar; pode ser repetido. O padrão é todos.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        help="Diretório de saída; o padrão é pipeline/fase_3/saida_fase3.",
    )
    args = parser.parse_args()
    executar(args.subtopicos, args.out_dir)


if __name__ == "__main__":
    main()