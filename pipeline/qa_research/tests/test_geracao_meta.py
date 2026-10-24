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
        d = getattr(self, tag.replace("meta_", "").replace("reauditoria", "auditoria"))(user)
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
                "resposta": f"Limpeza{self.n} mecanica{self.n}."}

    def janela(self, user):
        texto_f = re.search(r"\[F\] [^\n]*\n(.+?)(?:\n\n\[A\d\]|\n</janela>)", user, re.S).group(1)
        trecho = " ".join(texto_f.split()[:8])
        qs = []
        for k, t in enumerate(("conceito", "mecanismo", "procedimento", "diagnostico"), 1):
            self.n += 1
            p, cen = PERGUNTAS[t]
            qs.append({"id": k, "tipo": t, "cenario": cen, "conhecimento": f"r{self.n}",
                       "pergunta": p.format(k=f"{self.n} alfa{self.n} beta{self.n} gama{self.n}"),
                       "resposta": f"Elemento{self.n} especifico{self.n}.", "fundamentos": [{"bloco": "F", "trecho": trecho}]})
        return {"status": "ok", "motivo": "", "questoes": qs}

    def auditoria(self, user):
        itens = json.loads(user)
        return {"avaliacoes": [{"id": i["id"], "tipo_confere": True, "tipo_sugerido": i["tipo_declarado"],
                                "referencia_valida": True, "atalho": i["id"].endswith("2"),
                                "motivo": "reformula_enunciado" if i["id"].endswith("2") else "nenhum",
                                "justificativa": "j"} for i in itens]}

    def refino(self, user):
        import re as _re
        tipo = _re.search(r"Tipo: (\w+)", user).group(1)
        self.n += 1
        p, cen = PERGUNTAS[tipo]
        return {"status": "ok", "motivo": "", "cenario": cen,
                "pergunta": p.format(k=f"{self.n} refinada{self.n} delta{self.n}"),
                "resposta": f"Refinada{self.n} especifica{self.n}."}


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
            g = rodadas.GeracaoMeta(Path(tmp) / "out", ["08_02"], meta=60, max_rodadas=3, reusar=None, banco_inicial=None, clientes=cl,
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
            g2 = rodadas.GeracaoMeta(Path(tmp) / "out", ["08_02"], meta=60, max_rodadas=3, reusar=None, banco_inicial=None, clientes=cl,
                                     workers=4, progress=lambda *a, **k: None)
            self.assertEqual(g2.run(), 0)
            self.assertEqual(f.chamadas, antes)


class OndasTests(unittest.TestCase):
    def test_sem_meta_uma_passagem_e_banco_aprende_entre_ondas(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Falso()
            cl = {p: f for p in rodadas.MODELOS}
            g = rodadas.GeracaoMeta(Path(tmp) / "out", ["08_02", "06_06"], reusar=None, banco_inicial=None, onda=1,
                                    clientes=cl, workers=2, progress=lambda *a, **k: None)
            self.assertEqual(g.run(), 0)
            res = json.loads((Path(tmp) / "out" / "resultado.json").read_text(encoding="utf-8"))
            self.assertEqual(res["topicos"]["08_02"]["passagens_janela"], 12)   # uma passagem por janela
            self.assertIsNone(res["topicos"]["08_02"]["atingiu_meta"])
            janelas = [u for u, tag in zip(f.usuarios, f.tags) if tag == "meta_janela"]
            self.assertNotIn("aprovada pelo auditor", janelas[0])               # 1ª onda: só o banco curado
            self.assertIn("aprovada pelo auditor", janelas[-1])                 # 2ª onda: aprendeu com a 1ª


class RefinadorTests(unittest.TestCase):
    def test_refinador_recupera_e_vira_como_corrigir(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Falso()
            cl = {p: f for p in rodadas.MODELOS}
            g = rodadas.GeracaoMeta(Path(tmp) / "out", ["08_02"], reusar=None, banco_inicial=None, clientes=cl,
                                    workers=2, progress=lambda *a, **k: None)
            self.assertEqual(g.run(), 0)
            res = json.loads((Path(tmp) / "out" / "resultado.json").read_text(encoding="utf-8"))
            self.assertGreater(res["refinador"]["tentadas"], 0)
            self.assertGreater(res["refinador"]["aprovadas_apos_refino"], 0)
            banco = json.loads((Path(tmp) / "out" / "banco_dinamico.json").read_text(encoding="utf-8"))
            self.assertTrue(any(c.get("como_corrigir") for c in banco["reprovadas"]))
            # refinadas não são refinadas de novo
            self.assertEqual(f.tags.count("meta_refino"), res["refinador"]["tentadas"])

    def test_auditoria_exige_motivo_coerente(self):
        with self.assertRaises(ValueError):
            rodadas.validar_auditoria({"avaliacoes": [{"id": "Q1", "tipo_confere": True, "tipo_sugerido": "conceito",
                                                       "motivo": "nenhum", "referencia_valida": False, "atalho": False}]},
                                      ["Q1"])


class ReauditoriaTests(unittest.TestCase):
    def test_reauditar_aprovadas_e_removidas(self):
        with tempfile.TemporaryDirectory() as tmp:
            orig = Path(tmp) / "orig"
            orig.mkdir()
            qs = [{"uid": f"x:{k}", "item": "01_01", "tipo": "conceito", "pergunta": f"Qual termo {k}?", "resposta": "r"}
                  for k in range(1, 13)]
            (orig / "aprovadas.jsonl").write_text("\n".join(json.dumps(q) for q in qs[:10]), encoding="utf-8")
            (orig / "remocoes_manuais.json").write_text(json.dumps({"removidas": [{**q, "motivo": "m"} for q in qs[10:]]}),
                                                         encoding="utf-8")
            res = rodadas.reauditar(orig, Path(tmp) / "re", cliente=Falso(), workers=2, progress=lambda *a, **k: None)
            self.assertEqual(res["aprovadas_antes"], 10)
            self.assertEqual(res["removidas_manualmente"], 2)
            self.assertTrue((Path(tmp) / "re" / "REAUDITORIA.md").exists())


class AjustesV17Tests(unittest.TestCase):
    def test_resposta_curta_igual_conta_como_duplicata(self):
        a = rodadas._resposta_curta("A matriz de causa e efeito.")
        b = rodadas._resposta_curta("Matriz de causa e efeito")
        self.assertTrue(a and len(a & b) / len(a | b) >= rodadas.LIMIAR_RESPOSTA_CURTA)
        self.assertFalse(rodadas._resposta_curta("Porque a menor perda de carga reduz o campo centrífugo e piora a "
                                                 "separação das gotas de óleo"))

    def test_filtro_de_conteudo_vira_insuficiente(self):
        class ContentFiltered(Exception):
            pass

        class Bloqueia(Falso):
            def composta(self, user):
                raise ContentFiltered("filtrado")

        with tempfile.TemporaryDirectory() as tmp:
            f = Bloqueia()
            cl = {p: f for p in rodadas.MODELOS}
            g = rodadas.GeracaoMeta(Path(tmp) / "out", ["08_02"], meta=5, max_rodadas=1, reusar=None,
                                    banco_inicial=None, clientes=cl, workers=2, progress=lambda *a, **k: None)
            self.assertEqual(g.run(), 0)
            comp = list((Path(tmp) / "out" / "topicos" / "08_02" / "compostas").glob("*.json"))
            self.assertTrue(comp)
            self.assertTrue(all(json.loads(p.read_text(encoding="utf-8"))["status"] == "insuficiente" for p in comp))

    def test_citado_como(self):
        from pipeline.qa_research import tipos
        self.assertTrue(tipos.problemas_tipo("conceito", False, "Em que equipamento ocorre o fechamento citado como "
                                             "antecedente da segregação?", "ANM."))


if __name__ == "__main__":
    unittest.main()
