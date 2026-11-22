"""Loops da geração final v3: gerações dirigidas que completam o banco da geração principal (relatorios/geracao_final_v3).

A geração principal pede os seis tipos de uma vez e prioriza decisão e procedimento; o banco saiu com poucas questões
de conceito, mecanismo e consequência (que são justamente as de maior taxa de válidas) e com dois documentos de gestão
quase vazios (1.1 e 8.4, em que mais de 80% das questões caíram em atalho). Cada loop roda na mesma pasta, com o mesmo
mecanismo da principal (retroalimentação sem memória, datasets externos, convertidas em xadrez, auditor v23, gabarito de
até 20 palavras, sustentação) e com a MESMA deduplicação: toda válida de um loop é comparada com todas as válidas já
aceitas do documento, da principal e dos outros loops. Uma visita só conta como produtiva se trouxe válida nova.

Loops (`LOOPS`):
  conceito, mecanismo, consequencia, diagnostico, procedimento, decisao
      um tipo por loop (prompts/final3_tipo.md com a definição, o modo de fazer e os defeitos do tipo, de
      loops_v3.json); 0 a 3 questões por chamada, só do tipo pedido (as de outro tipo são descartadas); boas e ruins
      fixas do tipo (conceito: exemplos_conceito.json; os demais: válidas e reprovadas da geração principal, de
      documentos diferentes); boas e ruins sorteadas só do mesmo tipo, de tudo o que a principal e os loops já
      julgaram em outros documentos; convertidas do mesmo tipo. Um foco fecha na visita em que o gerador não propõe
      nenhuma questão (o bloco não sustenta o tipo) ou após PACIENCIA visitas seguidas sem válida nova.
  manual
      questões escritas à mão para 1.1 e 8.4 (gestao_manuais.json), sem gerador: passam pelo mesmo auditor, pela
      mesma sustentação e pela mesma deduplicação.
  composta
      questões que exigem juntar um elo de cada um de dois blocos distantes do mesmo documento ([F1] e [F2], a pelo
      menos DISTANCIA_PAR blocos um do outro); o par de cada bloco é o mais parecido com ele pelos embeddings da
      deduplicação, escolhido uma vez e gravado (loop_composta/pares.json); 0 a 2 questões por chamada, e só ficam as
      que citam os dois blocos nos fundamentos (prompts/final3_composta.md); até 3 visitas por par.
  reparo
      conserto das reprovadas por um único defeito (só atalho, só várias respostas, ou aprovada pelo auditor com o
      gabarito não sustentado), de todas as origens: o GPT-5.4 recebe a questão, o parecer do revisor (o que entrega a
      resposta, a alternativa não excluída ou as afirmações sem apoio), a janela e as questões já aceitas sobre os
      mesmos blocos, e conserta ou descarta (prompts/final3_reparo.md); a consertada passa de novo por auditor,
      sustentação e deduplicação. Uma tentativa por questão; a seleção fica gravada (loop_reparo/selecao.jsonl) e só
      cresce: rodar de novo depois de outro loop conserta só as reprovadas novas.
  gestao
      1.1 e 8.4, com prompt próprio (prompts/final3_gestao.md: o que tem conhecimento técnico nesses temas, os atalhos
      típicos e o teste de apagar do enunciado a falha, o objetivo e a categoria), boas fixas do outro documento
      (incluindo as manuais) e ruins de atalho reais; exemplos sorteados com metade dos documentos de gestão vizinhos;
      até 12 visitas, paciência 3.

Quando o banco v3 (relatorios/petroquest_banco_v3) já tem revisões, os exemplos sorteados dos loops passam a usar o
julgamento final: as válidas reprovadas na revisão de unicidade viram ruins (com o motivo da revisão, cota própria),
e metade das boas sorteadas é das que o GPT-5 erra sem contexto (marcadas como difíceis).

python -m pipeline.qa_research.experimento_ab final-v3-loops [--loops conceito,mecanismo,...] [--etapas ...]
"""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.geracao_tipos.rodadas import _filtrado

from . import comum as C
from .ablacao_v3 import (AUDITOR, CHAVES_REGRAS, CONFIGS, DEFEITO, GERADOR, MISTURA_EXTERNOS, N_CONVERTIDAS, SORTEIO_V2,
                         _boa, _rng, _ruim, bloco_fixas, categoria, codigo_semente, estratificado, validar_geracao)
from .dedup import centrar
from .v22 import TIPOS
from .final_v3 import CONFIG, DOCS_FINAIS, SAIDA, GeracaoFinalV3
from .final_v3 import markdown as markdown_final
from .variada import bloco_forma

AQUI = Path(__file__).resolve().parent
DADOS = AQUI / "loops_v3.json"
MANUAIS = AQUI / "gestao_manuais.json"
TIPOS_LOOP = ("conceito", "mecanismo", "consequencia", "diagnostico", "procedimento", "decisao")
LOOPS = {
    **{t: {"tipo": t, "prompt": "final3_tipo", "visitas": 6, "paciencia": 2, "fecha_sem_questao": True}
       for t in TIPOS_LOOP},
    "manual": {"tipo": None, "prompt": None, "visitas": 1, "paciencia": 1, "fecha_sem_questao": False,
               "manual": True, "gestao": True},
    "gestao": {"tipo": None, "prompt": "final3_gestao", "visitas": 12, "paciencia": 3, "fecha_sem_questao": False,
               "gestao": True},
    "composta": {"tipo": None, "prompt": "final3_composta", "visitas": 3, "paciencia": 1, "fecha_sem_questao": True,
                 "composta": True},
    "reparo": {"tipo": None, "prompt": "final3_reparo", "visitas": 1, "paciencia": 1, "fecha_sem_questao": False,
               "reparo": True},
}
# Ordem padrão: os tipos com menos questões no banco e maior taxa de válidas primeiro; depois as manuais (que entram no
# banco antes das geradas para os mesmos conhecimentos) e o loop de gestão. Decisão e procedimento já são a maioria do
# banco da principal e só rodam se pedidos (--loops).
PADRAO = ("conceito", "mecanismo", "consequencia", "diagnostico", "composta", "manual", "gestao")
POR_CHAMADA = 3
POR_CHAMADA_COMPOSTA = 2
DISTANCIA_PAR = 3          # blocos de distância mínima entre [F1] e [F2] (fora da mesma janela de 3 blocos)
POR_LOTE_REPARO = 5        # questões a consertar por chamada (do mesmo foco)
REVISAO = C.QA / "relatorios" / "petroquest_banco_v3"
CODIGO_REVISAO = {"R5": "varias_respostas", "R6": "nao_unico", "R7": "depende_do_documento",
                  "R9": "depende_do_documento", "R10": "atalho"}
DESCR_REVISAO = {"R5": "outra resposta também é correta", "R6": "gabarito vago", "R7": "depende do documento",
                 "R9": "o enunciado precisa do documento", "R10": "trivial"}
COTAS_V3 = {"revisao": 2, "atalho": 3, "varias_respostas": 2, "nao_sustentada": 1}   # ruins com a revisão final
CHAVES_MANUAL = ("tipo", "cenario", "conhecimento", "pergunta", "resposta", "explicacao", "resposta_padrao",
                 "por_que_nao", "fundamentos")
# respostas de conceito que são enquadramento regulatório, não vocabulário (não servem de boa sorteada)
NORMA = re.compile(r"^\s*(NR[- ]?\d|NORMAM|ANP\b|ASME|API\b|ISO\b|IEC\b|CONAMA|IBAMA|Marinha)", re.I)
CABECALHO_EXEMPLOS = ("São questões de outros documentos. As boas passaram em todas as verificações (autocontidas, de "
                      "resposta única, sem atalho e com o gabarito sustentado pelos blocos); as ruins foram reprovadas "
                      "pelo defeito indicado. Não copie assunto, cenário nem estrutura.")


def carregar_dados(caminho: Path = DADOS) -> dict:
    d = read_json(caminho)
    if not d or d.get("schema") != "loops-v3" or set(d["tipos"]) != set(TIPOS_LOOP):
        raise ValueError(f"{C.relativo(Path(caminho))}: dados dos loops inválidos")
    return d


def carregar_manuais(caminho: Path = MANUAIS) -> list[dict]:
    d = read_json(caminho)
    if not d or d.get("schema") != "gestao-manuais-v1":
        raise ValueError(f"{C.relativo(Path(caminho))}: questões manuais inválidas")
    for q in d["questoes"]:
        if set(CHAVES_MANUAL) - set(q) or not isinstance(q.get("foco"), int):
            raise ValueError(f"questão manual incompleta: {q.get('pergunta', '')[:60]}")
    return d["questoes"]


def carregar_revisao(pasta: Path = REVISAO) -> dict:
    """uid -> {"regra": regra da revisão final que a reprova ou None, "justificativa", "dificil"} do banco v3."""
    pasta, out = Path(pasta), {}
    if not pasta.is_dir():
        return out
    from .banco_v3 import regra_revisao
    if (pasta / "revisoes.jsonl").exists():
        revs = C.linhas(pasta / "revisoes.jsonl")
    else:
        revs = [read_json(p) for p in sorted((pasta / "unicidade").glob("*.json")) if p.name != "config.json"] \
            if (pasta / "unicidade").is_dir() else []
    for r in revs:
        if r and r.get("status") == "revisada":
            rj = regra_revisao(r)
            out[r["uid"]] = {"regra": rj[0] if rj else None, "justificativa": r["justificativa"]}
    if (pasta / "banco.jsonl").exists():
        for b in C.linhas(pasta / "banco.jsonl"):
            sc = b["dificuldade"]["sem_contexto"]
            out.setdefault(b["uid"], {"regra": None, "justificativa": ""})["dificil"] = \
                sc.get("gpt-5") not in (None, "", "correta")
    return out


def escolher_pares(bs: list[dict], embedder, media) -> list[list[int]]:
    """Para cada bloco, o bloco mais parecido a pelo menos DISTANCIA_PAR blocos dele (cosseno centrado); pares únicos."""
    import numpy as np
    if len(bs) <= DISTANCIA_PAR:
        return []
    V = centrar(embedder.encode([f"{b['subtitulo']}\n{b['texto']}"[:8000] for b in bs]), np.asarray(media))
    S = V @ V.T
    pares = set()
    for a in range(len(bs)):
        cand = [b for b in range(len(bs)) if abs(a - b) >= DISTANCIA_PAR]
        if cand:
            b = max(cand, key=lambda j: (S[a, j], -j))
            pares.add((min(a, b), max(a, b)))
    return [list(p) for p in sorted(pares)]


def validar_reparo(d: dict, ids: list[str]) -> None:
    if not isinstance(d, dict) or set(d) != {"reparos"} or not isinstance(d["reparos"], list):
        raise ValueError('Retorne {"reparos": [...]}, um objeto por questão recebida.')
    if sorted(r.get("id") for r in d["reparos"] if isinstance(r, dict)) != sorted(ids):
        raise ValueError(f"reparos deve ter exatamente um objeto para cada id: {ids}")
    for r in d["reparos"]:
        if r.get("acao") not in ("reparada", "descartada") or not isinstance(r.get("motivo"), str) \
                or set(r) != {"id", "acao", "motivo", "questao"}:
            raise ValueError("cada reparo tem id, acao (reparada ou descartada), motivo e questao")
        q = r["questao"]
        if r["acao"] == "descartada":
            if q is not None:
                raise ValueError("questao deve ser null quando a ação é descartada")
            continue
        if not isinstance(q, dict) or set(q) != CHAVES_REGRAS | {"fundamentos"} or q.get("tipo") not in TIPOS \
                or not str(q.get("pergunta", "")).strip() or not str(q.get("resposta", "")).strip() \
                or not isinstance(q.get("fundamentos"), list):
            raise ValueError(f"questao reparada precisa das chaves {sorted(CHAVES_REGRAS | {'fundamentos'})} e de "
                             "um tipo válido")


class LoopFinalV3(GeracaoFinalV3):
    PREFIXO = "PQ3L"
    EXTRA_CONFIGS = {f"loop_{n}": CONFIGS[CONFIG] for n in LOOPS}

    def __init__(self, loop: str, saida: Path = SAIDA, *, docs: Path = DOCS_FINAIS, visitas: int | None = None,
                 paciencia: int | None = None, itens=None, dados: Path = DADOS, manuais: Path = MANUAIS,
                 revisao: Path = REVISAO, **kw):
        if loop not in LOOPS:
            raise ValueError(f"loop desconhecido: {loop} (válidos: {', '.join(LOOPS)})")
        self.loop, self.spec, self.c = loop, LOOPS[loop], f"loop_{loop}"
        self.FECHA_SEM_QUESTAO = bool(self.spec["fecha_sem_questao"])
        self.dados = carregar_dados(dados)
        self.arq_dados, self.arq_manuais = Path(dados), Path(manuais)
        self.manuais = carregar_manuais(manuais) if self.spec.get("gestao") else []
        self.grupo_gestao = set(self.dados["gestao"]["itens"])
        if self.spec.get("gestao") and itens is None:
            itens = sorted(self.grupo_gestao)
        if not (Path(saida) / CONFIG / "geracao").is_dir():
            raise ValueError(f"Os loops completam a geração principal: rode antes o final-v3 em {C.relativo(Path(saida))}")
        self._base, self._banco_cache = None, None
        self.revisao = {} if self.spec.get("manual") or self.spec.get("reparo") else carregar_revisao(revisao)
        super().__init__(saida, docs=docs, visitas=visitas or self.spec["visitas"],
                         paciencia=paciencia or self.spec["paciencia"], itens=itens, **kw)

    # -------------------------------------------------------------- registro do loop
    def _config(self) -> None:
        """Cada loop registra o que o define em <pasta>/loop_<nome>/config.json; teto de visitas e paciência podem mudar
        entre execuções (a decisão de reabrir um foco é refeita a cada execução)."""
        docs = {i: C.sha(read_json(self.docs_dir / i / "documento.json")) for i in sorted(self.todos)}
        principal = read_json(self.saida / "config.json") or {}
        if principal.get("docs_sha256") and principal["docs_sha256"] != docs:
            raise ValueError("Os contextos mudaram em relação aos da geração principal; os loops usam os mesmos")
        cfg = {"schema": "final-v3-loop", "loop": self.loop, "itens": self.itens,
               "spec": {k: v for k, v in self.spec.items() if k not in ("visitas", "paciencia")},
               "por_chamada": POR_CHAMADA, "gerador": GERADOR, "auditor": AUDITOR,
               "mistura_externos": MISTURA_EXTERNOS, "n_convertidas": N_CONVERTIDAS,
               "prompt_sha256": C.sha(self.prompt_loop()) if not self.spec.get("manual") else None,
               "retro_sha256": C.sha(C.prompt("abl3_retro_v2")), "auditoria_sha256": C.sha(C.prompt("auditoria_v23")),
               "dados_sha256": C.sha(json.dumps(self._dados_loop(), sort_keys=True, ensure_ascii=False)),
               "docs_sha256": docs}
        arq = self.saida / self.c / "config.json"
        if arq.exists():
            antigo = read_json(arq)
            fixos = lambda d: {k: v for k, v in d.items()  # noqa: E731
                               if k not in ("criado_em", "visitas", "paciencia", "usa_revisao_final")}
            if json.dumps(fixos(antigo), sort_keys=True) != json.dumps(fixos(cfg), sort_keys=True):
                diff = sorted(k for k in set(fixos(antigo)) | set(fixos(cfg))
                              if json.dumps(antigo.get(k), sort_keys=True) != json.dumps(cfg.get(k), sort_keys=True))
                raise ValueError(f"O loop {self.loop} mudou em relação à pasta existente ({', '.join(diff)}); apague "
                                 f"{C.relativo(arq.parent)} para refazê-lo")
            cfg["criado_em"] = antigo.get("criado_em")
        atomic_json(arq, {**cfg, "visitas": self.visitas, "paciencia": self.paciencia,
                          "criado_em": cfg.get("criado_em") or datetime.now(timezone.utc).isoformat(),
                          "usa_revisao_final": bool(self.revisao)})

    def _dados_loop(self):
        if self.spec.get("manual"):
            return self.manuais
        if self.spec.get("reparo"):
            return {"por_lote": POR_LOTE_REPARO}
        if self.spec.get("composta"):
            return {"composta": self.dados["composta"], "distancia_par": DISTANCIA_PAR,
                    "por_chamada": POR_CHAMADA_COMPOSTA}
        if self.spec.get("gestao"):
            return {"gestao": self.dados["gestao"], "manuais": self.manuais}
        d = self.dados["tipos"][self.spec["tipo"]]
        if d.get("exemplos"):
            return {**d, "arquivo": read_json(AQUI / d["exemplos"])}
        return d

    def pasta_banco(self) -> Path:
        return self.saida / self.c

    def markdown(self, res: dict) -> str:
        return markdown_final(res).replace("# Geração final v3: banco de questões",
                                           f"# Geração final v3, loop {self.loop}: banco de questões", 1)

    # -------------------------------------------------------------- unidades
    def _unidades(self) -> list[dict]:
        if self.spec.get("composta"):
            return self._unidades_pares()
        if self.spec.get("reparo"):
            return self._unidades_reparo()
        if not self.spec.get("manual"):
            return super()._unidades()
        self.fechados = {}
        focos = sorted({(q["item"], q["foco"]) for q in self.manuais if q["item"] in self.itens})
        for i, f in focos:
            if not 0 <= f < len(self.docs[i]):
                raise ValueError(f"questão manual de {i} com foco fora do documento: {f}")
        return [self._unidade(i, f, 1) for i, f in focos]

    @staticmethod
    def _unidade_par(item: str, a: int, b: int, visita: int) -> dict:
        return {"item": item, "foco": a, "par": b, "visita": visita, "onda": (visita - 1) * 2 + a % 2,
                "id": f"{item}:{a:03d}x{b:03d}:v{visita}"}

    def pares(self) -> dict:
        """Pares de blocos por documento, escolhidos uma vez (embeddings) e gravados para a retomada."""
        arq = self.saida / self.c / "pares.json"
        d = read_json(arq) if arq.exists() else {}
        faltam = [i for i in self.itens if i not in d]
        if faltam:
            for i in faltam:
                d[i] = escolher_pares(self.docs[i], self.embedder, self.media)
            arq.parent.mkdir(parents=True, exist_ok=True)
            atomic_json(arq, d)
        return d

    def _unidades_pares(self) -> list[dict]:
        """Como a saturação por foco, com o par de blocos no lugar do foco."""
        out, self.fechados = [], {}
        pares = self.pares()
        for i in self.itens:
            abertos = {tuple(p): 0 for p in pares[i]}
            for v in range(1, self.visitas + 1):
                if not abertos:
                    break
                us = [self._unidade_par(i, a, b, v) for a, b in sorted(abertos)]
                out += us
                estados = [self._estado(u) for u in us]
                if not all(e[0] for e in estados):
                    break
                for u, (_, novas, geradas) in zip(us, estados):
                    k = (u["foco"], u["par"])
                    abertos[k] = 0 if novas else abertos[k] + 1
                    if abertos[k] >= self.paciencia or (self.FECHA_SEM_QUESTAO and not geradas):
                        self.fechados[(i, f"{k[0]}x{k[1]}")] = v
                        del abertos[k]
        return out

    # -------------------------------------------------------------- reparo
    def defeituosas(self) -> list[dict]:
        """Reprovadas por um único defeito consertável, de todas as origens (menos o próprio reparo)."""
        out = []
        for c in self.configs_em_disco():
            if c == self.c:
                continue
            for u in self.unidades_em_disco(c):
                if u["item"] not in self.itens:
                    continue
                for q in self.finais(c, [u]):
                    a, f = q["auditoria"], set(q["auditoria"].get("falhas", []))
                    if not q["resposta_curta"] or a.get("motivo") == "bloqueio":
                        continue
                    if not q["aprovada_auditor"] and f in ({"atalho"}, {"varias_respostas"}):
                        cod, extra = next(iter(f)), {}
                        if cod == "varias_respostas":
                            extra = {"resposta_alternativa": a.get("resposta_alternativa")}
                    elif q["aprovada_auditor"] and q["sustentacao"] in ("suporte_insuficiente", "contradicao"):
                        cod = "nao_sustentada"
                        s = read_json(self._arq_sust(q["uid"])) or {}
                        sem = [e["afirmacao"] for e in s.get("evidencias", []) if e["veredito"] != "sustentada"]
                        extra = {"afirmacoes_sem_apoio": sem or
                                 f"{int(s.get('insuficiente') or 0) + int(s.get('contradita') or 0)} de "
                                 f"{s.get('afirmacoes')} afirmações do gabarito"}
                    else:
                        continue
                    out.append({"uid": q["uid"], "item": u["item"], "foco": u["foco"], "par": u.get("par"),
                                "codigo": cod, "parecer": a.get("justificativa", ""), **extra,
                                **{k: q.get(k) for k in ("tipo", "pergunta", "resposta", "explicacao",
                                                         "resposta_padrao", "por_que_nao", "conhecimento")}})
        return out

    def selecao(self) -> list[dict]:
        """Seleção gravada; as reprovadas novas entram em lotes novos (o que já foi selecionado não muda)."""
        arq = self.saida / self.c / "selecao.jsonl"
        sel = C.linhas(arq) if arq.exists() else []
        vistos = {s["uid"] for s in sel}
        novas = [q for q in self.defeituosas() if q["uid"] not in vistos]
        if novas:
            lote = Counter()
            for s in sel:
                lote[(s["item"], s["foco"], s.get("par"))] = max(lote[(s["item"], s["foco"], s.get("par"))], s["lote"])
            grupos: dict = {}
            for q in novas:
                grupos.setdefault((q["item"], q["foco"], q.get("par")), []).append(q)
            for k, qs in sorted(grupos.items(), key=lambda x: (x[0][0], x[0][1], x[0][2] or -1)):
                for j in range(0, len(qs), POR_LOTE_REPARO):
                    lote[k] += 1
                    sel += [{**q, "lote": lote[k]} for q in qs[j:j + POR_LOTE_REPARO]]
            arq.parent.mkdir(parents=True, exist_ok=True)
            C.gravar_jsonl(arq, sel)
        return sel

    def _unidades_reparo(self) -> list[dict]:
        self.fechados = {}
        self._sel = {}
        for s in self.selecao():
            self._sel.setdefault((s["item"], s["foco"], s.get("par"), s["lote"]), []).append(s)
        out = []
        for (i, f, par, lote) in sorted(self._sel, key=lambda k: (k[0], k[1], k[2] or -1, k[3])):
            out.append(self._unidade(i, f, lote) if par is None else self._unidade_par(i, f, par, lote))
        self.visitas = max([u["visita"] for u in out] or [1])
        return out

    def _no_banco(self, u: dict) -> list[dict]:
        """Válidas aceitas (não redundantes) que usam algum bloco da janela desta unidade."""
        if self._banco_cache is None:
            red = self.redundantes() if self.pasta_dedup().exists() else {}
            self._banco_cache = {}
            for q in self.validas_banco():
                if q["uid"] not in red:
                    self._banco_cache.setdefault(q["item"], []).append(
                        ({b["indice_documento"] for b in q["blocos_contexto"]}, q["pergunta"], q["resposta"]))
        blocos_u = {b["indice"] for _, b in self._janela(u)[0]}
        return [{"pergunta": p, "resposta": r} for idx, p, r in self._banco_cache.get(u["item"], []) if idx & blocos_u]

    def usuario(self, c: str, u: dict, julgadas: list[dict] | None = None) -> str:
        if not self.spec.get("reparo"):
            return super().usuario(c, u, julgadas)
        sel = self._sel[(u["item"], u["foco"], u.get("par"), u["visita"])]
        qs = []
        for k, s in enumerate(sel, 1):
            q = {"id": f"Q{k}", "defeito": s["codigo"], "parecer_do_revisor": s["parecer"],
                 **{x: s.get(x) for x in ("tipo", "pergunta", "resposta", "explicacao", "resposta_padrao", "por_que_nao")}}
            for x in ("resposta_alternativa", "afirmacoes_sem_apoio"):
                if s.get(x):
                    q[x] = s[x]
            qs.append(q)
        banco = self._no_banco(u)
        return "\n\n".join([self._tema(u["item"]), f"<janela>\n{self._janela(u)[1]}\n</janela>",
                             "<ja_no_banco>\n" + ("\n".join(f"- {b['pergunta']} → {b['resposta']}" for b in banco)
                                                  or "Nenhuma.") + "\n</ja_no_banco>",
                             "<questoes_a_consertar>\n" + json.dumps(qs, ensure_ascii=False, indent=1)
                             + "\n</questoes_a_consertar>", f"Pedido: {u['id']}"])

    # -------------------------------------------------------------- prompt
    def prompt_loop(self) -> str:
        if self.spec["prompt"] == "final3_tipo":
            t, d = self.spec["tipo"], self.dados["tipos"][self.spec["tipo"]]
            s = C.prompt("final3_tipo")
            for k, v in {"<<TIPO>>": t, "<<DEFINICAO>>": d["definicao"],
                         "<<COMO>>": "\n".join(f"- {x}" for x in d["como"]),
                         "<<ARMADILHAS>>": "\n".join(f"- {x}" for x in d["armadilhas"]),
                         "<<RESPOSTA_MAX>>": str(d["resposta_max"]), "<<PERGUNTA_MAX>>": str(d["pergunta_max"]),
                         "<<CENARIO>>": d["cenario"]}.items():
                s = s.replace(k, v)
        elif self.spec["prompt"]:
            s = C.prompt(self.spec["prompt"])
        else:
            return ""
        if "<<" in s:
            raise ValueError(f"marcador não resolvido no prompt do loop {self.loop}")
        return s.strip()

    def _fixos(self) -> tuple[list, list, list]:
        """(boas, reservas, ruins) fixas do loop."""
        if self.spec.get("reparo"):
            return [], [], []
        if self.spec.get("composta"):
            k = self.dados["composta"]
            return k["boas"], k["reservas"], k["ruins"]
        if self.spec.get("gestao"):
            g = self.dados["gestao"]
            manuais = [{"id": f"MAN{k:02d}", **{c: q[c] for c in ("item", "tipo", "pergunta", "resposta",
                                                                  "resposta_padrao", "por_que_nao")}}
                       for k, q in enumerate(self.manuais, 1)]
            return g["boas"], manuais, g["ruins"]
        d = self.dados["tipos"][self.spec["tipo"]]
        if d.get("exemplos"):
            e = read_json(AQUI / d["exemplos"])
            return e["boas"], e["reservas"], e["ruins"]
        return d["boas"], d["reservas"], d["ruins"]

    def _semente(self, item: str) -> tuple[list, list, list, list]:
        """4 boas e 4 ruins fixas de outros documentos (reservas cobrem as do mesmo documento); o resto vai ao sorteio."""
        boas, reservas, ruins = self._fixos()
        livres = [e for e in boas + reservas if e["item"] != item]
        fb = livres[:4]
        rr = [e for e in ruins if e["item"] != item]
        return fb, rr[:4], livres[4:], rr[4:]

    def sistema(self, c: str, item: str) -> str:
        if self.spec.get("reparo"):
            return self.prompt_loop()
        retro = C.prompt("abl3_retro_v2").split("# Exemplos de referência")[0].rstrip()
        fb, fr, _, _ = self._semente(item)
        return f"{self.prompt_loop()}\n\n{retro}\n\n# Exemplos de referência\n\n{CABECALHO_EXEMPLOS}\n\n{bloco_fixas(fb, fr)}"

    # -------------------------------------------------------------- exemplos sorteados
    def _julgadas_base(self) -> list[dict]:
        """Tudo o que a principal e os outros loops já julgaram (lido uma vez por execução)."""
        if self._base is None:
            out = []
            for c in self.configs_em_disco():
                if c == self.c:
                    continue
                for u in self.unidades_em_disco(c):
                    for q in self._questoes_unidade(c, u):
                        ok, cod, motivo = self._julgamento_v2(q)
                        if ok is None:
                            continue
                        rv = self.revisao.get(q["uid"]) or {}
                        if ok and rv.get("regra"):           # válida, mas reprovada na revisão final
                            ok, cod = False, CODIGO_REVISAO[rv["regra"]]
                            motivo = f"Reprovada na revisão final ({DESCR_REVISAO[rv['regra']]}). {rv['justificativa']}"
                        out.append({**q, "item": u["item"], "foco": u["foco"], "visita": u["visita"], "boa": ok,
                                    "defeito": motivo, "codigo": cod, "revisao": bool(rv.get("regra")),
                                    "dificil": bool(ok and rv.get("dificil"))})
            self._base = out
        return self._base

    def _julgadas(self, c: str, ate_onda: int) -> list[dict]:
        if self.spec.get("reparo") or self.spec.get("manual"):
            return []
        return self._julgadas_base() + super()._julgadas(c, ate_onda)

    def _aceita(self, e: dict) -> bool:
        t = self.spec["tipo"]
        if t and (e.get("tipo") or "?") != t:
            return False
        return not (e.get("boa") and t == "conceito" and NORMA.search(str(e.get("resposta", ""))))

    def _area(self, item: str):
        """No loop de gestão, os documentos de gestão e os vizinhos contam como "mesma área" no sorteio."""
        if self.spec.get("gestao") and item in self.grupo_gestao | set(self.dados["gestao"]["vizinhos"]):
            return "gestao"
        return super()._area(item)

    def _exemplos(self, c: str, u: dict, julgadas: list[dict]) -> list[str]:
        js = [q for q in julgadas if self._aceita(q)]
        if not self.revisao:
            return super()._exemplos(c, u, js)
        return self._exemplos_revisados(c, u, js)

    def _exemplos_revisados(self, c: str, u: dict, julgadas: list[dict]) -> list[str]:
        """Retroalimentação com a revisão final: metade das boas é difícil (o GPT-5 erra sem contexto) e as ruins têm cota
        para os defeitos que só a revisão pegou (gabarito vago, outra resposta correta, dependência do documento)."""
        area = self._area(u["item"])
        mesma = lambda e: area is not None and self._area(e["item"]) == area  # noqa: E731
        tipo = lambda e: e.get("tipo") or "?"  # noqa: E731
        _, _, sb, sr = self._semente(u["item"])
        outras = [q for q in julgadas if q["item"] != u["item"]]
        rng = _rng("exemplos_v3", c, u["id"])
        pool_b = list(sb) + [q for q in outras if q["boa"]]
        boas = estratificado([q for q in pool_b if q.get("dificil")], SORTEIO_V2[0] // 2, rng, tipo, mesma)
        usadas = {id(e) for e in boas}
        boas += estratificado([q for q in pool_b if id(q) not in usadas], SORTEIO_V2[0] - len(boas), rng, tipo, mesma)
        pool_r = [{**e, "codigo": codigo_semente(e["defeito"])} for e in sr] + [q for q in outras if not q["boa"]]
        ruins: list = []
        for cat, n in COTAS_V3.items():
            usadas = {id(e) for e in ruins}
            sel = [e for e in pool_r if id(e) not in usadas and
                   (e.get("revisao") if cat == "revisao" else not e.get("revisao") and categoria(e["codigo"]) == cat)]
            ruins += estratificado(sel, n, rng, tipo, mesma)
        if len(ruins) < SORTEIO_V2[1]:
            usadas = {id(e) for e in ruins}
            ruins += estratificado([e for e in pool_r if id(e) not in usadas], SORTEIO_V2[1] - len(ruins), rng,
                                   lambda e: categoria(e["codigo"]), mesma)
        rng.shuffle(boas)
        rng.shuffle(ruins)
        if outras:
            cont = Counter(q["codigo"] for q in outras if not q["boa"])
            linhas = [f"Questões já julgadas em outros documentos: {len(outras)}; aprovadas em todas as verificações, "
                      f"inclusive a revisão final: {100 * sum(q['boa'] for q in outras) / len(outras):.0f}%. "
                      "Reprovadas por defeito:"]
            linhas += [f"- {DEFEITO.get(k, (k,))[0]}: {100 * v / len(outras):.0f}%" for k, v in cont.most_common()
                       if 100 * v / len(outras) >= 0.5]
            freq = "\n".join(linhas)
        else:
            freq = "Nenhuma questão julgada ainda."
        marca = lambda e: {**e, "tipo": f"{tipo(e)}; difícil: o GPT-5 errou sem contexto"} if e.get("dificil") else e  # noqa: E731
        return [f"<defeitos_frequentes>\n{freq}\n</defeitos_frequentes>",
                "<boas_ja_avaliadas>\n" + ("\n\n".join(_boa(marca(e)) for e in boas) or "Nenhuma ainda.")
                + "\n</boas_ja_avaliadas>",
                "<ruins_ja_avaliadas>\n" + ("\n\n".join(_ruim(e) for e in ruins) or "Nenhuma ainda.")
                + "\n</ruins_ja_avaliadas>"]

    def _forma(self, u: dict) -> str:
        """Externos como na principal; as convertidas, em xadrez, de preferência do mesmo tipo do loop."""
        rng = _rng("forma", self.c, u["id"])
        ex = []
        for fonte, n in MISTURA_EXTERNOS.items():
            pool = self.pools.get(fonte) or [r for v in self.pools.values() for r in v]
            ex += rng.sample(pool, min(n, len(pool)))
        if self.com_convertidas(u):
            outras = [q for q in self.convertidas if q.get("item") != u["item"]] or self.convertidas
            mesmas = [q for q in outras if q.get("tipo") == self.spec["tipo"]]
            pool = mesmas if len(mesmas) >= N_CONVERTIDAS else outras
            ex += rng.sample(pool, min(N_CONVERTIDAS, len(pool)))
        rng.shuffle(ex)
        return bloco_forma(ex)

    # -------------------------------------------------------------- geração
    def _filtrar(self, d: dict) -> dict:
        """Até POR_CHAMADA questões, só do tipo do loop: as de outro tipo são descartadas (registradas), não refeitas.
        Nas compostas, só ficam as que citam os dois blocos nos fundamentos."""
        if self.spec.get("composta"):
            dois = lambda q: {"F1", "F2"} <= {f.get("bloco") for f in q.get("fundamentos") or [] if isinstance(f, dict)}  # noqa: E731
            ok = [q for q in d["questoes"] if dois(q)]
            fora = len(d["questoes"]) - len(ok)
            return {**d, "questoes": ok[:POR_CHAMADA_COMPOSTA], **({"descartadas_composicao": fora} if fora else {})}
        t = self.spec["tipo"]
        fora = [q for q in d["questoes"] if t and q.get("tipo") != t]
        ok = [q for q in d["questoes"] if not (t and q.get("tipo") != t)][:POR_CHAMADA]
        extra = {"descartadas_tipo": len(fora)} if fora else {}
        return {**d, "questoes": ok, **extra}

    def _gerar(self, c: str, u: dict, julgadas: list[dict] | None) -> bool:
        arq = self._arq_ger(c, u)
        nome = f"geracao_{c}_{arq.stem}"
        if arq.exists():
            return True
        if self.spec.get("reparo"):
            return self._reparar(c, u, arq, nome)
        if self.spec.get("manual"):
            qs = [{k: q[k] for k in CHAVES_MANUAL} for q in self.manuais
                  if q["item"] == u["item"] and q["foco"] == u["foco"]]
            atomic_json(arq, {**u, "config": c, "motivo": "", "questoes": qs, "origem": "manual"})
            return True
        try:
            d = self.cliente("geracao").json(self.sistema(c, u["item"]), self.usuario(c, u, julgadas), tag=f"final3_{c}",
                                             max_tokens=16000, item=u["item"],
                                             validate=lambda d: validar_geracao(d, CHAVES_REGRAS))
            d = self._filtrar(d)
        except Exception as exc:  # noqa: BLE001
            if not _filtrado(exc):
                self._falha(nome, exc)
                return False
            d = {"questoes": [], "motivo": "bloqueado pelo filtro de conteúdo"}
        atomic_json(arq, {**u, "config": c, "motivo": d["motivo"], "questoes": d["questoes"],
                          **{k: d[k] for k in ("descartadas_tipo", "descartadas_composicao") if d.get(k)}})
        self._ok(nome)
        return True

    def _reparar(self, c: str, u: dict, arq: Path, nome: str) -> bool:
        sel = self._sel[(u["item"], u["foco"], u.get("par"), u["visita"])]
        ids = [f"Q{k}" for k in range(1, len(sel) + 1)]
        try:
            d = self.cliente("geracao").json(self.sistema(c, u["item"]), self.usuario(c, u), tag=f"final3_{c}",
                                             max_tokens=16000, item=u["item"], validate=lambda d: validar_reparo(d, ids))
        except Exception as exc:  # noqa: BLE001
            if not _filtrado(exc):
                self._falha(nome, exc)
                return False
            d = {"reparos": [{"id": i, "acao": "descartada", "motivo": "bloqueado pelo filtro de conteúdo",
                              "questao": None} for i in ids]}
        por_id = {r["id"]: r for r in d["reparos"]}
        questoes, reparos = [], []
        for i, s in zip(ids, sel):
            r = por_id[i]
            reparos.append({"id": i, "origem_uid": s["uid"], "defeito": s["codigo"], "acao": r["acao"],
                            "motivo": r["motivo"]})
            if r["acao"] == "reparada":
                questoes.append({**r["questao"], "origem_uid": s["uid"], "origem_defeito": s["codigo"]})
        atomic_json(arq, {**u, "config": c, "motivo": "" if questoes else "nenhuma reparada", "questoes": questoes,
                          "reparos": reparos})
        self._ok(nome)
        return True


def executar_loops(loops=PADRAO, etapas=None, *, visitas: int | None = None, paciencia: int | None = None,
                   progress=print, **kw) -> int:
    """Roda os loops em sequência (cada um depende do banco deixado pelos anteriores); para no primeiro incompleto."""
    from .final_v3 import ETAPAS
    for nome in loops:
        g = LoopFinalV3(nome, visitas=visitas, paciencia=paciencia, progress=progress, **kw)
        progress(f"[loop {nome}] {plano_loop(g)}", flush=True)
        st = g.executar(tuple(etapas or ETAPAS))
        if st:
            progress(f"[loop {nome}] incompleto; repita o mesmo comando", flush=True)
            return st
    gravar_resumo(kw.get("saida") or SAIDA)
    return 0


def plano_loop(g: LoopFinalV3) -> str:
    n = sum(len(g.docs[i]) for i in g.itens)
    if g.spec.get("manual"):
        return f"{len(g.manuais)} questões escritas à mão em {len(g.unidades)} blocos de {', '.join(g.itens)} (sem gerador)"
    if g.spec.get("reparo"):
        sel = C.linhas(g.saida / g.c / "selecao.jsonl") if (g.saida / g.c / "selecao.jsonl").exists() else []
        return (f"{len(sel)} reprovadas por um único defeito ({dict(Counter(s['codigo'] for s in sel))}) em "
                f"{len(g.unidades)} chamadas de conserto; cada consertada volta ao auditor, à sustentação e à deduplicação")
    if g.spec.get("composta"):
        n = sum(len(v) for k, v in g.pares().items() if k in g.itens)
        return (f"{n} pares de blocos distantes em {len(g.itens)} documentos; até {g.visitas} visitas por par "
                f"(fecha na visita sem questão composta)")
    return (f"{len(g.itens)} documentos, {n} blocos foco; visita 1 em todos, depois só os focos com válida nova "
            f"(paciência {g.paciencia}, teto de {g.visitas} visitas"
            + ("; fecha na visita sem nenhuma questão do tipo" if g.FECHA_SEM_QUESTAO else "") + ")")


def gravar_resumo(saida: Path = SAIDA) -> dict:
    """LOOPS.md: o que cada loop acrescentou ao banco único (únicas que ficaram depois da deduplicação conjunta)."""
    saida = Path(saida)
    linhas = ["# Geração final v3: loops", "",
              "Cada loop roda sobre os mesmos contextos e entra na mesma deduplicação da geração principal; \"únicas\" "
              "são as válidas que não são equivalentes a nenhuma válida anterior do documento, de qualquer origem.", "",
              "| Loop | Chamadas | Geradas | Válidas | % válidas | Únicas |", "|---|---|---|---|---|---|"]
    out = {}
    for c in [CONFIG] + sorted(p.name for p in saida.glob("loop_*") if (p / "banco_resumo.json").exists()):
        r = read_json((saida if c == CONFIG else saida / c) / "banco_resumo.json")
        if not r:
            continue
        out[c] = r
        linhas.append(f"| {c} | {r['chamadas']} | {r['geradas']} | {r['validas']} | {r['taxa_validas']:.1f}% | "
                      f"{r['unicas']} |")
    tipos = Counter()
    for r in out.values():
        tipos.update(r.get("tipos_unicas", {}))
    linhas += ["", f"Únicas no total: {sum(r['unicas'] for r in out.values())}.", "",
               "Tipos (únicas, todas as origens): " + ", ".join(f"{k} {v}" for k, v in tipos.most_common()) + "."]
    (saida / "LOOPS.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return out
