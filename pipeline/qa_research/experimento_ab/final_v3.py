"""Geração final v3 do PetroQuest sobre os 40 contextos finais (relatorios/geracao_final_v3).

Usa o melhor mecanismo medido na ablação v3: a retroalimentação sem memória (configuração retro_sem_memoria,
40% de válidas contra 29% de + Datasets externos), que reúne
  - regras e documentos: janela de 3 blocos em torno do bloco foco;
  - datasets externos como exemplos de forma (Pirá 2, MMMLU PT-BR 2, ARC-Challenge 1, QASC 1 por chamada) e,
    alternadamente, 2 questões do dataset de múltipla escolha convertidas para QA (de outros documentos): metade
    das chamadas leva as convertidas e metade não, em xadrez por foco e visita;
  - retroalimentação v2: 4 boas e 4 ruins fixas do especialista; 10 boas totalmente válidas e 8 ruins (com cotas
    por defeito e o defeito por extenso) sorteadas do que já foi julgado em outros documentos; proporção dos
    defeitos; teste de cada defeito antes de entregar. Nada do mesmo documento entra no prompt.

Diferenças em relação à ablação (que media a escada com 8 focos por documento):
  - todos os blocos de cada documento são foco e cada foco é visitado até saturar: depois de cada visita, as
    válidas são deduplicadas e o foco só volta na visita seguinte se a última trouxe ao menos uma válida nova
    (não equivalente a nenhuma anterior do documento); com PACIENCIA visitas seguidas sem nada novo, ele fecha.
    Teto de MAX_VISITAS visitas. Cada visita roda em 2 ondas (focos pares e ímpares);
  - a deduplicação calibrada roda só entre as questões válidas, para o banco (a da ablação era medida sobre todas);
  - etapa "banco": uma questão por grupo de equivalentes, só válidas.

Válida = aprovada pelo auditor v23 + gabarito de até 20 palavras + gabarito totalmente sustentado pelos blocos.

python -m pipeline.qa_research.experimento_ab final-v3 [--visitas 8] [--paciencia 1] [--etapas ...]
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from pipeline.inventario.textutil import atomic_json

from . import comum as C
from .ablacao_v3 import (AblacaoV3, CONFIGS, MISTURA_EXTERNOS, N_CONVERTIDAS, TETO_RESPOSTA, _rng)
from .variada import bloco_forma

SAIDA = C.QA / "relatorios" / "geracao_final_v3"
DOCS_FINAIS = C.QA / "relatorios" / "contextos_finais_v1"
CONFIG = "retro_sem_memoria"
MAX_VISITAS = 8
PACIENCIA = 1
TODOS_OS_BLOCOS = 10 ** 6
ETAPAS = ("geracao", "sustentacao", "dedup", "banco")
# O que fica só no servidor (retomada): respostas brutas, caches e um arquivo por chamada. Vai ao GitHub o banco,
# o resumo e as questões julgadas, sem o texto dos blocos (recuperável de contextos_finais_v1).
GITIGNORE = """.local/
chamadas/
falhas/
sustentacao/
*/geracao/
*/auditoria/
*/dedup_validas/
"""


class GeracaoFinalV3(AblacaoV3):
    def __init__(self, saida: Path = SAIDA, *, docs: Path = DOCS_FINAIS, visitas: int = MAX_VISITAS,
                 paciencia: int = PACIENCIA, **kw):
        if not any((p / "documento.json").exists() for p in Path(docs).iterdir() if p.is_dir()) if Path(docs).is_dir() else True:
            raise ValueError(f"Contextos finais ausentes em {C.relativo(Path(docs))}; rode antes "
                             "python -m pipeline.qa_research.refino.finalizar")
        self.paciencia = max(1, int(paciencia))
        super().__init__(saida, docs=docs, configs=[CONFIG], focos_por_topico=TODOS_OS_BLOCOS, visitas=visitas, **kw)
        (self.saida / ".gitignore").write_text(GITIGNORE, encoding="utf-8")

    def _config(self) -> None:
        """O teto de visitas pode mudar entre execuções (ex.: versão com 3 visitas fixas interrompida): as unidades da
        visita 1 são as mesmas, então a pasta é reaproveitada e só o teto registrado é atualizado."""
        arq = self.saida / "config.json"
        if arq.exists():
            d = json.loads(arq.read_text(encoding="utf-8"))
            if d.get("visitas") != self.visitas:
                d["visitas"] = self.visitas
                atomic_json(arq, d)
        super()._config()

    # -------------------------------------------------------------- saturação por foco
    @staticmethod
    def _unidade(item: str, foco: int, visita: int) -> dict:
        return {"item": item, "foco": foco, "visita": visita, "onda": (visita - 1) * 2 + foco % 2,
                "id": f"{item}:{foco:03d}:v{visita}"}

    def _estado(self, u: dict) -> tuple[bool, int]:
        """(visita concluída para a decisão, válidas novas): tudo gerado, auditado, sustentado e deduplicado."""
        if not self._arq_ger(CONFIG, u).exists():
            return False, 0
        novas = 0
        for q in self._questoes_unidade(CONFIG, u):
            a = q.get("auditoria")
            if a is None:
                return False, 0
            if not (a.get("aprovada") and len(str(q["resposta"]).split()) <= TETO_RESPOSTA):
                continue
            s = self._arq_sust(q["uid"])
            if not s.exists():
                return False, 0
            if json.loads(s.read_text(encoding="utf-8")).get("status") != "totalmente_sustentado":
                continue
            d = self.saida / CONFIG / "dedup_validas" / u["item"] / (q["uid"].replace(":", "_") + ".json")
            if not d.exists():
                return False, 0
            novas += json.loads(d.read_text(encoding="utf-8"))["decisao"] in ("nova", "substitui")
        return True, novas

    def _unidades(self) -> list[dict]:
        """Visita 1 de todos os blocos; a visita v+1 só para os focos ainda abertos depois da visita v concluída."""
        out, self.fechados = [], {}
        for i in self.itens:
            abertos = {f: 0 for f in range(len(self.docs[i]))}       # foco -> visitas seguidas sem nada novo
            for v in range(1, self.visitas + 1):
                if not abertos:
                    break
                us = [self._unidade(i, f, v) for f in sorted(abertos)]
                out += us
                estados = [self._estado(u) for u in us]
                if not all(ok for ok, _ in estados):
                    break                                            # visita em andamento: decide depois
                for u, (_, novas) in zip(us, estados):
                    abertos[u["foco"]] = 0 if novas else abertos[u["foco"]] + 1
                    if abertos[u["foco"]] >= self.paciencia:
                        self.fechados[(i, u["foco"])] = v
                        del abertos[u["foco"]]
        return out

    def gerar(self) -> int:
        """Visita a visita (2 ondas cada); depois de cada visita, deduplica as válidas e reabre só os focos com novidade."""
        from .ablacao_v3 import ONDAS_POR_VISITA
        falhas = 0
        for v in range(1, self.visitas + 1):
            if not any(u["visita"] == v for u in self.unidades):
                break
            for w in range((v - 1) * ONDAS_POR_VISITA, v * ONDAS_POR_VISITA):
                us = [u for u in self.unidades if u["onda"] == w]
                julg = self._julgadas(CONFIG, w)
                falhas += self._paralelo([u for u in us if not self._arq_ger(CONFIG, u).exists()],
                                         lambda u: self._gerar(CONFIG, u, julg), f"onda {w + 1}: geração")
                tarefas = [(CONFIG, u, q) for u in us for q in self._questoes_unidade(CONFIG, u) if q["auditoria"] is None]
                falhas += self._paralelo(tarefas, lambda x: self._auditar(*x), f"onda {w + 1}: auditoria")
                if not falhas:
                    qs = [q for q in self.finais(CONFIG, us) if q["aprovada_auditor"] and q["resposta_curta"]
                          and not self._arq_sust(q["uid"]).exists()]
                    falhas += self._paralelo(qs, self._sustentar_um, f"onda {w + 1}: sustentação")
                if falhas:
                    return falhas
            falhas += self.deduplicar()
            if falhas:
                return falhas
            antes = len(self.unidades)
            self.unidades = self._unidades()
            abertos = sum(u["visita"] == v + 1 for u in self.unidades)
            self.progress(f"[final v3] visita {v} concluída; {abertos} focos seguem para a visita {v + 1} "
                          f"({len(self.unidades) - antes} chamadas novas)", flush=True)
        return falhas

    # -------------------------------------------------------------- auditoria guarda só a referência dos blocos
    def _auditar(self, c: str, u: dict, q: dict) -> bool:
        ok = super()._auditar(c, u, q)
        arq = self._arq_aud(c, q["uid"])
        if ok and arq.exists():
            d = json.loads(arq.read_text(encoding="utf-8"))
            if any("texto" in b for b in d.get("contexto", [])):
                d["contexto"] = [{k: b[k] for k in ("id", "item", "titulo", "indice_documento")} for b in d["contexto"]]
                atomic_json(arq, d)
        return ok

    def _questoes_unidade(self, c: str, u: dict) -> list[dict]:
        out = super()._questoes_unidade(c, u)
        for q in out:
            for b in (q.get("auditoria") or {}).get("contexto", []):
                if "texto" not in b:
                    b["texto"] = self.todos[b["item"]][b["indice_documento"]]["texto"]
        return out

    @staticmethod
    def com_convertidas(u: dict) -> bool:
        """Xadrez por foco e visita: vizinhos e visitas seguidas alternam com e sem as convertidas."""
        return (u["foco"] + u["visita"]) % 2 == 1

    def _forma(self, u: dict) -> str:
        rng = _rng("forma", u["id"])
        ex = []
        for fonte, n in MISTURA_EXTERNOS.items():
            pool = self.pools.get(fonte) or [r for v in self.pools.values() for r in v]
            ex += rng.sample(pool, min(n, len(pool)))
        if self.com_convertidas(u):
            outras = [q for q in self.convertidas if q.get("item") != u["item"]] or self.convertidas
            ex += rng.sample(outras, min(N_CONVERTIDAS, len(outras)))
        rng.shuffle(ex)
        return bloco_forma(ex)

    # -------------------------------------------------------------- deduplicação só entre as válidas
    def _dedup(self, c: str):
        from .dedup import DedupIncremental
        from .geracao import _Preguicoso
        return DedupIncremental(self.saida / c / "dedup_validas", self.embedder, self.media, self.cal["limiar_auto"],
                                self.cal["limiar_juiz"], _Preguicoso(lambda: self.cliente("dedup_juiz")),
                                progress=self.progress)

    def deduplicar(self) -> int:
        falhas = 0
        for c in self.configs:
            dd = self._dedup(c)
            por_item = defaultdict(list)
            for q in sorted(self.finais(c), key=lambda q: (q["onda"], q["foco"], q["k"])):
                if q["valida"]:
                    por_item[q["item"]].append({**q, "conhecimento": q.get("conhecimento") or q["pergunta"],
                                                "explicacao": q.get("explicacao") or ""})
            for item, lst in sorted(por_item.items()):
                falhas += dd.processar(item, lst, falha=self._falha, ok=self._ok)
        return falhas

    # -------------------------------------------------------------- banco
    def banco(self) -> dict:
        qs = self.finais(CONFIG)
        red = self.redundantes(CONFIG) if (self.saida / CONFIG / "dedup_validas").exists() else {}
        validas = [q for q in qs if q["valida"]]
        unicas = [q for q in validas if q["uid"] not in red]
        unicas.sort(key=lambda q: (q["item"], q["foco"], q["visita"], q["k"]))
        linhas = []
        for n, q in enumerate(unicas, 1):
            linhas.append({"id": f"PQ3-{n:05d}", "uid": q["uid"], "item": q["item"], "tema": self.temas[q["item"]]["tema"],
                           "area": self.temas[q["item"]]["area"], "tipo": q["tipo"], "pergunta": q["pergunta"],
                           "resposta": q["resposta"], "explicacao": q["explicacao"], "conhecimento": q["conhecimento"],
                           "resposta_padrao": q["resposta_padrao"], "foco": q["foco"], "visita": q["visita"],
                           "com_convertidas": self.com_convertidas({"foco": q["foco"], "visita": q["visita"]}),
                           "blocos_contexto": [{k: b[k] for k in ("id", "item", "indice_documento")}
                                               for b in q["blocos_contexto"]]})
        C.gravar_jsonl(self.saida / "banco.jsonl", linhas)
        C.gravar_jsonl(self.saida / f"questoes_{CONFIG}.jsonl",
                       [{**{k: v for k, v in q.items() if k not in ("blocos_contexto", "fonte_texto")},
                         "blocos": [b["indice_documento"] for b in q["blocos_contexto"]]} for q in qs])
        chamadas = sum(1 for u in self.unidades if self._arq_ger(CONFIG, u).exists())
        motivos = Counter(f for q in qs for f in q["auditoria"].get("falhas", []))
        sust = Counter(q["sustentacao"] for q in qs if q["aprovada_auditor"] and q["resposta_curta"])
        por_item = {i: {"blocos": len(self.docs[i]), "geradas": sum(q["item"] == i for q in qs),
                        "validas": sum(q["item"] == i for q in validas), "unicas": sum(q["item"] == i for q in unicas)}
                    for i in self.itens}
        alt = {k: {"geradas": sum(self.com_convertidas(q) == k for q in qs),
                   "validas": sum(self.com_convertidas(q) == k for q in validas)} for k in (True, False)}
        res = {"documentos": len(self.itens), "blocos": sum(len(v) for v in self.docs.values()), "visitas": self.visitas,
               "chamadas": chamadas, "geradas": len(qs), "aprovadas_auditor": sum(q["aprovada_auditor"] for q in qs),
               "resposta_curta": sum(q["resposta_curta"] for q in qs), "validas": len(validas), "unicas": len(unicas),
               "taxa_validas": 100 * len(validas) / max(1, len(qs)),
               "por_visita": {v: {"geradas": sum(q["visita"] == v for q in qs),
                                  "validas": sum(q["visita"] == v for q in validas),
                                  "unicas": sum(q["visita"] == v for q in unicas)}
                              for v in range(1, max([u["visita"] for u in self.unidades] or [1]) + 1)},
               "focos_fechados_na_visita": dict(Counter(self.fechados.values()).most_common()),
               "convertidas": {"com" if k else "sem": v for k, v in alt.items()},
               "tipos_unicas": dict(Counter(q["tipo"] or "?" for q in unicas).most_common()),
               "motivos_auditor": dict(motivos.most_common()), "sustentacao": dict(sust.most_common()),
               "por_documento": por_item}
        atomic_json(self.saida / "banco_resumo.json", res)
        (self.saida / "BANCO.md").write_text(markdown(res), encoding="utf-8")
        return res

    def executar(self, etapas=ETAPAS, **_) -> int:
        etapas = tuple(etapas)
        falhas = 0
        if "geracao" in etapas:
            falhas += self.gerar()
        if "sustentacao" in etapas and not falhas:
            falhas += self.sustentar()
        if "dedup" in etapas and not falhas:
            falhas += self.deduplicar()
        if falhas:
            self.progress(f"[final v3] {falhas} unidades com falha (em {C.relativo(self.saida / 'falhas')}); repita o "
                          "mesmo comando", flush=True)
            return 2
        if "banco" in etapas:
            r = self.banco()
            self.progress(f"[final v3] {r['geradas']} geradas, {r['validas']} válidas, {r['unicas']} únicas "
                          f"({C.relativo(self.saida / 'BANCO.md')})", flush=True)
        return 0


def markdown(r: dict) -> str:
    pct = lambda a, b: f"{100 * a / b:.1f}%" if b else "-"  # noqa: E731
    linhas = ["# Geração final v3: banco de questões", "",
              f"Mecanismo: retroalimentação sem memória (melhor configuração da ablação v3), datasets externos e "
              f"convertidas do dataset de múltipla escolha em metade das chamadas. {r['documentos']} documentos, "
              f"{r['blocos']} blocos foco, visitados até saturar (teto de {r['visitas']} visitas), "
              f"{r['chamadas']} chamadas do gerador.", "",
              "Válida = aprovada pelo auditor v23, gabarito de até 20 palavras e totalmente sustentada pelos blocos. "
              "Única = uma por grupo de questões equivalentes (deduplicação calibrada entre as válidas).", "",
              "| Etapa | Questões | % das geradas |", "|---|---|---|",
              f"| Geradas | {r['geradas']} | 100% |",
              f"| Aprovadas pelo auditor | {r['aprovadas_auditor']} | {pct(r['aprovadas_auditor'], r['geradas'])} |",
              f"| Válidas | {r['validas']} | {pct(r['validas'], r['geradas'])} |",
              f"| Válidas únicas (banco) | {r['unicas']} | {pct(r['unicas'], r['geradas'])} |", "",
              "## Por visita", "", "| Visita | Geradas | Válidas | Únicas |", "|---|---|---|---|"]
    for v, x in r["por_visita"].items():
        linhas.append(f"| {v} | {x['geradas']} | {x['validas']} ({pct(x['validas'], x['geradas'])}) | {x['unicas']} |")
    c = r["convertidas"]
    linhas += ["", "## Com e sem as convertidas do dataset de múltipla escolha", "",
               f"- Com: {c['com']['validas']} válidas de {c['com']['geradas']} ({pct(c['com']['validas'], c['com']['geradas'])}).",
               f"- Sem: {c['sem']['validas']} válidas de {c['sem']['geradas']} ({pct(c['sem']['validas'], c['sem']['geradas'])}).",
               "", "## Tipos (únicas)", ""]
    linhas += [f"- {k}: {v}" for k, v in r["tipos_unicas"].items()]
    linhas += ["", "## Motivos de reprovação do auditor", ""]
    linhas += [f"- {k}: {v}" for k, v in r["motivos_auditor"].items()]
    linhas += ["", "## Por documento", "", "| Documento | Blocos | Geradas | Válidas | Únicas |", "|---|---|---|---|---|"]
    for i, x in r["por_documento"].items():
        linhas.append(f"| {i} | {x['blocos']} | {x['geradas']} | {x['validas']} | {x['unicas']} |")
    return "\n".join(linhas) + "\n"


def plano(visitas: int = MAX_VISITAS, docs: Path = DOCS_FINAIS) -> str:
    from pipeline.qa_research.piloto_janela.core import blocos
    itens = sorted(p.name for p in Path(docs).iterdir() if (p / "documento.json").exists())
    n = sum(len(blocos(i, Path(docs))[1]) for i in itens)
    return (f"{len(itens)} documentos, {n} blocos foco: visita 1 em todos ({n} chamadas do gerador, GPT-5.4 high); "
            f"cada foco volta enquanto a visita anterior trouxer ao menos uma válida nova (teto de {visitas} visitas, "
            f"no máximo {n * visitas} chamadas); auditor v23, sustentação e deduplicação das válidas a cada visita.")
