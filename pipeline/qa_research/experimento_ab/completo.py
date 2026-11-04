"""Geração v23 nos 40 documentos e dataset final v2, avaliado uma única vez com resposta de até 20 palavras.

1. v23-completo: o gerador v23 (o mesmo do B_v23) nos 37 documentos fora do experimento A/B, com o inventário
   (relações e encadeamentos) da geração final de outubro e os documentos dela (dez_areas_final_v2). Os 3 documentos
   do experimento já têm o B_v23, gerado sobre a versão refinada deles. Saída: relatorios/geracao_v23_completo.
2. final-v2 (relatorios/petroquest_final_v2):
   a. montar: v23 (B_v23) > v23c (v23 completo) > v22 (B_v22) > antigo filtrado > conceitos (geração de nomeação
      de termo técnico nos 40 documentos, relatorios/geracao_conceitos) > variada (conceito, mecanismo e consequência
      com exemplos de forma que mudam a cada visita, relatorios/geracao_variada), exclusões da revisão manual e
      deduplicação entre fontes (a mesma do dataset final v1) -> candidatos.jsonl;
   b. sustentar: auditoria de sustentação por afirmação de cada candidato (reaproveita a do v1 quando a questão é a
      mesma); só as totalmente sustentadas entram em dataset.jsonl;
   c. avaliar: todos os modelos avaliados (GPT-4.1 Nano/Mini/4.1 e GPT-5 nano/mini/5, com o GPT-5.4 só como
      referência), com e sem contexto, resposta de até 20 palavras (respondente_curta), juiz GPT-5.4;
   d. relatorio: QUALIDADE.md com acurácia, F1, ROUGE-L e BLEU por modelo, estratos de dificuldade e as métricas
      do dataset.
Cada etapa é retomável: repetir o comando continua de onde parou.
"""
from __future__ import annotations

import csv
import shutil
from collections import Counter
from pathlib import Path

import numpy as np

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json
from pipeline.inventario.textutil import read_json as ler
from pipeline.qa_research import benchmark_gap as G
from pipeline.qa_research.geracao_tipos.rodadas import _nome_arq
from pipeline.qa_research.piloto_janela.core import DOCS

from . import comum as C
from . import final as F
from . import limite as LI
from .painel import ESTRATOS, NAO_INDEPENDENTES, estrato

SAIDA_GERACAO = C.QA / "relatorios" / "geracao_v23_completo"
SAIDA_CONCEITOS = C.QA / "relatorios" / "geracao_conceitos"
SAIDA_VARIADA = C.QA / "relatorios" / "geracao_variada"
SAIDA = C.QA / "relatorios" / "petroquest_final_v2"
LIMITE = 20
DOCS_SIMULTANEOS = 6
# Os modelos avaliados, todos com effort low quando o modelo aceita (o GPT-4.1 não tem effort).
MODELOS = dict(LI.MODELOS)


def itens_completos(origem: Path = C.GERACAO_FINAL) -> list[str]:
    return [i for i in ler(Path(origem) / "config.json")["itens"] if i not in C.ITENS]


def gerador(exp: Path, *, workers: int = 8, onda: int = 4, saturacao: dict | None = None,
            docs_simultaneos: int = DOCS_SIMULTANEOS, itens=None, saida: Path = SAIDA_GERACAO,
            origem: Path = C.GERACAO_FINAL, docs: Path = DOCS, **kw):
    from .v23 import GeracaoV23
    itens = list(itens or itens_completos(origem))
    faltam = [i for i in itens if not (Path(origem) / "topicos" / i / "combinacoes.json").exists()]
    if faltam:
        raise ValueError(f"Inventário da geração de outubro ausente para {faltam} ({C.relativo(Path(origem))})")
    cal = Path(exp) / "calibracao" / "calibracao.json"
    if not cal.exists():
        raise ValueError(f"Falta a calibração da deduplicação ({C.relativo(cal)})")
    return GeracaoV23(Path(saida), itens, docs=Path(docs), braco="v23_completo", reusar=[Path(origem)],
                      calibracao=cal, saturacao=saturacao, onda=onda, workers=workers,
                      docs_simultaneos=docs_simultaneos, **kw)


def gerador_conceitos(exp: Path, *, workers: int = 8, onda: int = 4, saturacao: dict | None = None,
                      docs_simultaneos: int = DOCS_SIMULTANEOS, itens=None, saida: Path = SAIDA_CONCEITOS,
                      origem: Path = C.GERACAO_FINAL, docs: Path = DOCS, **kw):
    """Questões de nomeação de termo técnico nos 40 documentos (sem inventário: não há compostas)."""
    from .conceito import GeracaoConceito
    cal = Path(exp) / "calibracao" / "calibracao.json"
    if not cal.exists():
        raise ValueError(f"Falta a calibração da deduplicação ({C.relativo(cal)})")
    itens = list(itens or ler(Path(origem) / "config.json")["itens"])
    return GeracaoConceito(Path(saida), itens, docs=Path(docs), braco="conceitos", calibracao=cal,
                           saturacao=saturacao, onda=onda, workers=workers, docs_simultaneos=docs_simultaneos, **kw)


def gerador_variada(exp: Path, *, workers: int = 8, onda: int = 4, docs_simultaneos: int = DOCS_SIMULTANEOS,
                    itens=None, saida: Path = SAIDA_VARIADA, origem: Path = C.GERACAO_FINAL, docs: Path = DOCS, **kw):
    """Conceito, mecanismo e consequência nos 40 documentos, com exemplos de forma externos (visitas 1 a 3) e do
    dataset de múltipla escolha convertido (visita 4)."""
    from .variada import GeracaoVariada
    cal = Path(exp) / "calibracao" / "calibracao.json"
    if not cal.exists():
        raise ValueError(f"Falta a calibração da deduplicação ({C.relativo(cal)})")
    itens = list(itens or ler(Path(origem) / "config.json")["itens"])
    return GeracaoVariada(Path(saida), itens, docs=Path(docs), braco="variada", calibracao=cal, onda=onda,
                          workers=workers, docs_simultaneos=docs_simultaneos, **kw)


def fontes_v2(exp: Path = C.EXPERIMENTO, geracao: Path = SAIDA_GERACAO, conceitos: Path = SAIDA_CONCEITOS,
              variada: Path = SAIDA_VARIADA) -> list[dict]:
    """Prioridade na deduplicação: v23 > v23 completo > v22 > antigo > conceitos > variada (as fontes novas entram
    no que falta)."""
    v23, v22, antigo = ({**f, "obrigatoria": True} for f in F.fontes(exp))
    v23c = {"nome": "v23c", "pasta": Path(geracao), "marcador": "geracao_concluida.json", "docs": DOCS,
            "obrigatoria": True}
    conc = {"nome": "conceitos", "pasta": Path(conceitos), "marcador": "geracao_concluida.json", "docs": DOCS,
            "obrigatoria": True}
    var = {"nome": "variada", "pasta": Path(variada), "marcador": "geracao_concluida.json", "docs": DOCS,
           "obrigatoria": True}
    return [v23, v23c, v22, antigo, conc, var]


def metricas_modelo(pares: list[dict]) -> dict:
    """Acurácia (juiz) e métricas lexicais contra o gabarito, por condição."""
    out = {}
    for cond, chave in (("sem", "closed_book"), ("com", "open_book")):
        ps = [(r[f"resposta_{chave}"], r[f"veredito_{chave}"], r["gabarito"]) for r in pares
              if r[f"veredito_{chave}"] in ("correta", "parcial", "incorreta") and r[f"resposta_{chave}"]]
        if not ps:
            continue
        fs = [LI.f1(a, g)[0] for a, _, g in ps]
        out[cond] = {"n": len(ps), "acuracia": 100 * np.mean([v == "correta" for _, v, _ in ps]),
                     "com_parcial": 100 * np.mean([{"correta": 1, "parcial": .5}.get(v, 0) for _, v, _ in ps]),
                     "f1": 100 * np.mean(fs), "rouge_l": 100 * np.mean([LI.rouge_l(a, g) for a, _, g in ps]),
                     "bleu": LI.bleu([a for a, _, _ in ps], [g for _, _, g in ps]),
                     "palavras": float(np.mean([len(a.split()) for a, _, _ in ps])),
                     "auc_f1_juiz": LI.auc([f for f, (_, v, _) in zip(fs, ps) if v == "correta"],
                                           [f for f, (_, v, _) in zip(fs, ps) if v == "incorreta"])}
    return out


class DatasetCompleto(F.DatasetFinal):
    ARQ = "candidatos.jsonl"

    def __init__(self, saida: Path = SAIDA, exp: Path = C.EXPERIMENTO, *, limite: int = LIMITE,
                 modelos: dict | None = None, v1: Path = F.SAIDA, fontes_: list | None = None, **kw):
        super().__init__(Path(saida), exp=exp, fontes_=fontes_ if fontes_ is not None else fontes_v2(exp), **kw)
        self.limite, self.modelos, self.v1 = int(limite), dict(modelos or MODELOS), Path(v1)

    # ---------------------------------------------------------------- 2a. montagem
    def montar(self) -> int:
        """A do v1. Nos 3 documentos do experimento, as fontes e a ordem são as mesmas do v1 (a v23 completa não os
        inclui), então as decisões de deduplicação já pagas são copiadas; os embeddings também."""
        for item in C.ITENS:
            origem, destino = self.v1 / "dedup" / item, self.saida / "dedup" / item
            if origem.exists() and not destino.exists():
                shutil.copytree(origem, destino)
        for arq in (self.v1 / ".local").glob("embeddings_*.sqlite3") if (self.v1 / ".local").exists() else []:
            alvo = self.saida / ".local" / arq.name
            if not alvo.exists():
                alvo.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(arq, alvo)
        return super().montar()

    def _aceita_mudanca(self, final: list) -> bool:
        """A avaliação é guardada por questão (uid): com uma fonte nova, as questões que já existiam continuam
        avaliadas e só as novas são pagas. Exige que nenhuma questão antiga tenha mudado de conteúdo."""
        antigo = self.saida / self.ARQ
        if not antigo.exists():
            return False
        novo = {q["uid"]: q for q in final}
        mudaram = [q["uid"] for q in C.linhas(antigo) if q["uid"] in novo and novo[q["uid"]] != q]
        if mudaram:
            raise ValueError(f"{len(mudaram)} questões mudaram de conteúdo com o mesmo uid (ex.: {mudaram[0]}); apague "
                             f"{C.relativo(self.saida)} para reavaliar do zero")
        return True

    # ---------------------------------------------------------------- 2b. sustentação
    def sustentar(self, workers: int = 8, clientes=None) -> int:
        cands = C.linhas(self.saida / self.ARQ)
        pasta = self.saida / "sustentacao"
        destino = pasta / "faithfulness"
        destino.mkdir(parents=True, exist_ok=True)
        reusadas = 0
        for q in cands:      # mesma questão e mesmo contexto do dataset v1: a auditoria já paga é reaproveitada
            nome = _nome_arq(q["uid"]) + ".json"
            antiga = self.v1 / "faithfulness" / nome
            if not (destino / nome).exists() and antiga.exists():
                shutil.copy2(antiga, destino / nome)
                reusadas += 1
        e = G.AvaliacaoGap(pasta, respondentes=self.modelos, juiz=G.Q.JUIZ, workers=workers, clientes=clientes,
                           progress=self.progress)
        try:
            ok = G.faithfulness(e, cands)
        finally:
            for c in e.clientes.values():
                if hasattr(c, "close"):
                    c.close()
        if not ok:
            return 2
        st = {r["uid"]: r.get("status") for r in C.linhas(pasta / "faithfulness.jsonl")}
        final = [q for q in cands if st.get(q["uid"]) == "totalmente_sustentado"]
        C.gravar_jsonl(self.saida / "dataset.jsonl", final)
        res = {"candidatos": len(cands), "sustentadas": len(final), "reaproveitadas_do_v1": reusadas,
               "por_status": dict(Counter(st.get(q["uid"]) for q in cands)),
               "por_fonte": {f: {"candidatos": sum(q["fonte"] == f for q in cands),
                                 "sustentadas": sum(q["fonte"] == f for q in final)}
                             for f in dict.fromkeys(q["fonte"] for q in cands)}}
        atomic_json(self.saida / "sustentacao.json", res)
        self.progress(f"[final-v2] sustentação: {len(final)}/{len(cands)} totalmente sustentadas | "
                      + " | ".join(f"{k}: {v['sustentadas']}/{v['candidatos']}" for k, v in res["por_fonte"].items()),
                      flush=True)
        return 0

    # ---------------------------------------------------------------- 2c. avaliação
    def avaliar(self, workers=8, judge_workers=2, clientes=None, **_) -> int:
        original = C.linhas(self.saida / "dataset.jsonl")
        rows = [{**q, "uid_original": q["uid"], "uid": arm + ":" + q["uid"], "condicao": arm,
                 "contexto_tecnico": q["contexto_tecnico"] if arm == "open_book" else None}
                for q in original for arm in G.ARMS]
        cfg = dict(schema="petroquest-final-v2-avaliacao", n=len(original), dados_sha256=C.sha(original),
                   questoes_sha256=C.sha(rows), modelos=self.modelos, referencia_nao_independente=list(NAO_INDEPENDENTES),
                   juiz=G.Q.JUIZ, limite_palavras=self.limite, lote_juiz=8,
                   contexto="blocos que geraram a questão, no documento de origem",
                   prompts={"respondente": C.sha(LI.prompt_curta(self.limite)), "juiz": C.sha(G.prompt("juiz"))})
        with output_lock(self.saida / "avaliacao"):
            old = ler(self.saida / "config.json")
            dados = ("n", "dados_sha256", "questoes_sha256")
            if old is not None and {k: v for k, v in old.items() if k not in dados} != \
                    {k: v for k, v in cfg.items() if k not in dados}:
                raise ValueError("O protocolo (modelos, limite, prompts ou juiz) mudou em relação à avaliação "
                                 f"existente; apague {C.relativo(self.saida / 'avaliacao')} e config.json para reavaliar")
            if old is not None and old != cfg:     # dataset ampliado: as respostas e vereditos por questão continuam
                self.progress(f"[final-v2] dataset mudou ({old['n']} -> {cfg['n']} questões): só as novas serão "
                              "respondidas e julgadas", flush=True)
            local = self.saida / "avaliacao" / ".local"
            lim = self.v1 / f"limite_{self.limite}" / "avaliacao" / ".local"
            if not local.exists() and clientes is None and lim.exists():
                self._mesclar_cache(local, [lim])     # mesmas respostas curtas sem contexto do experimento do limite
            atomic_json(self.saida / "config.json", cfg)
            G.Q.C.GeracaoSemConteudo.jsonl(self.saida / "questoes.jsonl", rows)
            G.Q.C.GeracaoSemConteudo.jsonl(self.saida / "contextos.jsonl", original)
            d = self.saida / "avaliacao"
            for m in self.modelos:
                for sub in ("respostas", "juiz"):
                    (d / sub / m).mkdir(parents=True, exist_ok=True)
            (d / "falhas").mkdir(exist_ok=True)
            marcador = self.saida / "rodada_concluida.json"
            marcador.unlink(missing_ok=True)
            LI.AvaliacaoCurta.limite = self.limite
            e = LI.AvaliacaoCurta(self.saida, respondentes=self.modelos, juiz=G.Q.JUIZ, grupos=[tuple(self.modelos)],
                                  workers=workers, judge_workers=judge_workers, lote_juiz=8, clientes=clientes,
                                  progress=self.progress)
            try:
                e.run()
                G.exportar_gap(self.saida, self.modelos)
                ok = all(r["uid"] in e.vereditos[m] for m in self.modelos for r in rows)
            finally:
                for c in e.clientes.values():
                    if hasattr(c, "close"):
                        c.close()
            if ok:
                atomic_json(marcador, {"status": "concluida", "questoes": len(original)})
            return 0 if ok else 2

    # ---------------------------------------------------------------- 2d. relatório
    def relatorio(self) -> dict:
        qs = {q["uid"]: q for q in C.linhas(self.saida / "dataset.jsonl")}
        n = len(qs)
        res: dict = {"n": n, "topicos": len({q["item"] for q in qs.values()}), "limite_palavras": self.limite,
                     "por_fonte": dict(Counter(q["fonte"] for q in qs.values())),
                     "por_tipo": dict(Counter(q["tipo"] for q in qs.values())),
                     "por_topico": dict(sorted(Counter(q["item"] for q in qs.values()).items())),
                     "sustentacao": ler(self.saida / "sustentacao.json"),
                     "montagem": {k: v for k, v in (ler(self.saida / "montagem.json") or {}).items()
                                  if k in ("por_fonte", "dataset")}}
        pares: dict = {}
        if (self.saida / "pares.csv").exists():
            with (self.saida / "pares.csv").open(encoding="utf-8-sig") as f:
                for r in csv.DictReader(C.sem_nul(f)):
                    if r["uid"] in qs:
                        pares.setdefault(r["modelo"], []).append({**r, "gabarito": qs[r["uid"]]["resposta"]})
        res["modelos"] = {m: metricas_modelo(pares[m]) for m in self.modelos if m in pares}
        # estratos de dificuldade (sem contexto); o GPT-5.4 gerou as questões e fica fora dos estratos
        vs: dict = {}
        for m, ps in pares.items():
            for r in ps:
                vs.setdefault(r["uid"], {})[m] = r["veredito_closed_book"]
        linhas = []
        for u, v in sorted(vs.items()):
            if set(v) >= set(self.modelos) and all(x is not None for x in v.values()):
                linhas.append({"uid": u, "item": qs[u]["item"], "tipo": qs[u]["tipo"], "fonte": qs[u]["fonte"],
                               **{f"v_{m}": v[m] for m in self.modelos}, "estrato": estrato(v)})
        if linhas:
            with (self.saida / "dificuldade.csv").open("w", encoding="utf-8-sig", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(linhas[0]))
                w.writeheader()
                w.writerows(linhas)
        est = Counter(r["estrato"] for r in linhas)
        res["estratos_pct"] = {e: round(100 * est.get(e, 0) / len(linhas), 1) for e in ESTRATOS} if linhas else None
        res["dificil_por_tipo"] = {t: round(100 * sum(r["estrato"] in ("dificil", "muito_dificil") for r in rs)
                                            / len(rs), 1)
                                   for t in sorted({r["tipo"] for r in linhas})
                                   for rs in [[r for r in linhas if r["tipo"] == t]]}
        res.update(self.diversidade(list(qs.values())))
        atomic_json(self.saida / "qualidade.json", res)
        (self.saida / "QUALIDADE.md").write_text(_markdown(res), encoding="utf-8")
        return res


NOMES = {"gpt-4-1-nano": "GPT-4.1 Nano", "gpt-4-1-mini": "GPT-4.1 Mini", "gpt-4-1": "GPT-4.1",
         "gpt-5-nano": "GPT-5 nano", "gpt-5-mini": "GPT-5 mini", "gpt-5": "GPT-5", "gpt-5-4": "GPT-5.4 (referência)"}


def _markdown(r: dict) -> str:
    f = lambda v, c=1: "-" if v is None else f"{v:.{c}f}"  # noqa: E731
    s = r.get("sustentacao") or {}
    out = ["# PetroQuest: qualidade do dataset final v2", "",
           f"{r['n']} questões em {r['topicos']} tópicos, todas com gabarito totalmente sustentado pelo contexto "
           f"({s.get('sustentadas', '-')} de {s.get('candidatos', '-')} candidatas). Por fonte: {r['por_fonte']}. "
           f"Por tipo: {r['por_tipo']}.", "",
           f"## Modelos (resposta de até {r['limite_palavras']} palavras)", "",
           "| Modelo | Sem contexto ↓ | Com parcial ↓ | Com contexto ↑ | Gap | F1 | ROUGE-L | BLEU |",
           "|---|---|---|---|---|---|---|---|"]
    for m, x in r["modelos"].items():
        sem, com = x.get("sem", {}), x.get("com", {})
        gap = None if not sem or not com else com["acuracia"] - sem["acuracia"]
        out.append(f"| {NOMES.get(m, m)} | {f(sem.get('acuracia'))}% | {f(sem.get('com_parcial'))}% | "
                   f"{f(com.get('acuracia'))}% | {f(gap)} | {f(sem.get('f1'))} | {f(sem.get('rouge_l'))} | "
                   f"{f(sem.get('bleu'))} |")
    out += ["", "F1, ROUGE-L e BLEU (0 a 100) comparam a resposta sem contexto com o gabarito. O veredito do juiz é a "
            "métrica principal; as lexicais são complementares. O GPT-5.4 gerou, auditou e julga as questões: fica "
            "fora dos estratos e só serve de referência.", ""]
    e, lx = r.get("estratos_pct") or {}, r["lexical"]
    tipos = r["por_tipo"]
    dp = 100 * (tipos.get("decisao", 0) + tipos.get("procedimento", 0)) / r["n"] if r["n"] else None
    linhas = [
        ("Dificuldade", "Difícil para o GPT-5 (inclui muito difícil)", "↑", "> 15%",
         "-" if not e else f"{e['dificil'] + e['muito_dificil']:.1f}%"),
        ("Dificuldade", "Nenhum modelo independente acerta", "↑ (com questões boas)", "5–15%",
         "-" if not e else f"{e['muito_dificil']:.1f}%"),
        ("Dificuldade", "Todos os modelos independentes acertam (fácil)", "↓", "< 40%",
         "-" if not e else f"{e['facil']:.1f}%"),
        ("Não trivialidade", "Max ROUGE-L pergunta ↔ frase do contexto", "↓", "0,15–0,40", f(lx["max_rougeL"], 3)),
        ("Não trivialidade", "Bigramas novos no gabarito", "↑", "> 30%", f"{f(lx['novel_2gram'])}%"),
        ("Diversidade", "Self-BLEU-4 entre perguntas do mesmo tópico", "↓", "< 0,25", f(lx["self_bleu4_por_topico"], 3)),
        ("Diversidade", "Vizinho mais próximo no tópico (cosseno centrado)", "↓", "< 0,50",
         f(r.get("vizinho_cosseno_centrado"), 3)),
        ("Forma", "Palavras no gabarito", "↓", "3–15", f(lx["palavras_resposta"])),
        ("Cobertura", "Decisão + procedimento", "↑", "> 30%", f"{f(dp)}%"),
    ]
    out += ["## Dataset", "", "| Dimensão | Métrica | Melhor | Faixa de referência | Valor |", "|---|---|---|---|---|"]
    out += [f"| {a} | {b} | {c} | {d} | {v} |" for a, b, c, d, v in linhas]
    out += ["", f"Difícil para o GPT-5 por tipo: {r.get('dificil_por_tipo')}.", "",
            f"Questões por tópico: {r['por_topico']}.", "",
            "As faixas são referências de trabalho do projeto, não padrões da literatura."]
    return "\n".join(out) + "\n"


def executar(exp: Path = C.EXPERIMENTO, workers=8, judge_workers=2, limite: int = LIMITE, progress=print) -> int:
    d = DatasetCompleto(exp=exp, limite=limite, progress=progress)
    for etapa in (d.montar, lambda: d.sustentar(workers), lambda: d.avaliar(workers, judge_workers)):
        if etapa():
            return 2
    d.relatorio()
    return 0
