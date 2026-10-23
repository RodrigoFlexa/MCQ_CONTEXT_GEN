"""Testes offline da geração por meta (v16), com cliente falso."""
import json
import re
import tempfile
import unittest
from pathlib import Path

from pipeline.qa_research.geracao_tipos import rodadas
from pipeline.qa_research.tests.test_geracao_tipos import PERGUNTAS


class Falso:
    """Responde por tag; a auditoria reprova toda questão cujo id termina em 2 (atalho)."""

    def __init__(self):
        self.chamadas, self.usuarios, self.n = 0, [], 0
        self.tags = []

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        self.chamadas += 1
        self.usuarios.append(user)
        self.tags.append(tag)
        d = getattr(self, tag.replace("meta_", ""))(user)
        if validate:
            validate(d)
        return d

    def relacoes(self, user):
        texto = re.search(r"<bloco>\n[^\n]*\n(.+?)\n</bloco>", user, re.S).group(1)
        pal = texto.split()
        return {"status": "ok", "motivo": "", "relacoes": [
            {"afirmacao": f"Relação {k}.", "tipo": "mecanismo", "condicoes": [], "limites": [],
             "trecho": " ".join(pal[k * 6:k * 6 + 6]), "niveis": ["facil"], "explicacao_concorrente": "",
             "condicao_que_distingue": ""} for k in range(2)]}

    def combinacoes(self, user):
        ids = re.findall(r"^(B(\d{3})\.R\d+) \|", user, re.M)
        primeiros = list(dict.fromkeys(i for i, b in ids if i.endswith("R1")))
        return {"combinacoes": [{"relacoes": [primeiros[k], primeiros[k + 1]], "tipo": "encadeamento", "titulo": "t",
                                 "ponte": "p", "cadeia": "c", "cenario": "c", "resposta": "y", "resposta_atraente": "z",
                                 "sinal_que_descarta": "s", "condicoes_enunciado": [], "limites": []}
                                for k in range(0, min(6, len(primeiros) - 1), 2)], "observacao": ""}

    def composta(self, user):
        self.n += 1
        return {"status": "ok", "motivo": "", "tipo": "decisao", "cenario": True,
                "pergunta": f"Num FPSO, o residual some cedo no trecho {self.n}. Que ação técnica deve ser executada?",
                "resposta": f"Limpeza mecânica {self.n}."}

    def janela(self, user):
        texto_f = re.search(r"\[F\] [^\n]*\n(.+?)(?:\n\n\[A\d\]|\n</janela>)", user, re.S).group(1)
        trecho = " ".join(texto_f.split()[:8])
        qs = []
        for k, t in enumerate(("conceito", "mecanismo", "procedimento", "diagnostico"), 1):
            self.n += 1
            p, cen = PERGUNTAS[t]
            qs.append({"id": k, "tipo": t, "cenario": cen, "conhecimento": f"r{self.n}",
                       "pergunta": p.format(k=f"{self.n} alfa{self.n} beta{self.n} gama{self.n}"),
                       "resposta": f"Elemento {self.n} único.", "fundamentos": [{"bloco": "F", "trecho": trecho}]})
        return {"status": "ok", "motivo": "", "questoes": qs}

    def auditoria(self, user):
        itens = json.loads(user)
        return {"avaliacoes": [{"id": i["id"], "tipo_confere": True, "tipo_sugerido": i["tipo_declarado"],
                                "referencia_valida": True, "atalho": i["id"].endswith("2"),
                                "justificativa": "j"} for i in itens]}


class MetaTests(unittest.TestCase):
    def test_v16_barra_decisao_na_janela(self):
        f = Falso()
        d = f.janela("[F] t / s\ntexto do bloco foco com palavras suficientes aqui\n</janela>")
        d["questoes"][2]["tipo"] = "decisao"
        d["questoes"][2]["cenario"] = True
        with self.assertRaises(ValueError):
            rodadas.validar_janela_v16(d)

    def test_rodadas_ate_a_meta_banco_dinamico_e_retomada(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Falso()
            cl = {p: f for p in rodadas.MODELOS}
            g = rodadas.GeracaoMeta(Path(tmp) / "out", ["08_02"], meta=60, max_rodadas=3, reusar=None, clientes=cl,
                                    workers=4, progress=lambda *a, **k: None)
            self.assertEqual(g.run(), 0)
            res = json.loads((Path(tmp) / "out" / "resultado.json").read_text(encoding="utf-8"))
            t = res["topicos"]["08_02"]
            self.assertEqual(t["blocos"], 12)
            self.assertGreaterEqual(t["validas"], 60)       # 12 janelas x ~3 aprovadas não bastam; precisou de r2
            self.assertGreaterEqual(t["rodadas"], 2)
            self.assertGreater(res["banco_dinamico"]["reprovadas"], 0)
            # depois da primeira auditoria, os prompts trazem exemplos e contraexemplos dinâmicos
            janelas_r2 = [u for u, tag in zip(f.usuarios, f.tags) if tag == "meta_janela"][-1]
            self.assertIn("<contraexemplos>", janelas_r2)
            self.assertIn("Nenhuma.", [u for u, tag in zip(f.usuarios, f.tags) if tag == "meta_janela"][0])
            self.assertNotIn("Nenhuma.", janelas_r2)        # rodada 2 recebe as questões já geradas na janela
            self.assertTrue((Path(tmp) / "out" / "exemplos_proposto.json").exists())
            aprov = [json.loads(l) for l in (Path(tmp) / "out" / "aprovadas.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(aprov), t["validas"])
            antes = f.chamadas
            g2 = rodadas.GeracaoMeta(Path(tmp) / "out", ["08_02"], meta=60, max_rodadas=3, reusar=None, clientes=cl,
                                     workers=4, progress=lambda *a, **k: None)
            self.assertEqual(g2.run(), 0)
            self.assertEqual(f.chamadas, antes)


if __name__ == "__main__":
    unittest.main()
