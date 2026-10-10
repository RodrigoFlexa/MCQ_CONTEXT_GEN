"""Fase 5 — filtragem do dataset pela semelhança com o texto do especialista.

As questões da fase 3 foram geradas a partir de facetas extraídas das instruções
do especialista; depois da revisão, o especialista reescreveu essas instruções em
versões mais curtas. Esta fase mede, questão a questão, o quanto ela se parece
com o texto da referência do PRÓPRIO subtópico e permite cortar o dataset em
diferentes limiares de semelhança, observando quanto sobra de fácil, média e
difícil.

Decisões de desenho (set/2026, combinadas com o usuário):
  * referência = "Versão compacta" quando existe, senão "Versão resumida",
    senão a descrição longa (ver `extrair_referencias.py`, que também descarta
    variante copiada de outro subtópico);
  * texto da questão = enunciado + TODAS as alternativas, para capturar também o
    vocabulário dos distratores;
  * cada questão é comparada apenas com a referência do subtópico em que foi
    gerada — a métrica é aderência ao que o especialista pediu ali, não
    reclassificação;
  * dificuldade = campo `difficulty` da própria geração (juiz da fase 3), não a
    reavaliação da fase 4;
  * embeddings: mesmo modelo do resto do projeto
    (`paraphrase-multilingual-MiniLM-L12-v2`), via `utils_fase3.Embedder`, com
    cache em disco próprio da fase 5.

Uso, a partir da raiz do repositório:

    python pipeline/fase_5/filtragem_fase5.py                     # varredura
    python pipeline/fase_5/filtragem_fase5.py --exportar 0.45     # + dataset filtrado

Saídas em `pipeline/fase_5/saida_fase5/`:
    similaridades.csv          uma linha por questão, com a similaridade
    varredura_limiares.csv     quanto sobra em cada limiar, por dificuldade
    varredura_por_subtopico.csv  o mesmo, quebrado por subtópico
    questoes_filtradas_<limiar>.jsonl   dataset cortado (com --exportar)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(RAIZ / "pipeline" / "fase_3"))

DIFICULDADES = ("facil", "media", "dificil")
LIMIARES_PADRAO = tuple(round(x, 2) for x in np.arange(0.0, 0.81, 0.05))


# ===========================================================================
# entrada
# ===========================================================================

def carregar_referencias(caminho: Path) -> dict[tuple[str, str], dict]:
    dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
    return {(r["topico"], r["subtopico"]): r for r in dados["referencias"]}


def carregar_questoes(caminho: Path) -> list[dict]:
    return [json.loads(l) for l in Path(caminho).read_text(encoding="utf-8").splitlines()
            if l.strip()]


def texto_da_questao(questao: dict, modo: str = "enunciado+alternativas") -> str:
    stem = questao["stem"]
    alternativas = questao.get("alternatives") or []
    if modo == "enunciado":
        return stem
    if modo == "enunciado+correta":
        i = int(questao["correct_answer_index"])
        return f"{stem} {alternativas[i]}"
    return " ".join([stem, *alternativas])


# ===========================================================================
# similaridade
# ===========================================================================

def construir_embedder(out_dir: Path, verbose: bool = True):
    """`utils_fase3.Embedder` com cache próprio da fase 5 (mesmo modelo)."""
    import utils_fase3 as U
    cfg = U.Config(raiz=RAIZ, out_dir=out_dir)
    # `Config.__post_init__` cria a árvore de pastas da fase 3; aqui só o cache
    # de embeddings é usado, então as outras saem se estiverem vazias.
    for sub in ("indices", "documentos", "estado", "repositorio", "logs"):
        caminho = out_dir / sub
        if caminho.is_dir() and not any(caminho.iterdir()):
            caminho.rmdir()
    return U.Embedder(cfg, verbose=verbose)


def embeddings_das_questoes(questoes: list[dict], emb,
                            modo_texto: str = "enunciado+alternativas",
                            verbose: bool = True) -> np.ndarray:
    """Matriz (n, dim) com os mesmos textos usados na similaridade."""
    return emb.encode([texto_da_questao(q, modo_texto) for q in questoes],
                      progresso=verbose)


def calcular_similaridades(questoes: list[dict],
                           referencias: dict[tuple[str, str], dict],
                           emb,
                           modo_texto: str = "enunciado+alternativas",
                           verbose: bool = True) -> pd.DataFrame:
    """Cosseno entre cada questão e a referência do próprio subtópico.

    Os vetores do `Embedder` já saem normalizados, então o cosseno é o produto
    interno. As referências são poucas (uma por subtópico) e entram todas de uma
    vez; as questões vão em lote, com cache em disco.
    """
    chaves = sorted({(r["topico"], r["subtopico"]) for r in referencias.values()})
    textos_ref = [referencias[c]["texto"] or "" for c in chaves]
    sem_texto = [c for c, t in zip(chaves, textos_ref) if not t]
    if sem_texto:
        raise ValueError(f"referência sem texto: {sem_texto}")
    E_ref = emb.encode(textos_ref)
    idx_ref = {c: i for i, c in enumerate(chaves)}

    orfas: dict[tuple[str, str], int] = {}
    usaveis = []
    for q in questoes:
        chave = (q.get("topico"), q.get("subtopico"))
        if chave not in idx_ref:
            orfas[chave] = orfas.get(chave, 0) + 1
            continue
        usaveis.append(q)
    if orfas and verbose:
        print("questões sem referência (ignoradas):")
        for chave, n in sorted(orfas.items(), key=lambda kv: -kv[1]):
            print(f"  {n:6d}  {chave[0]} >> {chave[1]}")

    E_q = emb.encode([texto_da_questao(q, modo_texto) for q in usaveis],
                     progresso=verbose)
    linhas_ref = np.array([idx_ref[(q["topico"], q["subtopico"])] for q in usaveis])
    sim = np.einsum("ij,ij->i", E_q, E_ref[linhas_ref])

    df = pd.DataFrame({
        "id": [q["id"] for q in usaveis],
        "topico": [q["topico"] for q in usaveis],
        "subtopico": [q["subtopico"] for q in usaveis],
        "dificuldade": [q.get("difficulty") for q in usaveis],
        "nota": [q.get("nota") for q in usaveis],
        "similaridade": sim.astype(float),
    })
    df["variante_referencia"] = [
        referencias[(t, s)]["variante_escolhida"]
        for t, s in zip(df["topico"], df["subtopico"])]
    df["minimo_subtopico"] = [
        referencias[(t, s)].get("minimo_questoes")
        for t, s in zip(df["topico"], df["subtopico"])]
    return df


# ===========================================================================
# varredura de limiares
# ===========================================================================

def varredura(df: pd.DataFrame, limiares=LIMIARES_PADRAO) -> pd.DataFrame:
    """Quanto sobra do dataset em cada limiar, por dificuldade."""
    total = len(df)
    linhas = []
    for limiar in limiares:
        mantidas = df[df["similaridade"] >= limiar]
        linha = {"limiar": limiar, "questoes": len(mantidas),
                 "frac_do_total": len(mantidas) / total if total else 0.0}
        for nivel in DIFICULDADES:
            n = int((mantidas["dificuldade"] == nivel).sum())
            linha[nivel] = n
            linha[f"frac_{nivel}"] = n / len(mantidas) if len(mantidas) else 0.0
        linha["subtopicos_com_questao"] = mantidas["subtopico"].nunique()
        linhas.append(linha)
    return pd.DataFrame(linhas)


def varredura_por_subtopico(df: pd.DataFrame, limiares=LIMIARES_PADRAO) -> pd.DataFrame:
    """O mesmo corte, subtópico a subtópico, com o piso pedido no docx."""
    linhas = []
    for (topico, subtopico), g in df.groupby(["topico", "subtopico"], sort=True):
        minimo = g["minimo_subtopico"].iloc[0]
        for limiar in limiares:
            mantidas = g[g["similaridade"] >= limiar]
            linha = {"topico": topico, "subtopico": subtopico, "limiar": limiar,
                     "questoes": len(mantidas), "total_subtopico": len(g),
                     "minimo_topico_docx": minimo}
            for nivel in DIFICULDADES:
                linha[nivel] = int((mantidas["dificuldade"] == nivel).sum())
            linhas.append(linha)
    return pd.DataFrame(linhas)


def piso_por_topico(df: pd.DataFrame, referencias: dict, limiar: float) -> pd.DataFrame:
    """Compara o que sobra em cada TÓPICO com o mínimo pedido no docx.

    Os números do docx ("600 questões") são por tópico e são piso, não cota.
    """
    minimos = {}
    for (topico, _), ref in referencias.items():
        if ref.get("minimo_questoes"):
            minimos[topico] = ref["minimo_questoes"]
    mantidas = df[df["similaridade"] >= limiar]
    linhas = []
    for topico, g in mantidas.groupby("topico", sort=True):
        minimo = minimos.get(topico)
        linhas.append({"topico": topico, "limiar": limiar, "questoes": len(g),
                       "minimo_docx": minimo,
                       "atende": None if minimo is None else len(g) >= minimo,
                       **{nivel: int((g["dificuldade"] == nivel).sum())
                          for nivel in DIFICULDADES}})
    return pd.DataFrame(linhas)


def limiar_para_piso(df: pd.DataFrame, referencias: dict,
                     limiares=LIMIARES_PADRAO) -> float | None:
    """Maior limiar da grade em que TODOS os tópicos ainda atendem o piso."""
    melhor = None
    for limiar in sorted(limiares):
        tabela = piso_por_topico(df, referencias, limiar)
        if tabela.empty:
            break
        atende = tabela["atende"].dropna()
        if len(atende) and bool(atende.all()):
            melhor = limiar
    return melhor


def filtrar_com_piso(df: pd.DataFrame, referencias: dict, limiar: float,
                     ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Corta em `limiar`, mas nunca abaixo do piso do docx em cada tópico.

    O limiar é o corte mais RIGOROSO que se admite: nenhum tópico é podado além
    dele. Quando um tópico não tem questões parecidas o bastante para chegar ao
    seu piso, ele para de ser podado antes — ficam as `minimo` questões mais
    parecidas dele, o que equivale a um limiar efetivo mais baixo só ali.

    Devolve (questões mantidas, relatório por tópico). O relatório traz o limiar
    efetivo de cada tópico: onde ele for menor que o pedido, o piso é que mandou.
    """
    minimos = {topico: ref["minimo_questoes"]
               for (topico, _), ref in referencias.items()
               if ref.get("minimo_questoes")}

    partes, relatorio = [], []
    for topico, g in df.groupby("topico", sort=True):
        acima = g[g["similaridade"] >= limiar]
        minimo = minimos.get(topico)
        if minimo is not None and len(acima) < minimo:
            mantidas = g.nlargest(min(minimo, len(g)), "similaridade")
            motivo = "piso" if len(mantidas) >= minimo else "esgotado"
        else:
            mantidas = acima
            motivo = "limiar"
        efetivo = float(mantidas["similaridade"].min()) if len(mantidas) else float("nan")
        partes.append(mantidas)
        relatorio.append({
            "topico": topico, "total": len(g), "questoes": len(mantidas),
            "minimo_docx": minimo, "acima_do_limiar": len(acima),
            "limiar_pedido": limiar, "limiar_efetivo": round(efetivo, 4),
            "criterio": motivo,
            **{nivel: int((mantidas["dificuldade"] == nivel).sum())
               for nivel in DIFICULDADES},
        })

    mantidas = pd.concat(partes).sort_values("similaridade", ascending=False)
    return mantidas, pd.DataFrame(relatorio).sort_values("questoes", ascending=False)


def filtrar_por_cota_cluster(df: pd.DataFrame, E: np.ndarray, alvos: dict[str, int],
                             piso: float = 0.45, k: int = 24, seed: int = 42,
                             verbose: bool = True,
                             ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Piso de relevância como filtro duro, cota por cluster entre os sobreviventes.

    Dois estágios, que respondem a duas perguntas diferentes:

    1. **Piso**: `similaridade >= piso` elimina o que o especialista disse para não
       abordar. É filtro duro — nenhuma questão abaixo do piso entra em nada, nem
       para preencher cota. Cluster cujas questões estão todas abaixo do piso
       simplesmente desaparece, e é esse o efeito pretendido do texto revisado.
    2. **Cota**: entre os sobreviventes, o subtópico é clusterizado (k-means sobre
       os embeddings das próprias questões, o mesmo k do codebook da fase 3) e a
       seleção pega as mais parecidas de CADA cluster até o alvo, em vez das mais
       parecidas do subtópico inteiro. É o que preserva a variabilidade semântica:
       ordenar só por similaridade concentra a seleção em volta do centroide da
       referência.

    `alvos` é o número de questões desejado por subtópico (normalmente o que o
    corte por limiar dava, para manter o tamanho comparável).

    Devolve (mantidas, relatório por subtópico, clusters eliminados pelo piso).
    """
    from sklearn.cluster import KMeans

    if len(E) != len(df):
        raise ValueError(f"embeddings ({len(E)}) e similaridades ({len(df)}) "
                         f"não batem — recalcule na mesma ordem das questões")

    escolhidos: list[int] = []
    relatorio, mortos = [], []
    for subtopico, g in df.groupby("subtopico", sort=True):
        idx = g.index.to_numpy()
        sims = g["similaridade"].to_numpy()
        alvo = int(alvos.get(subtopico, 0))
        if alvo <= 0:
            continue

        k_sub = max(2, min(k, len(idx) // 8))
        rotulos = KMeans(n_clusters=k_sub, random_state=seed,
                         n_init=10).fit(E[idx]).labels_

        elegiveis = np.where(sims >= piso)[0]
        if len(elegiveis) < alvo and verbose:
            print(f"  [aviso] '{subtopico}': só {len(elegiveis)} acima do piso "
                  f"{piso:.2f} para um alvo de {alvo} — o alvo manda, o piso "
                  f"seria furado; mantendo as {alvo} mais parecidas")
        if len(elegiveis) < alvo:
            elegiveis = np.argsort(-sims)[:alvo]

        # cota igual por cluster, sobras preenchidas pelas mais parecidas
        por_cluster = max(1, alvo // max(1, len(set(rotulos[elegiveis]))))
        sel: list[int] = []
        for c in sorted(set(rotulos[elegiveis])):
            do_cluster = elegiveis[rotulos[elegiveis] == c]
            sel.extend(do_cluster[np.argsort(-sims[do_cluster])][:por_cluster])
        if len(sel) < alvo:
            resto = [i for i in elegiveis[np.argsort(-sims[elegiveis])]
                     if i not in set(sel)]
            sel.extend(resto[:alvo - len(sel)])
        sel = np.array(sel[:alvo], dtype=int)
        escolhidos.extend(idx[sel])

        vivos = set(rotulos[elegiveis])
        for c in range(k_sub):
            do_cluster = np.where(rotulos == c)[0]
            if len(do_cluster) and c not in vivos:
                mortos.append({
                    "subtopico": subtopico, "cluster": int(c),
                    "questoes": int(len(do_cluster)),
                    "sim_media": round(float(sims[do_cluster].mean()), 4),
                    "sim_maxima": round(float(sims[do_cluster].max()), 4),
                    "exemplo_id": df.loc[idx[do_cluster[np.argmax(sims[do_cluster])]], "id"],
                })

        relatorio.append({
            "topico": g["topico"].iloc[0], "subtopico": subtopico,
            "total": len(idx), "acima_do_piso": int((sims >= piso).sum()),
            "alvo": alvo, "mantidas": len(sel),
            "clusters": k_sub, "clusters_vivos": len(vivos),
            "clusters_eliminados": k_sub - len(vivos),
            "sim_media": round(float(sims[sel].mean()), 4),
            "sim_minima": round(float(sims[sel].min()), 4),
            **{nivel: int((g["dificuldade"].to_numpy()[sel] == nivel).sum())
               for nivel in DIFICULDADES},
        })

    return (df.loc[escolhidos].sort_values("similaridade", ascending=False),
            pd.DataFrame(relatorio), pd.DataFrame(mortos))


def alvos_do_corte(df: pd.DataFrame, referencias: dict,
                   limiar: float) -> dict[str, int]:
    """Alvo por subtópico = o que o corte por limiar com piso do docx daria.

    Serve para comparar métodos com o MESMO tamanho de dataset.
    """
    mantidas, _ = filtrar_com_piso(df, referencias, limiar)
    return mantidas.groupby("subtopico").size().to_dict()


def exportar_filtrado(df: pd.DataFrame, questoes: list[dict], limiar: float,
                      destino: Path, ids: set[str] | None = None) -> int:
    """Grava o dataset cortado, com a similaridade anotada em cada questão.

    `ids` permite gravar uma seleção já pronta (por exemplo a de
    `filtrar_com_piso`); sem ela, o corte é o limiar simples.
    """
    sim_por_id = dict(zip(df["id"], df["similaridade"]))
    manter = set(ids) if ids is not None else {
        i for i, s in sim_por_id.items() if s >= limiar}
    n = 0
    with Path(destino).open("w", encoding="utf-8") as fh:
        for q in questoes:
            if q["id"] in manter:
                saida = dict(q)
                saida["similaridade_especialista"] = round(float(sim_por_id[q["id"]]), 4)
                saida["limiar_fase5"] = limiar
                fh.write(json.dumps(saida, ensure_ascii=False) + "\n")
                n += 1
    return n


# ===========================================================================
# CLI
# ===========================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--questoes", type=Path,
                        default=RAIZ / "pipeline" / "fase_3" / "saida_fase3" / "questoes_fase3.jsonl")
    parser.add_argument("--referencias", type=Path,
                        default=AQUI / "referencias_especialista.json")
    parser.add_argument("--out-dir", type=Path, default=AQUI / "saida_fase5")
    parser.add_argument("--texto", default="enunciado+alternativas",
                        choices=["enunciado", "enunciado+correta",
                                 "enunciado+alternativas"])
    parser.add_argument("--limiares", default=None,
                        help="Lista separada por vírgula; o padrão é 0.00 a 0.80 de 0.05 em 0.05.")
    parser.add_argument("--similaridades", type=Path, default=None,
                        help="Reaproveita um similaridades.csv já calculado "
                             "(pula os embeddings, que levam minutos).")
    parser.add_argument("--exportar", type=float, default=None,
                        help="Grava também o dataset filtrado neste limiar.")
    parser.add_argument("--cota-cluster", action="store_true",
                        help="Seleciona por cota de cluster entre as questões "
                             "acima de --piso, com o tamanho que --exportar daria.")
    parser.add_argument("--piso", type=float, default=0.45,
                        help="Piso de relevância da cota por cluster (padrão 0,45).")
    parser.add_argument("--respeitar-piso", action="store_true",
                        help="No --exportar, nenhum tópico é podado abaixo do "
                             "mínimo do docx: onde faltar, ficam as N mais "
                             "parecidas (limiar efetivo menor só naquele tópico).")
    args = parser.parse_args()

    limiares = (tuple(float(x) for x in args.limiares.split(","))
                if args.limiares else LIMIARES_PADRAO)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    referencias = carregar_referencias(args.referencias)
    questoes = carregar_questoes(args.questoes)
    print(f"{len(questoes)} questões · {len(referencias)} referências")

    if args.similaridades:
        df = pd.read_csv(args.similaridades)
        print(f"similaridades lidas de {args.similaridades} "
              f"({len(df)} linhas) — embeddings não recalculados")
    else:
        emb = construir_embedder(args.out_dir)
        df = calcular_similaridades(questoes, referencias, emb, args.texto)
        emb.salvar_cache()
        df.to_csv(args.out_dir / "similaridades.csv", index=False)

    tabela = varredura(df, limiares)
    tabela.to_csv(args.out_dir / "varredura_limiares.csv", index=False)

    por_sub = varredura_por_subtopico(df, limiares)
    por_sub.to_csv(args.out_dir / "varredura_por_subtopico.csv", index=False)

    print("\nsimilaridade: "
          f"min {df['similaridade'].min():.3f} · "
          f"p25 {df['similaridade'].quantile(.25):.3f} · "
          f"mediana {df['similaridade'].median():.3f} · "
          f"p75 {df['similaridade'].quantile(.75):.3f} · "
          f"max {df['similaridade'].max():.3f}")
    print("\nvarredura de limiares:")
    print(tabela.to_string(index=False,
                           formatters={"frac_do_total": "{:.1%}".format,
                                       "frac_facil": "{:.1%}".format,
                                       "frac_media": "{:.1%}".format,
                                       "frac_dificil": "{:.1%}".format}))

    piso = limiar_para_piso(df, referencias, limiares)
    if piso is None:
        print("\nnenhum limiar da grade mantém todos os tópicos acima do piso do docx.")
    else:
        print(f"\nmaior limiar da grade em que todo tópico ainda atende o piso "
              f"do docx: {piso:.2f}")
        print(piso_por_topico(df, referencias, piso).to_string(index=False))

    if args.exportar is not None and args.cota_cluster:
        emb = construir_embedder(args.out_dir)
        E = embeddings_das_questoes(questoes, emb)
        emb.salvar_cache()
        ordem = {q["id"]: i for i, q in enumerate(questoes)}
        E = E[[ordem[i] for i in df["id"]]]

        alvos = alvos_do_corte(df, referencias, args.exportar)
        mantidas, relatorio, mortos = filtrar_por_cota_cluster(
            df, E, alvos, piso=args.piso)
        relatorio.to_csv(args.out_dir / "cota_cluster_relatorio.csv", index=False)
        mortos.to_csv(args.out_dir / "cota_cluster_clusters_eliminados.csv",
                      index=False)

        por_topico = (mantidas.groupby("topico")
                      .agg(questoes=("id", "size"),
                           sim_media=("similaridade", "mean"),
                           **{n: ("dificuldade", lambda s, n=n: (s == n).sum())
                              for n in DIFICULDADES})
                      .round(3))
        print("\npor tópico:")
        print(por_topico.to_string())
        print(f"\n{len(mortos)} clusters eliminados pelo piso {args.piso:.2f}")

        destino = (args.out_dir /
                   f"questoes_filtradas_cota_cluster_piso{args.piso:.2f}.jsonl")
        n = exportar_filtrado(df, questoes, args.piso, destino,
                              ids=set(mantidas["id"]))
        print(f"\n{n} questões -> {destino}")
    elif args.exportar is not None:
        if args.respeitar_piso:
            mantidas, relatorio = filtrar_com_piso(df, referencias, args.exportar)
            relatorio.to_csv(args.out_dir / f"piso_{args.exportar:.2f}.csv",
                             index=False)
            print(f"\ncorte em {args.exportar:.2f} com piso do docx:")
            print(relatorio.to_string(index=False))
            destino = (args.out_dir /
                       f"questoes_filtradas_{args.exportar:.2f}_com_piso.jsonl")
            n = exportar_filtrado(df, questoes, args.exportar, destino,
                                  ids=set(mantidas["id"]))
        else:
            destino = args.out_dir / f"questoes_filtradas_{args.exportar:.2f}.jsonl"
            n = exportar_filtrado(df, questoes, args.exportar, destino)
        print(f"\n{n} questões -> {destino}")


if __name__ == "__main__":
    main()
