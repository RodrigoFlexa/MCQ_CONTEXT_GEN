"""Geração por tipo: decisão, diagnóstico e procedimento, cada um numa geração separada.

É a geração variada (variada.py) restrita a um único tipo: sem boas fixas, só os defeitos da v23 no sistema;
visitas 1 a 3 com exemplos de forma de datasets externos e visita 4 com questões do dataset de múltipla escolha
convertido (de preferência do mesmo tipo); até 4 visitas por foco; régua, auditor v23 e deduplicação da v23.
O prompt (foco_v23tipo) é um modelo com a definição do tipo; cada tipo grava em relatorios/geracao_tipo_<tipo>.
"""
from __future__ import annotations

import hashlib

from .variada import GeracaoVariada

TIPOS = ("decisao", "diagnostico", "procedimento")

DEFINICOES = {
    "decisao": (
        "Dada uma situação, qual ação técnica específica tomar: intervenção, ajuste, arranjo, técnica, ponto de "
        "aplicação ou variável a controlar. A situação traz a condição que torna inadequada a ação que um generalista "
        "escolheria; a resposta é a solução mais adequada ao cenário, não apenas uma solução possível. Boas questões "
        "de decisão pesam alternativas com vantagens e limitações, priorizam ações ou integram operação, segurança, "
        "manutenção e integridade."),
    "diagnostico": (
        "Dados os sinais observados, qual a causa. O enunciado traz observações (medidas, tendências, condições que "
        "mudaram e que não mudaram), não a interpretação delas; a resposta é a causa primária, não um efeito "
        "secundário nem uma categoria de falha. Boas questões de diagnóstico têm mais de uma hipótese plausível, e "
        "um sinal do enunciado descarta a hipótese que o generalista daria."),
    "procedimento": (
        "Como executar, monitorar, testar ou verificar algo; a resposta é o método, a etapa, o ponto, a sequência ou "
        "o critério específico. Boas questões de procedimento pedem o passo ou a verificação que distingue a "
        "execução correta da habitual: o ponto certo de medição, a condição em que o teste vale, a etapa que não "
        "pode ser invertida, o critério de aceitação aplicável."),
}
CENARIO = {
    "decisao": "sempre true: a decisão depende da situação descrita.",
    "diagnostico": "sempre true: o diagnóstico parte dos sinais descritos.",
    "procedimento": "true quando o enunciado descreve uma situação (sinais, condições ou mudança); false na pergunta "
                    "direta sobre como executar, testar ou verificar.",
}


class GeracaoTipo(GeracaoVariada):
    VERSAO = "v23tipo"

    def __init__(self, *a, tipo: str, **kw):
        if tipo not in TIPOS:
            raise ValueError(f"tipo deve ser um de {TIPOS}")
        self.tipo = tipo
        self.TIPOS_FOCO = (tipo,)
        super().__init__(*a, **kw)

    def prompt_nome(self, papel: str) -> str:
        return {"foco": "foco_v23tipo", "auditoria": "auditoria_v23"}.get(papel, "composta_v23")

    def extra_config(self) -> dict:
        return {**super().extra_config(), "tipo": self.tipo,
                "definicao_sha256": hashlib.sha256(
                    (DEFINICOES[self.tipo] + CENARIO[self.tipo]).encode()).hexdigest()}

    def sistema(self, papel: str, item: str) -> str:
        s = super().sistema(papel, item)
        if papel != "foco":
            return s
        return (s.replace("<<TIPO>>", self.tipo).replace("<<DEFINICAO>>", DEFINICOES[self.tipo])
                .replace("<<CENARIO>>", CENARIO[self.tipo]))
