"""Testes offline do piloto de dificuldade v2 (clientes falsos, sem chamadas ao Azure)."""
import json
import re
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from pipeline.qa_research import dificuldade as dif
from pipeline.qa_research.inventario_docs import core

DESENHO_VAZIO = {"passo_oculto": "", "resposta_atraente": "", "sinal_que_descarta": ""}
DESENHO = {"passo_oculto": "estado X", "resposta_atraente": "causa comum", "sinal_que_descarta": "sinal Y"}


class Falso:
    """Um cliente por papel; responde de forma válida a partir do próprio prompt."""

    def __init__(self, papel, insuficientes=0):
        self.papel, self.chamadas, self.usuarios, self.insuficientes = papel, 0, [], insuficientes

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        self.chamadas += 1
        self.usuarios.append(user)
        d = getattr(self, self.papel if not self.papel.startswith("R") else "respondente")(user)
        if validate:
            validate(d)
        return d

    def relacoes(self, user):
        texto = re.search(r"<bloco>\n[^\n]*\n(.+?)\n</bloco>", user, re.S).group(1)
        pal = texto.split()
        rels = [{"afirmacao": f"Relação {k}.", "tipo": tipo, "condicoes": ["c"], "limites": [],
                 "trecho": " ".join(pal[k * 6:k * 6 + 6]), "niveis": niv,
                 "explicacao_concorrente": "outra causa" if "dificil_A" in niv else "",
                 "condicao_que_distingue": "sinal x" if "dificil_A" in niv else ""}
                for k, (niv, tipo) in enumerate(((["facil"], "definicao"), (["media"], "criterio"),
                                                 (["media", "dificil_A"], "mecanismo")))]
        return {"status": "ok", "motivo": "", "relacoes": rels}

    def combinacoes(self, user):
        ids = re.findall(r"^(B(\d{3})\.R\d+) \|", user, re.M)
        por_bloco = {}
        for i, b in ids:
            por_bloco.setdefault(b, i)
        uns = list(por_bloco.values())
        combos = [{"relacoes": [uns[k], uns[k + 1]], "tipo": "encadeamento", "titulo": "t", "ponte": "p",
                   "cadeia": "a leva a p, p leva a y", "cenario": "c", "resposta": "y", "resposta_atraente": "z",
                   "sinal_que_descarta": "s", "condicoes_enunciado": [], "limites": []}
                  for k in range(0, len(uns) - 1, 2)]
        return {"combinacoes": combos[:25], "observacao": ""}

    def questao(self, user):
        tipo = json.loads(re.search(r"<alvo>\n(.+?)\n</alvo>", user, re.S).group(1))["tipo"]
        if self.insuficientes and self.chamadas <= self.insuficientes:
            return {"status": "insuficiente", "motivo": "sem sinal", "pergunta": "", "resposta": "",
                    "desenho": DESENHO_VAZIO}
        return {"status": "ok", "motivo": "", "pergunta": f"Qual mecanismo {tipo} {self.chamadas}?",
                "resposta": "Resposta.", "desenho": DESENHO if tipo.startswith("dificil") else DESENHO_VAZIO}

    def ec(self, user):
        texto_f = re.search(r"\[F\] [^\n]*\n(.+?)(?:\n\n\[A\d\]|\n</janela>)", user, re.S).group(1)
        trecho = " ".join(texto_f.split()[:8])
        qs = [{"id": k, "dificuldade": d, "tipo_demanda": "inferir", "conhecimento": f"r{k}",
               "pergunta": f"Qual efeito {k}?", "resposta": "Resposta.",
               "fundamentos": [{"bloco": "F", "trecho": trecho}],
               "desenho": DESENHO if d == "dificil" else DESENHO_VAZIO}
              for k, d in enumerate(("facil", "media", "media", "dificil"), 1)]
        return {"status": "ok", "motivo": "", "questoes": qs}

    def respondente(self, user):
        return {"resposta": "Resposta." if self.chamadas % 2 else "Outra coisa."}

    def juiz(self, user):
        itens = json.loads(user)
        return {"avaliacoes": [{"id": i["id"], "vereditos": {c: "correta" if r == "Resposta." else "incorreta"
                                                             for c, r in i["respostas_candidatos"].items()},
                                "referencia_valida": True, "atalho_generico": False, "justificativa": "j"}
                               for i in itens]}


def clientes(**kw):
    out = {p: Falso(p) for p in ("relacoes", "combinacoes", "juiz", "ec", "R1", "R2")}
    out["questao"] = Falso("questao", **kw)
    return out


class FormaTests(unittest.TestCase):
    def test_sim_nao_e_escolha_binaria(self):
        self.assertTrue(dif.problemas_forma("Esse KPI, visto sozinho, é adequado para a decisão?", "x"))
        self.assertTrue(dif.problemas_forma("Entre manter o programa e revê-lo, qual decisão é correta?", "x"))
        self.assertTrue(dif.problemas_forma("Qual é a conclusão técnica correta sobre essa decisão?", "x"))
        self.assertTrue(dif.problemas_forma("Que mecanismo explica a queda?", "Não. Considere o contexto."))
        self.assertFalse(dif.problemas_forma("Após a troca, que mecanismo explica a persistência da espuma?",
                                             "Estabilização do filme por surfactantes."))
        self.assertFalse(dif.problemas_forma("Na decisão entre intervir agora ou adiar, qual aspecto deve orientar "
                                             "a escolha?", "O tempo para restaurar a função."))

    def test_resposta_longa_e_desenho(self):
        self.assertTrue(dif.problemas_forma("Qual causa?", " ".join(["p"] * 31)))
        self.assertTrue(dif.problemas_desenho(DESENHO_VAZIO, "dificil_A", "x"))
        self.assertFalse(dif.problemas_desenho(DESENHO_VAZIO, "facil", "x"))
        self.assertTrue(dif.problemas_desenho({**DESENHO, "resposta_atraente": "Resposta"}, "dificil", "Resposta."))


class ValidacaoTests(unittest.TestCase):
    def test_trecho_precisa_ser_literal(self):
        rel = {"afirmacao": "a", "tipo": "mecanismo", "condicoes": [], "limites": [], "trecho": "texto inventado",
               "niveis": ["facil"], "explicacao_concorrente": "", "condicao_que_distingue": ""}
        with self.assertRaises(ValueError):
            core.validar_relacoes({"status": "ok", "motivo": "", "relacoes": [rel]}, "O bloco diz outra coisa.")
        core.validar_relacoes({"status": "ok", "motivo": "", "relacoes": [{**rel, "trecho": "diz outra"}]},
                              "O bloco diz outra coisa.")

    def test_encadeamento_exige_ponte_e_blocos_diferentes(self):
        c = {"relacoes": ["B001.R1", "B002.R2"], "tipo": "encadeamento", "titulo": "t", "ponte": "", "cadeia": "c",
             "cenario": "c", "resposta": "x", "resposta_atraente": "z", "sinal_que_descarta": "s",
             "condicoes_enunciado": [], "limites": []}
        with self.assertRaises(ValueError):
            core.validar_combinacoes({"combinacoes": [c], "observacao": ""}, {"B001.R1": 1, "B002.R2": 2}, 5)
        with self.assertRaises(ValueError):
            core.validar_combinacoes({"combinacoes": [{**c, "ponte": "p"}], "observacao": ""},
                                     {"B001.R1": 1, "B002.R2": 1}, 5)

    def test_questao_rejeita_sim_nao(self):
        with self.assertRaises(ValueError):
            core.validar_questao({"status": "ok", "motivo": "", "pergunta": "O empate basta?", "resposta": "Não.",
                                  "desenho": DESENHO}, "dificil_B")

    def test_juiz_vereditos_por_candidato(self):
        with self.assertRaises(ValueError):
            core.validar_juiz({"avaliacoes": [{"id": "Q1", "vereditos": {"R1": "correta"}, "referencia_valida": True,
                                               "atalho_generico": False}]}, ["Q1"], ["R1", "R2"])

    def test_cotas_acompanham_janelas_ec(self):
        self.assertEqual(core.cotas_item(24, 10, 10, None, 36), {"facil": 10, "media": 10, "dificil_A": 12, "dificil_B": 12})
        self.assertEqual(core.cotas_item(57, 10, 10, None, 36)["dificil_A"], 18)


class FluxoTests(unittest.TestCase):
    def piloto(self, saida, cl, **kw):
        return core.Piloto(saida, faceis=2, medias=2, dificeis=4, ec_janelas=3, limite_blocos=10, clientes=cl,
                           workers=2, progress=lambda *a, **k: None, **kw)

    def test_fluxo_completo_reservas_e_retomada(self):
        with tempfile.TemporaryDirectory() as tmp:
            saida = Path(tmp) / "out"
            cl = clientes(insuficientes=3)
            self.assertEqual(self.piloto(saida, cl).run(), 0)
            res = json.loads((saida / "resultado.json").read_text(encoding="utf-8"))
            inv, ec = res["metodos"]["inventario"], res["metodos"]["ec"]
            self.assertEqual(inv["total"]["n"], 16)                  # 2 docs x (2 + 2 + 2 A + 2 B)
            self.assertEqual(res["inventario_geracao"]["insuficiente"], 3)
            self.assertEqual(res["inventario_geracao"]["faltas_finais"], {})   # reservas cobriram
            self.assertEqual(ec["por_nivel"]["dificil"]["n"], 6)      # 3 janelas por doc, 1 difícil cada
            self.assertIn("filtro", inv["total"])
            self.assertNotIn("inv:", cl["juiz"].usuarios[0])
            self.assertIn("<questoes_ja_geradas>", cl["questao"].usuarios[0])
            self.assertTrue((saida / "RELATORIO.md").exists())
            antes = {k: c.chamadas for k, c in cl.items()}
            self.assertEqual(self.piloto(saida, cl).run(), 0)
            self.assertEqual({k: c.chamadas for k, c in cl.items()}, antes)

    def test_reaproveita_relacoes(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a", Path(tmp) / "b"
            cl = clientes()
            self.piloto(a, cl).run(("relacoes",))
            n = cl["relacoes"].chamadas
            self.piloto(b, cl, reusar=a).run(("relacoes",))
            self.assertEqual(cl["relacoes"].chamadas, n)
            self.assertEqual(len(list((b / "relacoes" / "01_01").glob("*.json"))), 10)

    def test_config_diferente_recusa_pasta(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.piloto(Path(tmp) / "o", clientes()).config()
            with self.assertRaises(ValueError):
                core.Piloto(Path(tmp) / "o", faceis=3, clientes=clientes()).config()


if __name__ == "__main__":
    unittest.main()
