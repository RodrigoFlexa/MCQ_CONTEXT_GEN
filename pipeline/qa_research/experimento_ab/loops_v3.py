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
  gestao
      1.1 e 8.4, com prompt próprio (prompts/final3_gestao.md: o que tem conhecimento técnico nesses temas, os atalhos
      típicos e o teste de apagar do enunciado a falha, o objetivo e a categoria), boas fixas do outro documento
      (incluindo as manuais) e ruins de atalho reais; exemplos sorteados com metade dos documentos de gestão vizinhos;
      até 12 visitas, paciência 3.

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
from .ablacao_v3 import CHAVES_REGRAS, CONFIGS, GERADOR, AUDITOR, N_CONVERTIDAS, MISTURA_EXTERNOS, _rng, bloco_fixas, \
    validar_geracao
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
}
# Ordem padrão: os tipos com menos questões no banco e maior taxa de válidas primeiro; depois as manuais (que entram no
# banco antes das geradas para os mesmos conhecimentos) e o loop de gestão. Decisão e procedimento já são a maioria do
# banco da principal e só rodam se pedidos (--loops).
PADRAO = ("conceito", "mecanismo", "consequencia", "diagnostico", "manual", "gestao")
POR_CHAMADA = 3
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


class LoopFinalV3(GeracaoFinalV3):
    PREFIXO = "PQ3L"
    EXTRA_CONFIGS = {f"loop_{n}": CONFIGS[CONFIG] for n in LOOPS}

    def __init__(self, loop: str, saida: Path = SAIDA, *, docs: Path = DOCS_FINAIS, visitas: int | None = None,
                 paciencia: int | None = None, itens=None, dados: Path = DADOS, manuais: Path = MANUAIS, **kw):
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
        self._base = None
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
            fixos = lambda d: {k: v for k, v in d.items() if k not in ("criado_em", "visitas", "paciencia")}  # noqa: E731
            if json.dumps(fixos(antigo), sort_keys=True) != json.dumps(fixos(cfg), sort_keys=True):
                diff = sorted(k for k in set(fixos(antigo)) | set(fixos(cfg))
                              if json.dumps(antigo.get(k), sort_keys=True) != json.dumps(cfg.get(k), sort_keys=True))
                raise ValueError(f"O loop {self.loop} mudou em relação à pasta existente ({', '.join(diff)}); apague "
                                 f"{C.relativo(arq.parent)} para refazê-lo")
            cfg["criado_em"] = antigo.get("criado_em")
        atomic_json(arq, {**cfg, "visitas": self.visitas, "paciencia": self.paciencia,
                          "criado_em": cfg.get("criado_em") or datetime.now(timezone.utc).isoformat()})

    def _dados_loop(self):
        if self.spec.get("manual"):
            return self.manuais
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
        if not self.spec.get("manual"):
            return super()._unidades()
        self.fechados = {}
        focos = sorted({(q["item"], q["foco"]) for q in self.manuais if q["item"] in self.itens})
        for i, f in focos:
            if not 0 <= f < len(self.docs[i]):
                raise ValueError(f"questão manual de {i} com foco fora do documento: {f}")
        return [self._unidade(i, f, 1) for i, f in focos]

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
                        if ok is not None:
                            out.append({**q, "item": u["item"], "foco": u["foco"], "visita": u["visita"], "boa": ok,
                                        "defeito": motivo, "codigo": cod})
            self._base = out
        return self._base

    def _julgadas(self, c: str, ate_onda: int) -> list[dict]:
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
        return super()._exemplos(c, u, [q for q in julgadas if self._aceita(q)])

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
        """Até POR_CHAMADA questões, só do tipo do loop: as de outro tipo são descartadas (registradas), não refeitas."""
        t = self.spec["tipo"]
        fora = [q for q in d["questoes"] if t and q.get("tipo") != t]
        ok = [q for q in d["questoes"] if not (t and q.get("tipo") != t)][:POR_CHAMADA]
        extra = {"descartadas_tipo": len(fora)} if fora else {}
        return {**d, "questoes": ok, **extra}

    def _gerar(self, c: str, u: dict, julgadas: list[dict] | None) -> bool:
        arq, nome = self._arq_ger(c, u), f"geracao_{c}_{u['item']}_{u['foco']:03d}_v{u['visita']}"
        if arq.exists():
            return True
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
                          **({"descartadas_tipo": d["descartadas_tipo"]} if d.get("descartadas_tipo") else {})})
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
