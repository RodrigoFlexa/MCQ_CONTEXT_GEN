"""Remove de `saida_fase3/` todas as questões de um tópico (ou subtópico).

Serve para regenerar um tópico do zero depois que o especialista reescreveu a
instrução dele em `topicos.py`: as questões antigas foram geradas a partir do
texto velho e não valem mais.

Uso, a partir da raiz do repositório (o padrão é SIMULAR, nada é escrito):

    python pipeline/fase_3/purgar_topico.py --topico "Gestão do Desempenho"
    python pipeline/fase_3/purgar_topico.py --topico "Gestão do Desempenho" --aplicar

O que é tocado, sempre com backup `.bak_purga_<timestamp>` ao lado:
  * `repositorio/questoes.jsonl`   linhas do tópico removidas
  * `repositorio/embeddings.npy`   mesmas posições removidas (se o arquivo existir)
  * `questoes_fase3.jsonl`         idem (export; é reescrito no fim da geração)
  * `estado/<hash>.json`           ids purgados saem do `ids_pool`; o arquivo é
                                   movido para `.removido_<timestamp>` se ficar vazio
  * `indices/facetas.jsonl`        facetas do tópico purgado saem do cache

O índice de candidatos do corpus (`indices/candidatos.jsonl`) NÃO é mexido: a
assinatura dele inclui o conjunto de facetas, então a próxima execução do
pipeline o refaz sozinha quando as facetas novas entrarem no lugar das antigas.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def hash_curto(*partes, n: int = 10) -> str:
    """Mesma função de `utils_fase3`, copiada para o script rodar sozinho."""
    h = hashlib.sha1("|".join(str(p) for p in partes).encode("utf-8"))
    return h.hexdigest()[:n]


def ler_jsonl(caminho: Path) -> list[dict]:
    if not caminho.exists():
        return []
    return [json.loads(l) for l in caminho.read_text(encoding="utf-8").splitlines()
            if l.strip()]


def escrever_jsonl(caminho: Path, linhas: list[dict]) -> None:
    with caminho.open("w", encoding="utf-8") as fh:
        for linha in linhas:
            fh.write(json.dumps(linha, ensure_ascii=False) + "\n")


def backup(caminho: Path, ts: str, aplicar: bool) -> None:
    if caminho.exists() and aplicar:
        shutil.copy2(caminho, caminho.with_name(caminho.name + f".bak_purga_{ts}"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--topico", required=True,
                        help="Nome EXATO do tópico como aparece nas questões já geradas.")
    parser.add_argument("--subtopico", default=None,
                        help="Restringe a purga a um subtópico do tópico.")
    parser.add_argument("--out-dir", type=Path, default=AQUI / "saida_fase3",
                        help="Diretório de saída da fase 3.")
    parser.add_argument("--aplicar", action="store_true",
                        help="Escreve as mudanças. Sem isso, apenas simula.")
    args = parser.parse_args()

    out = args.out_dir
    ts = time.strftime("%Y%m%d_%H%M%S")
    aplicar = args.aplicar
    modo = "APLICANDO" if aplicar else "SIMULANDO (use --aplicar para valer)"
    print(f"[{modo}] saída: {out}")

    def alvo(q: dict) -> bool:
        if q.get("topico") != args.topico:
            return False
        return args.subtopico is None or q.get("subtopico") == args.subtopico

    # ------------------------------------------------------ repositório --
    caminho_repo = out / "repositorio" / "questoes.jsonl"
    questoes = ler_jsonl(caminho_repo)
    if not questoes:
        raise SystemExit(f"nada lido em {caminho_repo}")

    manter = [i for i, q in enumerate(questoes) if not alvo(q)]
    remover = [i for i, q in enumerate(questoes) if alvo(q)]
    ids_purgados = {questoes[i]["id"] for i in remover}
    pares = sorted({(questoes[i].get("topico"), questoes[i].get("subtopico"))
                    for i in remover})

    print(f"repositório: {len(questoes)} questões · {len(remover)} a remover "
          f"· {len(manter)} a manter")
    for topico, subtopico in pares:
        n = sum(1 for i in remover if questoes[i].get("subtopico") == subtopico)
        print(f"  - {topico} >> {subtopico}: {n}")
    if not remover:
        raise SystemExit("nenhuma questão bate com o filtro — nada a fazer.")

    backup(caminho_repo, ts, aplicar)
    if aplicar:
        escrever_jsonl(caminho_repo, [questoes[i] for i in manter])

    # ------------------------------------------------------- embeddings --
    caminho_emb = out / "repositorio" / "embeddings.npy"
    if caminho_emb.exists():
        import numpy as np
        E = np.load(caminho_emb)
        if len(E) == len(questoes):
            print(f"embeddings.npy: {len(E)} -> {len(manter)} linhas")
            backup(caminho_emb, ts, aplicar)
            if aplicar:
                np.save(caminho_emb, E[np.asarray(manter, dtype=int)])
        else:
            print(f"embeddings.npy dessincronizado ({len(E)} x {len(questoes)}) "
                  f"— deixando como está; o Repositorio recalcula ao carregar.")
    else:
        print("embeddings.npy não existe (recalculado ao carregar o repositório).")

    # ----------------------------------------------------------- export --
    caminho_export = out / "questoes_fase3.jsonl"
    export = ler_jsonl(caminho_export)
    if export:
        restante = [q for q in export if q.get("id") not in ids_purgados]
        print(f"questoes_fase3.jsonl: {len(export)} -> {len(restante)}")
        backup(caminho_export, ts, aplicar)
        if aplicar:
            escrever_jsonl(caminho_export, restante)

    # ----------------------------------------------------------- estado --
    # O estado é indexado por hash do NOME do subtópico, então um mesmo arquivo
    # pode servir a dois tópicos que usam o mesmo nome (era o caso de "Geral",
    # compartilhado entre Gestão do Desempenho e Descomissionamento). Por isso
    # aqui não se apaga por tópico: filtra-se o `ids_pool` pelos ids purgados e
    # só se move o arquivo se ele ficar sem nenhuma questão.
    dono_restante = {}
    for q in (questoes[i] for i in manter):
        dono_restante.setdefault(q.get("subtopico"), q.get("topico"))

    for caminho in sorted((out / "estado").glob("*.json")):
        est = json.loads(caminho.read_text(encoding="utf-8"))
        pool = est.get("ids_pool", [])
        novo = [i for i in pool if i not in ids_purgados]
        if len(novo) == len(pool):
            continue
        if novo:
            dono = dono_restante.get(est.get("subtopico"), est.get("topico"))
            print(f"estado {caminho.name} ('{est.get('subtopico')}'): "
                  f"ids_pool {len(pool)} -> {len(novo)} · tópico "
                  f"'{est.get('topico')}' -> '{dono}'")
            est["ids_pool"] = novo
            est["topico"] = dono
            backup(caminho, ts, aplicar)
            if aplicar:
                caminho.write_text(json.dumps(est, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
        else:
            destino = caminho.with_name(caminho.name + f".removido_{ts}")
            print(f"estado {caminho.name} ('{est.get('subtopico')}'): "
                  f"ficou vazio -> {destino.name}")
            if aplicar:
                caminho.rename(destino)

    # ---------------------------------------------------------- facetas --
    caminho_fac = out / "indices" / "facetas.jsonl"
    facetas = ler_jsonl(caminho_fac)
    if facetas:
        ids_sub = {hash_curto(t, s) for t, s in pares}
        restante = [f for f in facetas if f.get("subtopico_id") not in ids_sub]
        print(f"facetas.jsonl: {len(facetas)} -> {len(restante)} "
              f"({len(facetas) - len(restante)} facetas do tópico purgado)")
        backup(caminho_fac, ts, aplicar)
        if aplicar:
            escrever_jsonl(caminho_fac, restante)

    print()
    if aplicar:
        print(f"pronto. backups com sufixo .bak_purga_{ts} / .removido_{ts}")
        print("próximo passo: rodar o pipeline com --topico no tópico novo "
              "(as facetas e o índice de candidatos são refeitos sozinhos).")
    else:
        print("nada foi escrito. repita com --aplicar quando os números acima "
              "estiverem como você espera.")


if __name__ == "__main__":
    main()
