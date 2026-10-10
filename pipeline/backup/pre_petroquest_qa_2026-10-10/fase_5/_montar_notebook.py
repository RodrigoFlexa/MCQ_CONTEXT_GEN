"""Gera filtragem_fase5.ipynb (rodar só quando o roteiro do notebook mudar)."""
import json
from pathlib import Path

def md(texto):
    return {"cell_type": "markdown", "metadata": {},
            "source": texto.strip("\n").splitlines(keepends=True)}

def code(texto):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": texto.strip("\n").splitlines(keepends=True)}

celulas = [
md("""
# Fase 5 — filtragem do dataset pela aderência ao texto do especialista

As questões da fase 3 nasceram das instruções longas de `topicos.py`. Depois da
revisão, o especialista reescreveu essas instruções em versões mais curtas
(*Versão resumida* e *Versão compacta*) no docx
**SUGESTÃO DE FRASES PARA COMPOR PROMPT MÚLTIPLA ESCOLHA V14 (09/09/26)**.
Esta fase mede o quanto cada questão se parece com a referência do próprio
subtópico e corta o dataset em diferentes limiares, observando quanto sobra de
fácil, média e difícil.

| decisão | escolha |
|---|---|
| referência | `Versão compacta` > `Versão resumida` > descrição longa |
| texto da questão | enunciado + **todas** as alternativas |
| comparação | cada questão contra a referência do **próprio** subtópico |
| dificuldade | campo `difficulty` da geração (juiz da fase 3) |
| embeddings | `paraphrase-multilingual-MiniLM-L12-v2`, o mesmo do resto do projeto |

O corte é por **limiar de similaridade do cosseno**: quanto maior o limiar, mais
parecida com o texto do especialista a questão precisa ser para permanecer.
Os números do docx (200, 600, 400…) são **piso por tópico**, então o limiar
máximo utilizável é o maior que ainda deixa todo tópico acima do seu piso.
"""),

code("""
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

AQUI = Path.cwd() if Path.cwd().name == "fase_5" else Path("pipeline/fase_5")
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(RAIZ / "pipeline" / "fase_3"))

import filtragem_fase5 as F

QUESTOES = RAIZ / "pipeline" / "fase_3" / "saida_fase3" / "questoes_fase3.jsonl"
REFERENCIAS = AQUI / "referencias_especialista.json"
SAIDA = AQUI / "saida_fase5"
SAIDA.mkdir(parents=True, exist_ok=True)

# cores fixas por dificuldade (paleta categórica validada, slots 1-3)
CORES = {"facil": "#2a78d6", "media": "#eb6834", "dificil": "#1baf7a"}
print(QUESTOES, QUESTOES.exists())
"""),

md("""
## 1. Referências do especialista

`extrair_referencias.py` lê o docx e guarda, por subtópico, as três variantes do
texto mais a escolhida. Rode-o de novo sempre que o especialista mandar um docx
novo:

```
python pipeline/fase_5/extrair_referencias.py
```

Ele também descarta variante copiada de outro subtópico — no V14 isso acontece em
*Operação de Separadores Trifásicos* e *Compressão de Gás*, cujas versões
resumida e compacta trazem o texto do subtópico vizinho. Nesses dois casos a
referência usada é a descrição longa, que está correta.
"""),

code("""
referencias = F.carregar_referencias(REFERENCIAS)
tabela_ref = pd.DataFrame([
    {"topico": r["topico"], "subtopico": r["subtopico"],
     "variante": r["variante_escolhida"], "caracteres": len(r["texto"] or ""),
     "minimo_docx": r["minimo_questoes"], "avisos": len(r["avisos"])}
    for r in referencias.values()
]).sort_values(["topico", "subtopico"])

print(tabela_ref["variante"].value_counts().to_string())
tabela_ref
"""),

code("""
# avisos de reconciliação (variante descartada, subtópico sem referência, ...)
for r in referencias.values():
    for aviso in r["avisos"]:
        print(f"[{r['subtopico'][:45]}] {aviso}")
"""),

md("""
## 2. Similaridade de cada questão com a sua referência

O `Embedder` é o mesmo da fase 3 (modelo multilíngue local, cache em disco). Os
vetores saem normalizados, então o cosseno é o produto interno. A primeira
execução leva alguns minutos; as seguintes reaproveitam o cache em
`saida_fase5/embeddings/`.
"""),

code("""
questoes = F.carregar_questoes(QUESTOES)
print(f"{len(questoes)} questões · {len(referencias)} referências")

emb = F.construir_embedder(SAIDA)
df = F.calcular_similaridades(questoes, referencias, emb,
                              modo_texto="enunciado+alternativas")
emb.salvar_cache()
df.to_csv(SAIDA / "similaridades.csv", index=False)
df.head()
"""),

code("""
print(df["similaridade"].describe().to_string())
"""),

md("""
## 3. Como a similaridade se distribui

Duas leituras importam aqui:

* a distribuição geral diz em que faixa o limiar faz sentido (um limiar acima do
  máximo observado zera o dataset, um abaixo do mínimo não filtra nada);
* a distribuição **por subtópico** diz se um limiar único é justo. Referências
  mais longas e genéricas tendem a puxar a similaridade para cima, então um
  limiar absoluto corta mais de uns subtópicos do que de outros. Se a diferença
  entre as medianas for grande, vale usar corte por quantil dentro de cada
  subtópico em vez de um número só (a última seção mostra como).
"""),

code("""
fig, ax = plt.subplots(figsize=(8, 3.4))
ax.hist(df["similaridade"], bins=60, color="#2a78d6", edgecolor="white", linewidth=0.4)
ax.set_xlabel("similaridade com a referência do subtópico (cosseno)")
ax.set_ylabel("questões")
ax.set_title("Distribuição da similaridade")
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)
ax.grid(axis="y", color="#e5e5e2", linewidth=0.8)
ax.set_axisbelow(True)
plt.tight_layout()
plt.show()
"""),

code("""
por_sub = (df.groupby(["topico", "subtopico"])["similaridade"]
             .agg(questoes="size", minimo="min", p25=lambda s: s.quantile(.25),
                  mediana="median", p75=lambda s: s.quantile(.75), maximo="max")
             .sort_values("mediana"))
por_sub.round(3)
"""),

md("""
## 4. Varredura de limiares

Para cada limiar da grade, quantas questões sobram no total e por dificuldade.
"""),

code("""
LIMIARES = [round(x, 2) for x in np.arange(0.0, 0.81, 0.05)]

tabela = F.varredura(df, LIMIARES)
tabela.to_csv(SAIDA / "varredura_limiares.csv", index=False)
colunas_frac = [c for c in tabela.columns if c.startswith("frac")]
tabela.assign(**{c: (tabela[c] * 100).round(1) for c in colunas_frac})
"""),

code("""
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))

for nivel, cor in CORES.items():
    ax1.plot(tabela["limiar"], tabela[nivel], color=cor, linewidth=2,
             marker="o", markersize=4, label=nivel)
    # rótulo direto no fim da série (a cor sozinha não carrega a identidade)
    ax1.annotate(nivel, (tabela["limiar"].iloc[0], tabela[nivel].iloc[0]),
                 xytext=(4, 4), textcoords="offset points", fontsize=9, color=cor)
ax1.set_xlabel("limiar de similaridade")
ax1.set_ylabel("questões mantidas")
ax1.set_title("Questões mantidas por dificuldade")
ax1.legend(frameon=False, fontsize=9)

for nivel, cor in CORES.items():
    ax2.plot(tabela["limiar"], tabela[f"frac_{nivel}"] * 100, color=cor,
             linewidth=2, marker="o", markersize=4, label=nivel)
ax2.set_xlabel("limiar de similaridade")
ax2.set_ylabel("% das mantidas")
ax2.set_title("Composição do que sobra")
ax2.legend(frameon=False, fontsize=9)

for ax in (ax1, ax2):
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.grid(axis="y", color="#e5e5e2", linewidth=0.8)
    ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig(SAIDA / "varredura_limiares.png", dpi=150)
plt.show()
"""),

md("""
## 5. O piso do docx

Os números entre parênteses no docx (200, 600, 400, …) são **mínimos por
tópico**. O limiar só é utilizável se, depois do corte, todo tópico continuar
acima do seu piso.
"""),

code("""
limiar_max = F.limiar_para_piso(df, referencias, LIMIARES)
print("maior limiar da grade que mantém todo tópico acima do piso:", limiar_max)

F.piso_por_topico(df, referencias, limiar_max if limiar_max is not None else 0.0)
"""),

code("""
# o mesmo corte por subtópico, para ver quem seca primeiro
detalhe = F.varredura_por_subtopico(df, LIMIARES)
detalhe.to_csv(SAIDA / "varredura_por_subtopico.csv", index=False)

alvo = limiar_max if limiar_max is not None else 0.0
(detalhe[detalhe["limiar"] == alvo]
 .sort_values("questoes")
 .loc[:, ["topico", "subtopico", "questoes", "total_subtopico",
          "facil", "media", "dificil"]]
 .head(15))
"""),

md("""
## 6. Corte escolhido: limiar como teto de poda, piso do docx como trava

A regra combinada: **0,55 é o corte mais rigoroso que se admite** — nenhum
tópico é podado além dele. Mas o piso do docx tem prioridade: quando um tópico
não tem questões parecidas o bastante para chegar ao seu mínimo, ele para de ser
podado antes, ficando com as N mais parecidas. Na prática isso é um limiar
efetivo mais baixo, só naquele tópico.

`filtrar_com_piso` faz as duas coisas e devolve o relatório com o limiar efetivo
de cada tópico: onde a coluna `criterio` disser `piso`, foi o mínimo do docx que
mandou; onde disser `limiar`, o corte de 0,55 valeu inteiro.
"""),

code("""
LIMIAR = 0.55

mantidas, relatorio = F.filtrar_com_piso(df, referencias, LIMIAR)
relatorio.to_csv(SAIDA / f"piso_{LIMIAR:.2f}.csv", index=False)
print(f"{len(mantidas)} questões mantidas de {len(df)} "
      f"({len(mantidas)/len(df):.1%})")
relatorio
"""),

code("""
destino = SAIDA / f"questoes_filtradas_{LIMIAR:.2f}_com_piso.jsonl"
n = F.exportar_filtrado(df, questoes, LIMIAR, destino, ids=set(mantidas["id"]))
print(f"{n} questões -> {destino}")
print(mantidas["dificuldade"].value_counts().to_string())
"""),

code("""
# como o piso se distribui entre os subtópicos dos tópicos que travaram
travados = relatorio.loc[relatorio["criterio"] == "piso", "topico"]
(mantidas[mantidas["topico"].isin(travados)]
 .groupby(["topico", "subtopico"])
 .agg(mantidas=("id", "size"), sim_minima=("similaridade", "min"))
 .round(3))
"""),

md("""
## 7. Método adotado: piso de relevância + cota por cluster

Ordenar por similaridade e cortar concentra a seleção em volta do centroide da
referência: medido com o codebook da fase 3 (k=24), o corte por limiar leva a
entropia de 0,953 para 0,793 e cobre 17,6 dos 24 clusters, enquanto uma amostra
ALEATÓRIA do mesmo tamanho mantém 0,920 — ou seja, a perda vem do critério, não
do tamanho.

Cota por cluster sozinha não resolve, porque pegaria as mais parecidas de cada
cluster inclusive de clusters inteiramente fora do assunto — justamente o que o
texto revisado do especialista veio excluir. Daí os dois estágios:

1. **piso de relevância (0,45) como filtro duro** — nada abaixo entra, nem para
   preencher cota; cluster todo abaixo do piso desaparece, e esse é o efeito
   pretendido;
2. **cota por cluster entre os sobreviventes**, até o alvo de cada subtópico (o
   que o corte em 0,55 com piso do docx daria, para manter o tamanho comparável).

Resultado: entropia 0,925 e 22,4 clusters cobertos, ao custo de 0,016 de
similaridade média.
"""),

code("""
PISO = 0.45

E = F.embeddings_das_questoes(questoes, emb)
emb.salvar_cache()
ordem = {q["id"]: i for i, q in enumerate(questoes)}
E = E[[ordem[i] for i in df["id"]]]      # mesma ordem das linhas de df

alvos = F.alvos_do_corte(df, referencias, LIMIAR)
sel, relatorio_cota, mortos = F.filtrar_por_cota_cluster(df, E, alvos, piso=PISO)
relatorio_cota.to_csv(SAIDA / "cota_cluster_relatorio.csv", index=False)
mortos.to_csv(SAIDA / "cota_cluster_clusters_eliminados.csv", index=False)

print(f"{len(sel)} questões · {len(mortos)} clusters eliminados pelo piso {PISO}")
print(sel["dificuldade"].value_counts().to_string())
relatorio_cota.head(10)
"""),

code("""
# por tópico, contra o mínimo do docx
minimos = {t: r["minimo_questoes"] for (t, _), r in referencias.items()
           if r.get("minimo_questoes")}
por_topico = (sel.groupby("topico")
              .agg(questoes=("id", "size"), sim_media=("similaridade", "mean"),
                   **{n: ("dificuldade", lambda s, n=n: (s == n).sum())
                      for n in ["facil", "media", "dificil"]}))
por_topico["minimo_docx"] = por_topico.index.map(minimos)
por_topico["atende"] = por_topico["questoes"] >= por_topico["minimo_docx"]
por_topico.round(3)
"""),

code("""
# o que o piso eliminou: clusters inteiros fora do assunto, com exemplo
por_id = {q["id"]: q for q in questoes}
for linha in mortos.nlargest(6, "questoes").itertuples():
    q = por_id[linha.exemplo_id]
    print(f"· {linha.subtopico} | cluster {linha.cluster} | "
          f"{linha.questoes} questões | sim média {linha.sim_media}")
    print(f"  faceta: {q.get('faceta_titulo')}")
    print(f"  ex.: {q['stem'][:180]}\n")
"""),

code("""
destino = SAIDA / f"questoes_filtradas_cota_cluster_piso{PISO:.2f}.jsonl"
n = F.exportar_filtrado(df, questoes, PISO, destino, ids=set(sel["id"]))
print(f"{n} questões -> {destino}")
"""),

md("""
### Alternativa: corte por quantil dentro de cada subtópico

Se a tabela da seção 3 mostrar medianas muito diferentes entre subtópicos, um
limiar absoluto é injusto: ele corta quase tudo de um subtópico e quase nada de
outro. Manter a fração mais parecida **dentro de cada subtópico** preserva a
cobertura temática.
"""),

code("""
FRACAO_MANTIDA = 0.70   # mantém as 70% mais parecidas de cada subtópico

corte = (df.groupby("subtopico")["similaridade"]
           .transform(lambda s: s.quantile(1 - FRACAO_MANTIDA)))
por_quantil = df[df["similaridade"] >= corte]

print(f"{len(por_quantil)} questões mantidas ({len(por_quantil)/len(df):.1%})")
print(por_quantil["dificuldade"].value_counts().to_string())
por_quantil.groupby("topico").size().rename("questoes").to_frame()
"""),

md("""
## Checklist antes de fechar a fase

* [ ] `referencias_especialista.json` foi gerado a partir do docx mais recente
* [ ] nenhum subtópico ficou sem referência (avisos da seção 1 vazios, fora os dois copiar/colar conhecidos)
* [ ] o limiar escolhido deixa todo tópico acima do piso do docx
* [ ] a composição fácil/média/difícil do corte foi conferida
* [ ] o `.jsonl` filtrado foi commitado junto com `varredura_limiares.csv`
"""),
]

notebook = {
    "cells": celulas,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python",
                       "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    },
    "nbformat": 4, "nbformat_minor": 5,
}
Path("filtragem_fase5.ipynb").write_text(
    json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
print("filtragem_fase5.ipynb:", len(celulas), "células")
