"""Geração de conceitos: questões de nomeação de termo técnico (a pergunta descreve, a resposta é o nome).

Mesma infraestrutura da v23 (janela de 3 blocos, saturação, segunda chance, auditor por questão, deduplicação
calibrada), sem as compostas: um termo técnico vive num bloco, não num encadeamento. Mudam só o prompt do gerador
(foco_v23conceito), o do auditor (auditoria_v23conceito), os exemplos fixos (exemplos_conceito.json: 12 boas, 4
reservas e 8 ruins) e a régua, que aceita só o tipo conceito, enunciado de até 45 palavras (cenário curto
permitido) e gabarito de até 6 palavras.
"""
from __future__ import annotations

from pathlib import Path

from .v23 import GeracaoV23, regua_v23

EXEMPLOS_CONCEITO = Path(__file__).resolve().parent / "exemplos_conceito.json"
TETO_TERMO = 6
TETO_ENUNCIADO = 45     # o conceito da v23 é direto (até 35 palavras, sem cenário); aqui um cenário curto pode
                        # ajudar a identificar o termo sem entregá-lo


class GeracaoConceito(GeracaoV23):
    VERSAO = "v23conceito"
    TIPOS_FOCO = ("conceito",)
    COMPOSTAS = False

    def __init__(self, *a, exemplos: Path = EXEMPLOS_CONCEITO, **kw):
        super().__init__(*a, exemplos=exemplos, **kw)

    def prompt_nome(self, papel: str) -> str:
        return "composta_v23" if papel == "composta" else f"{papel}_{self.VERSAO}"   # composta não é usada

    def inventario(self) -> int:
        return 0      # sem compostas, o inventário de relações e encadeamentos não é necessário

    def regua(self, q, textos, tipos, rotulo_obrigatorio=None) -> list[str]:
        out = regua_v23(q, textos, tipos, rotulo_obrigatorio)
        if out[:1] and out[0].startswith("use exatamente os campos"):
            return out
        out = [m for m in out if not m.startswith("conceito é pergunta direta")]
        if len(q["pergunta"].split()) > TETO_ENUNCIADO:
            out.append(f"enunciado com mais de {TETO_ENUNCIADO} palavras")
        if isinstance(q.get("resposta"), str) and len(q["resposta"].split()) > TETO_TERMO:
            out.append(f"resposta com mais de {TETO_TERMO} palavras: deixe só o termo técnico")
        return out
