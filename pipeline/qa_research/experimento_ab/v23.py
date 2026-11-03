"""Gerador v23: o fluxo da v22 com exemplos fixos de questões boas e ruins como corpo do prompt.

Mudanças em relação à v22, ligadas à revisão manual do B_v22, do banco antigo e do dataset de múltipla escolha:
  1. exemplos fixos (exemplos_v23.json) no prompt de sistema: 10 boas, cada uma com a resposta padrão que um
     generalista daria e o conhecimento que a exclui, e 9 ruins, cada uma com o defeito. Exemplos do mesmo documento
     são trocados por reservas; no máximo 2 vêm de datasets externos ao pipeline (dataset de múltipla escolha);
  2. o gerador declara `resposta_padrao` e `por_que_nao`: se não há resposta atraente e errada, a questão é fácil;
  3. sem eliminação nem interpretação no enunciado: o sinal que separa a resposta certa exige conhecimento;
  4. decisão também nas janelas, e o prompt prioriza decisão e procedimento;
  5. auditor v23: alternativa equivalente ou caso particular da referência conta como excluída; eliminação e
     interpretação dada contam como atalho; "sem documento" julga o conhecimento do ofício, não o do modelo.
Régua, auditor por questão, deduplicação, saturação e segunda chance são os da v22.
"""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.qa_research.geracao_tipos.core import _texto
from pipeline.qa_research.piloto_janela.core import normalizar

from . import comum as C
from .v22 import CHAVES, GeracaoV22, regua

CHAVES_V23 = CHAVES + ("resposta_padrao", "por_que_nao")
TIPOS_FOCO_V23 = ("conceito", "mecanismo", "consequencia", "diagnostico", "decisao", "procedimento")
EXEMPLOS = Path(__file__).resolve().parent / "exemplos_v23.json"
MAX_EXTERNOS = 2


def carregar_exemplos(caminho: Path = EXEMPLOS) -> dict:
    d = json.loads(Path(caminho).read_text(encoding="utf-8"))
    if d.get("schema") != "exemplos-v23" or not d["boas"] or not d["ruins"]:
        raise ValueError(f"{caminho}: banco de exemplos inválido")
    return d


def selecionar_exemplos(banco: dict, item: str) -> tuple[list, list]:
    """Boas e ruins fixas; uma boa do mesmo documento dá lugar à primeira reserva do mesmo tipo (ou à primeira livre)."""
    boas = [e for e in banco["boas"] if e["item"] != item]
    usados = {e["id"] for e in boas}
    for falta in (e for e in banco["boas"] if e["item"] == item):
        livres = [r for r in banco["reservas"] if r["item"] != item and r["id"] not in usados]
        if livres:
            r = next((r for r in livres if r["tipo"] == falta["tipo"]), livres[0])
            boas.append(r)
            usados.add(r["id"])
    if sum(e.get("origem") == "dataset_mcq" for e in boas) > MAX_EXTERNOS:
        raise ValueError(f"Mais de {MAX_EXTERNOS} exemplos de datasets externos")
    return boas, [e for e in banco["ruins"] if e["item"] != item]


def bloco_exemplos(boas: list, ruins: list) -> str:
    b = "\n\n".join(f"[{e['tipo']}] Pergunta: {e['pergunta']}\nResposta: {e['resposta']}\n"
                    f"Resposta padrão (errada aqui): {e['resposta_padrao']}\nPor que não: {e['por_que_nao']}" for e in boas)
    r = "\n\n".join(f"[{e['tipo']}] Pergunta: {e['pergunta']}\nResposta: {e['resposta']}\nDefeito: {e['defeito']}"
                    for e in ruins)
    return f"<questoes_boas>\n{b}\n</questoes_boas>\n\n<questoes_ruins>\n{r}\n</questoes_ruins>"


def regua_v23(q, textos: dict, tipos: tuple, rotulo_obrigatorio: str | None = None) -> list[str]:
    out = regua(q, textos, tipos, rotulo_obrigatorio, CHAVES_V23)
    if out[:1] and out[0].startswith("use exatamente os campos"):
        return out
    out += [f"{c} vazio" for c in ("resposta_padrao", "por_que_nao") if not _texto(q[c])]
    if _texto(q["resposta_padrao"]) and normalizar(q["resposta_padrao"]) == normalizar(q["resposta"]):
        out.append("resposta_padrao igual à resposta: declare a resposta atraente que está errada nesta situação")
    return out


class GeracaoV23(GeracaoV22):
    VERSAO = "v23"
    CHAVES, TIPOS_FOCO = CHAVES_V23, TIPOS_FOCO_V23

    def __init__(self, *a, exemplos: Path = EXEMPLOS, **kw):
        super().__init__(*a, **kw)
        self.caminho_exemplos_v23 = Path(exemplos)
        self.banco_v23 = carregar_exemplos(self.caminho_exemplos_v23)

    def extra_config(self) -> dict:
        return {"exemplos_v23_sha256": C.sha(self.caminho_exemplos_v23.read_text(encoding="utf-8")),
                "max_externos": MAX_EXTERNOS}

    def regua(self, q, textos, tipos, rotulo_obrigatorio=None) -> list[str]:
        return regua_v23(q, textos, tipos, rotulo_obrigatorio)

    def sistema(self, papel: str, item: str) -> str:
        base = super().sistema(papel, item)
        if papel not in ("foco", "composta"):
            return base
        return base + "\n\n" + bloco_exemplos(*selecionar_exemplos(self.banco_v23, item))

    def _exemplos(self, item: str, semente: str, composta: bool) -> str:
        return ""   # os exemplos fixos estão no prompt de sistema
