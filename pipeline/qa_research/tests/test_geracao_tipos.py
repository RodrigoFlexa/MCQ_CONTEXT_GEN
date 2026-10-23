"""Testes offline da geração híbrida por tipo (clientes falsos, sem chamadas ao Azure)."""
import csv
import json
import re
import tempfile
import unittest
from pathlib import Path

from pipeline.qa_research import tipos
from pipeline.qa_research.geracao_tipos import core

PERGUNTAS = {
    "conceito": ("Qual é a função principal do componente {k}?", False),
    "mecanismo": ("Por que a mudança {k} leva ao efeito observado?", False),
    "consequencia": ("Se a vazão {k} aumentar, o que acontece com a perda de carga?", False),
    "diagnostico": ("Num separador, a espuma persiste com dose confirmada {k}. Que causa explica o quadro?", True),
    "decisao": ("Num FPSO, o residual some cedo no trecho {k}. Que ação deve ser priorizada?", True),
    "procedimento": ("Como se acompanha a evolução do tratamento {k} no poço?", False),
}


def questao(k, tipo, trecho):
    p, cen = PERGUNTAS[tipo]
    return {"id": k, "tipo": tipo, "cenario": cen, "conhecimento": f"r{k}", "pergunta": p.format(k=k),
            "resposta": "Elemento decisivo.", "fundamentos": [{"bloco": "F", "trecho": trecho}]}


class Falso:
    def __init__(self, papel, composicao=("conceito", "mecanismo", "decisao", "consequencia")):
        self.papel, self.composicao, self.chamadas, self.usuarios = papel, composicao, 0, []

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        self.chamadas += 1
        self.usuarios.append(user)
        d = getattr(self, tag.replace("tipos_", ""))(user)
        if validate:
            validate(d)
        return d

    def janela(self, user):
        texto_f = re.search(r"\[F\] [^\n]*\n(.+?)(?:\n\n\[A\d\]|\n</janela>)", user, re.S).group(1)
        trecho = " ".join(texto_f.split()[:8])
        return {"status": "ok", "motivo": "",
                "questoes": [questao(k, t, trecho) for k, t in enumerate(self.composicao, 1)]}

    def composta(self, user):
        return {"status": "ok", "motivo": "", "tipo": "diagnostico", "cenario": True,
                "pergunta": f"Num FPSO, após a troca {self.chamadas}, a espuma voltou. Que causa explica?",
                "resposta": "Surfactante no novo produto."}

    def auditoria(self, user):
        itens = json.loads(user)
        return {"avaliacoes": [{"id": i["id"], "tipo_confere": True, "tipo_sugerido": i["tipo_declarado"],
                                "referencia_valida": True, "atalho": False, "justificativa": "j"} for i in itens]}

    def reclassificar(self, user):
        itens = json.loads(user)
        return {"classificacoes": [{"id": i["id"], "tipo": "diagnostico" if "?" in i["pergunta"] else "conceito",
                                    "ambiguo": False, "cenario": True, "resposta_dado_especifico": False} for i in itens]}


class TiposTests(unittest.TestCase):
    def test_conceito_direto_e_sem_lista_aberta(self):
        self.assertFalse(tipos.problemas_tipo("conceito", False, "Qual é a função da URS?", "Reduzir sulfato."))
        self.assertTrue(tipos.problemas_tipo("conceito", True, "Qual é a função da URS?", "Reduzir sulfato."))
        self.assertTrue(tipos.problemas_tipo("conceito", False, "Que aspectos da formulação avaliar?", "x"))
        self.assertTrue(tipos.problemas_tipo("conceito", False, "Além da dose, que variável importa?", "x"))

    def test_diagnostico_exige_cenario_e_forma_aberta(self):
        self.assertTrue(tipos.problemas_tipo("diagnostico", False, "Que causa explica a espuma?", "x"))
        self.assertTrue(tipos.problemas_tipo("decisao", True, "Num FPSO, X ocorreu. A ação basta?", "Não."))
        self.assertTrue(tipos.problemas_tipo("inexistente", True, "Qual?", "x"))

    def test_regras_v15(self):
        self.assertTrue(tipos.problemas_tipo("conceito", False, "Com que tipo de referência um KPI compara resultados?", "x"))
        self.assertTrue(tipos.problemas_tipo("conceito", False, "Qual condição é citada como fator de complexidade?", "x"))
        self.assertTrue(tipos.problemas_tipo("decisao", True, "Dois sistemas param. Um é crítico e volta rápido; o outro "
                                             "é menos crítico. Qual deve receber prioridade?", "O crítico."))
        self.assertFalse(tipos.problemas_tipo("diagnostico", True, "No quadro descrito, com residual baixo, que causa "
                                              "explica a recontaminação?", "Biofilme."))

    def test_banco_de_exemplos(self):
        banco = core.carregar_banco()
        self.assertEqual({e["tipo"] for e in banco["exemplos"]}, set(tipos.TIPOS))
        txt = core.render_exemplos(banco, "02_02", "simples")
        self.assertEqual(txt.count("Por que é boa:"), 6)
        self.assertIn("Problema:", txt)
        compostas = core.render_exemplos(banco, "02_02", "composta")
        self.assertNotIn("conceito]", compostas.split("<contraexemplos>")[1])

    def test_caracteres_estranhos(self):
        self.assertEqual(tipos.caracteres_estranhos("MEG հետո regenerado"), ["ե", "հ", "ո", "տ"])
        self.assertEqual(tipos.caracteres_estranhos("H₂S, SO₄²⁻, ΔP ≥ 2 °C, 5 µm → queda"), [])

    def test_composicao(self):
        self.assertFalse(tipos.problemas_composicao("ok", ["conceito", "mecanismo", "decisao", "conceito"], ""))
        self.assertTrue(tipos.problemas_composicao("ok", ["conceito", "mecanismo", "decisao", "conceito"], "",
                                                   maximo=tipos.MAXIMO_V15))
        self.assertFalse(tipos.problemas_composicao("ok", ["conceito", "mecanismo", "decisao", "procedimento"], "",
                                                    maximo=tipos.MAXIMO_V15))
        self.assertTrue(tipos.problemas_composicao("ok", ["conceito", "mecanismo", "consequencia", "mecanismo"], ""))
        self.assertTrue(tipos.problemas_composicao("ok", ["conceito", "mecanismo", "decisao"], ""))
        self.assertFalse(tipos.problemas_composicao("parcial", ["conceito", "mecanismo"], "bloco de gestão"))


class ValidacaoTests(unittest.TestCase):
    def test_janela_rejeita_composicao_incompleta_como_ok(self):
        f = Falso("g", ("conceito", "mecanismo", "consequencia", "mecanismo"))
        d = f.janela("[F] t / s\nalgum texto do bloco foco aqui com palavras\n</janela>")
        with self.assertRaises(ValueError):
            core.validar_janela(d)

    def test_composta_nao_aceita_conceito(self):
        with self.assertRaises(ValueError):
            core.validar_composta({"status": "ok", "motivo": "", "tipo": "conceito", "cenario": False,
                                   "pergunta": "Qual é a função da URS?", "resposta": "Reduzir sulfato."})


class FluxoTests(unittest.TestCase):
    def _encadeamentos(self, raiz: Path):
        for item in core.ITENS:
            (raiz / "relacoes" / item).mkdir(parents=True)
            rels = [{"id": f"B00{b}.R1", "bloco": b, "afirmacao": "a", "condicoes": [], "limites": []} for b in (1, 2)]
            for r in rels:
                (raiz / "relacoes" / item / f"00{r['bloco']}.json").write_text(json.dumps({"relacoes": [r]}), encoding="utf-8")
            c = {"id": "C1", "relacoes": ["B001.R1", "B002.R1"], "tipo": "encadeamento", "titulo": "t", "ponte": "p",
                 "cadeia": "c", "cenario": "c", "resposta": "y", "resposta_atraente": "z", "sinal_que_descarta": "s",
                 "condicoes_enunciado": [], "limites": []}
            (raiz / "combinacoes").mkdir(exist_ok=True)
            (raiz / "combinacoes" / f"{item}.json").write_text(json.dumps({"combinacoes": [c, {**c, "id": "C2"}]}),
                                                               encoding="utf-8")
        with (raiz / "questoes_avaliadas.csv").open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["id", "nivel", "pergunta", "resposta", "veredito_R1", "veredito_R2",
                                              "referencia_valida"])
            w.writeheader()
            for k in range(12):
                w.writerow({"id": f"q{k}", "nivel": "facil", "pergunta": f"P{k}?", "resposta": "r",
                            "veredito_R1": "correta", "veredito_R2": "parcial", "referencia_valida": "True"})

    def test_fluxo_completo_e_retomada(self):
        with tempfile.TemporaryDirectory() as tmp:
            enc = Path(tmp) / "piloto"
            self._encadeamentos(enc)
            f = Falso("g")
            cl = {"geracao": f, "auditoria": f}
            g = core.Geracao(Path(tmp) / "out", ec_janelas=3, encadeamentos=enc, clientes=cl, workers=2,
                             progress=lambda *a, **k: None)
            self.assertEqual(g.run(("reclassificar", "janelas", "compostas", "auditoria", "relatorio"), piloto=enc), 0)
            res = json.loads((Path(tmp) / "out" / "resultado.json").read_text(encoding="utf-8"))
            self.assertEqual(res["janelas"]["total"], 6)
            self.assertEqual(res["por_origem"]["janela"]["n"], 24)
            self.assertEqual(res["por_origem"]["composta"]["n"], 4)
            self.assertEqual(res["por_origem"]["janela"]["auditadas"], 24)
            self.assertEqual(res["reclassificacao"]["por_tipo"]["diagnostico"]["n"], 12)
            prompts = [u for u in f.usuarios if "<janela>" in u]
            self.assertIn("<exemplos_por_tipo>", prompts[0])
            self.assertIn("<contraexemplos>", prompts[0])
            self.assertNotIn("<exemplos_de_forma>", prompts[0])
            self.assertEqual(res["aprovadas"]["total"], 28)
            self.assertTrue((Path(tmp) / "out" / "RELATORIO.md").exists())
            antes = f.chamadas
            g2 = core.Geracao(Path(tmp) / "out", ec_janelas=3, encadeamentos=enc, clientes=cl,
                              progress=lambda *a, **k: None)
            self.assertEqual(g2.run(("reclassificar", "janelas", "compostas", "auditoria", "relatorio"), piloto=enc), 0)
            self.assertEqual(f.chamadas, antes)


if __name__ == "__main__":
    unittest.main()
