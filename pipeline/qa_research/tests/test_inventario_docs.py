"""Testes offline do piloto inventário x EC (clientes falsos, sem chamadas ao Azure)."""
import json
import re
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from pipeline.qa_research.inventario_docs import core


class Falso:
    """Um cliente por papel; responde de forma válida a partir do próprio prompt."""

    def __init__(self, papel):
        self.papel, self.chamadas, self.usuarios = papel, 0, []

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        self.chamadas += 1
        self.usuarios.append(user)
        d = getattr(self, self.papel)(user)
        if validate:
            validate(d)
        return d

    def relacoes(self, user):
        texto = re.search(r"<bloco>\n[^\n]*\n(.+?)\n</bloco>", user, re.S).group(1)
        pal = texto.split()
        rels = [{"afirmacao": f"Relação {k}.", "tipo": "mecanismo", "condicoes": ["c"], "limites": [],
                 "trecho": " ".join(pal[k * 6:k * 6 + 6]), "niveis": niv,
                 "explicacao_concorrente": "outra causa" if "dificil_A" in niv else "",
                 "condicao_que_distingue": "sinal x" if "dificil_A" in niv else ""}
                for k, niv in enumerate((["facil"], ["media"], ["media", "dificil_A"]))]
        return {"status": "ok", "motivo": "", "relacoes": rels}

    def combinacoes(self, user):
        ids = re.findall(r"^(B(\d{3})\.R\d+) \|", user, re.M)
        por_bloco = {}
        for i, b in ids:
            por_bloco.setdefault(b, i)
        uns = list(por_bloco.values())
        combos = [{"relacoes": [uns[k], uns[k + 1]], "titulo": "t", "ligacao": "l", "raciocinio": "r",
                   "cenario": "c", "resposta": "x", "criterios_correcao": [], "condicoes_enunciado": [],
                   "limites": []} for k in range(0, min(len(uns) - 1, 20), 2)]
        return {"combinacoes": combos[:15], "observacao": ""}

    def questao(self, user):
        tipo = json.loads(re.search(r"<alvo>\n(.+?)\n</alvo>", user, re.S).group(1))["tipo"]
        return {"status": "ok", "motivo": "", "pergunta": f"Pergunta {tipo} {self.chamadas}?", "resposta": "Resposta."}

    def respondente(self, user):
        return {"resposta": "Resposta." if self.chamadas % 2 else "Outra coisa."}

    def juiz(self, user):
        itens = json.loads(user)
        return {"avaliacoes": [{"id": i["id"], "veredito": "correta" if i["resposta_candidato"] == "Resposta."
                                else "incorreta", "referencia_valida": True, "justificativa": "j"} for i in itens]}


def clientes():
    return {p: Falso(p) for p in core.MODELOS}


class ValidacaoTests(unittest.TestCase):
    def test_trecho_precisa_ser_literal(self):
        rel = {"afirmacao": "a", "tipo": "mecanismo", "condicoes": [], "limites": [], "trecho": "texto inventado",
               "niveis": ["facil"], "explicacao_concorrente": "", "condicao_que_distingue": ""}
        with self.assertRaises(ValueError):
            core.validar_relacoes({"status": "ok", "motivo": "", "relacoes": [rel]}, "O bloco diz outra coisa.")
        core.validar_relacoes({"status": "ok", "motivo": "", "relacoes": [{**rel, "trecho": "diz outra"}]},
                              "O bloco diz outra coisa.")

    def test_dificil_a_exige_explicacao_concorrente(self):
        rel = {"afirmacao": "a", "tipo": "mecanismo", "condicoes": [], "limites": [], "trecho": "bloco",
               "niveis": ["dificil_A"], "explicacao_concorrente": "", "condicao_que_distingue": ""}
        with self.assertRaises(ValueError):
            core.validar_relacoes({"status": "ok", "motivo": "", "relacoes": [rel]}, "bloco")

    def test_combinacao_exige_blocos_diferentes(self):
        c = {"relacoes": ["B001.R1", "B001.R2"], "titulo": "t", "ligacao": "l", "raciocinio": "r", "cenario": "c",
             "resposta": "x", "criterios_correcao": [], "condicoes_enunciado": [], "limites": []}
        with self.assertRaises(ValueError):
            core.validar_combinacoes({"combinacoes": [c], "observacao": ""}, {"B001.R1": 1, "B001.R2": 1}, 5)

    def test_juiz_mesma_ordem(self):
        with self.assertRaises(ValueError):
            core.validar_juiz({"avaliacoes": [{"id": "Q2", "veredito": "correta", "referencia_valida": True}]}, ["Q1"])

    def test_cotas_somam_total(self):
        c = core.cotas(100, ["01_01", "02_02"])
        self.assertEqual(sum(v for d in c.values() for v in d.values()), 100)
        self.assertEqual(c["01_01"], {"facil": 13, "media": 25, "dificil_A": 6, "dificil_B": 6})


class FluxoTests(unittest.TestCase):
    def test_fluxo_completo_e_retomada(self):
        with tempfile.TemporaryDirectory() as tmp:
            ec = Path(tmp) / "ec.jsonl"
            linhas = [{"uid": f"{i}-{n}-{k}", "item": i, "dificuldade": n, "pergunta": f"EC {n} {k}?", "resposta": "Resposta."}
                      for i in core.ITENS for n in ("facil", "media", "dificil") for k in range(10)]
            ec.write_text("\n".join(json.dumps(l) for l in linhas), encoding="utf-8")
            saida = Path(tmp) / "out"
            cl = clientes()
            p = core.Piloto(saida, ec, total=16, limite_blocos=8, clientes=cl, workers=2, progress=lambda *a, **k: None)
            self.assertEqual(p.run(), 0)
            res = json.loads((saida / "resultado.json").read_text(encoding="utf-8"))
            self.assertEqual(res["metodos"]["inventario"]["total"]["n"], 16)
            self.assertEqual(res["metodos"]["ec"]["total"]["n"], 16)
            alvos = json.loads((saida / "alvos.json").read_text(encoding="utf-8"))["alvos"]
            self.assertEqual(Counter(a["tipo"] for a in alvos)["dificil_B"], 2)
            # alvos não repetem relação
            rels = [r["id"] for a in alvos if a["tipo"] != "dificil_B" for r in a["relacoes"]]
            self.assertEqual(len(rels), len(set((a["item"], r) for a in alvos if a["tipo"] != "dificil_B"
                                                for r in [x["id"] for x in a["relacoes"]])))
            # o juiz não vê método nem nível
            self.assertNotIn("inv:", cl["juiz"].usuarios[0])
            self.assertNotIn("ec:", cl["juiz"].usuarios[0])
            # o prompt da questão leva os exemplos EC
            self.assertIn("<questoes_ja_geradas>", cl["questao"].usuarios[0])
            self.assertTrue((saida / "RELATORIO.md").exists())
            antes = {k: c.chamadas for k, c in cl.items()}
            self.assertEqual(core.Piloto(saida, ec, total=16, limite_blocos=8, clientes=cl,
                                         progress=lambda *a, **k: None).run(), 0)
            self.assertEqual({k: c.chamadas for k, c in cl.items()}, antes)

    def test_config_diferente_recusa_pasta(self):
        with tempfile.TemporaryDirectory() as tmp:
            ec = Path(tmp) / "ec.jsonl"
            ec.write_text("", encoding="utf-8")
            core.Piloto(Path(tmp) / "o", ec, total=10, clientes=clientes()).config()
            with self.assertRaises(ValueError):
                core.Piloto(Path(tmp) / "o", ec, total=20, clientes=clientes()).config()


if __name__ == "__main__":
    unittest.main()
