"""Testes offline do piloto de geração por janela (cliente falso, sem chamadas ao Azure)."""
import json
import re
import tempfile
import unittest
from pathlib import Path

from pipeline.qa_research.piloto_janela import core, exemplos as ex


class ClienteFalso:
    """Devolve n questões ancoradas no início do bloco [F] recebido."""

    def __init__(self, n=6):
        self.n, self.chamadas, self.usuarios = n, 0, []

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        self.chamadas += 1
        self.usuarios.append(user)
        texto_f = re.search(r"\[F\] [^\n]*\n(.+?)(?:\n\n\[A\d\]|\n</janela>)", user, re.S).group(1)
        trecho = " ".join(texto_f.split()[:8])
        qs = [{"id": k, "dificuldade": core.DIFICULDADES[k % 3], "tipo_demanda": "recordar",
               "conhecimento": f"relação {k}", "pergunta": f"Pergunta {k} sobre {trecho}?",
               "resposta": f"Resposta {k}.", "fundamentos": [{"bloco": "F", "trecho": trecho}]}
              for k in range(1, self.n + 1)]
        data = {"status": "ok" if self.n >= 6 else ("parcial" if self.n else "sem_questoes"),
                "motivo": "" if self.n >= 6 else "foco curto", "questoes": qs}
        if validate:
            validate(data)
        return data


class JanelaTests(unittest.TestCase):
    def setUp(self):
        _, self.bs = core.blocos("01_01")

    def test_rotulos_nas_pontas_e_no_meio(self):
        self.assertEqual([r for r, _ in core.janela(self.bs, 0)], ["F", "A1", "A2"])
        self.assertEqual([r for r, _ in core.janela(self.bs, 5)], ["A1", "F", "A2"])
        ultimo = len(self.bs) - 1
        self.assertEqual([r for r, _ in core.janela(self.bs, ultimo)], ["A1", "A2", "F"])
        indices = [b["indice"] for _, b in core.janela(self.bs, 5)]
        self.assertEqual(indices, [4, 5, 6])

    def test_prompt_sem_marcadores_pendentes(self):
        system, usuario, _ = core.carregar_prompt(6, 8)
        self.assertNotIn("{{", system)
        self.assertIn("de 6 a 8 questões", system)
        self.assertIn("de 1 a 5", system)
        texto = core.preencher(usuario, core.tema("01_01"), core.SEM_PREFERENCIA, "Nenhuma.",
                               core.janela(self.bs, 3))
        self.assertNotIn("{{", texto)
        self.assertIn("[F]", texto)


class ValidacaoTests(unittest.TestCase):
    def base(self, n, status):
        q = {"id": 1, "dificuldade": "facil", "tipo_demanda": "recordar", "conhecimento": "c",
             "pergunta": "p", "resposta": "r", "fundamentos": [{"bloco": "F", "trecho": "t"}]}
        return {"status": status, "motivo": "" if status == "ok" else "m",
                "questoes": [{**q, "id": k} for k in range(1, n + 1)]}

    def test_quantidades(self):
        core.validar(self.base(6, "ok"), 6, 8)
        core.validar(self.base(3, "parcial"), 6, 8)
        core.validar(self.base(0, "sem_questoes"), 6, 8)
        for data in (self.base(5, "ok"), self.base(9, "ok"), self.base(0, "parcial"), self.base(6, "parcial")):
            with self.assertRaises(ValueError):
                core.validar(data, 6, 8)

    def test_formato(self):
        d = self.base(6, "ok")
        d["questoes"][2]["fundamentos"] = [{"bloco": "B", "trecho": "x"}]
        with self.assertRaises(ValueError):
            core.validar(d, 6, 8)
        d = self.base(6, "ok")
        d["questoes"][0]["id"] = 7
        with self.assertRaises(ValueError):
            core.validar(d, 6, 8)
        d = self.base(2, "parcial")
        d["motivo"] = " "
        with self.assertRaises(ValueError):
            core.validar(d, 6, 8)


class ExecucaoTests(unittest.TestCase):
    def test_gera_retoma_e_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            saida = Path(tmp) / "run"
            cli = ClienteFalso()
            core.Piloto(saida, ["01_01"], "falso:low", limite=3, client=cli, progress=lambda *a, **k: None).run()
            self.assertEqual(cli.chamadas, 3)
            resumo = json.loads((saida / "resumo.json").read_text(encoding="utf-8"))
            self.assertEqual(resumo["total"]["janelas"], 3)
            self.assertEqual(resumo["total"]["questoes"], 18)
            self.assertEqual(resumo["total"]["ancora_em_F_pct"], 100.0)
            self.assertEqual(resumo["total"]["status"]["ok"], 3)
            self.assertTrue((saida / "QUESTOES.md").exists() and (saida / "questoes.csv").exists())

            core.Piloto(saida, ["01_01"], "falso:low", limite=3, client=cli, progress=lambda *a, **k: None).run()
            self.assertEqual(cli.chamadas, 3, "janelas concluídas não devem ser regeradas")

            with self.assertRaises(ValueError):
                core.Piloto(saida, ["01_01"], "falso:low", minimo=4, limite=3, client=cli,
                            progress=lambda *a, **k: None).run()

            cli2 = ClienteFalso()
            core.Piloto(Path(tmp) / "rodada2", ["01_01"], "falso:low", limite=1, anteriores=saida, client=cli2,
                        progress=lambda *a, **k: None).run()
            self.assertIn("- relação 1 | Resposta: Resposta 1.", cli2.usuarios[0])

    def test_parcial_e_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            saida = Path(tmp) / "run"
            core.Piloto(saida, ["02_02"], "falso:low", limite=2, client=ClienteFalso(3),
                        progress=lambda *a, **k: None).run()
            resumo = json.loads((saida / "resumo.json").read_text(encoding="utf-8"))
            self.assertEqual(resumo["total"]["status"]["parcial"], 2)
            seco = Path(tmp) / "seco"
            core.Piloto(seco, ["01_01"], "falso:low", limite=2, dry_run=True, progress=lambda *a, **k: None).run()
            self.assertEqual(len(list((seco / "prompts_dry_run" / "01_01").glob("*.txt"))), 2)


def externos_falsos(pasta: Path) -> Path:
    caminho = pasta / "qa_examples.jsonl"
    linhas = []
    for fonte, lingua in (("pira_ptbr", "pt"), ("arc_challenge", "en"), ("hotpotqa", "en")):
        for k in range(5):
            linhas.append({"id": f"{fonte}:{k}", "question": f"Pergunta externa {fonte} numero {k} sobre ciencia?",
                           "answer": f"Resposta {k}", "source_license": "x", "source_language": lingua})
    linhas.append({"id": "hotpotqa:sim", "question": "Are both of them from the same country?", "answer": "yes"})
    linhas.append({"id": "squad_v2:1", "question": "What is outside the selection pool?", "answer": "x"})
    caminho.write_text("\n".join(json.dumps(l) for l in linhas), encoding="utf-8")
    return caminho


class ExemplosTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.pool = ex.carregar_externos(externos_falsos(Path(self.tmp.name)))
        self.banco = ex.carregar_especialista()

    def tearDown(self):
        self.tmp.cleanup()

    def test_pool_externo_filtra(self):
        self.assertEqual(set(self.pool), {"pira_ptbr", "arc_challenge", "hotpotqa"})
        self.assertNotIn("hotpotqa:sim", [r["id"] for r in self.pool["hotpotqa"]])

    def test_condicoes(self):
        for item, foco in (("01_01", 0), ("02_02", 10), ("02_02", 56)):
            a = ex.exemplos_da_janela("A", item, foco, self.pool, self.banco)
            b = ex.exemplos_da_janela("B", item, foco, self.pool, self.banco)
            c = ex.exemplos_da_janela("C", item, foco, self.pool, self.banco)
            d = ex.exemplos_da_janela("D", item, foco, self.pool, self.banco)
            self.assertEqual(a, [])
            self.assertEqual(sorted(e["dificuldade"] for e in b), ["dificil", "facil", "media"])
            self.assertEqual(len({e["fonte"] for e in b}), 3)
            self.assertEqual(sorted(e["dificuldade"] for e in c), ["dificil", "facil", "media"])
            areas = [e["area_id"] for e in c]
            self.assertEqual(len(set(areas)), 3, "áreas distintas entre si")
            self.assertNotIn(item[:2], areas, "nenhum exemplo da área da janela")
            self.assertEqual(sorted(e["id"] for e in d), sorted(e["id"] for e in b + c), "D = B + C")
            self.assertEqual(c, ex.exemplos_da_janela("C", item, foco, self.pool, self.banco), "determinístico")

    def test_render_sem_dificuldade(self):
        txt = ex.render(ex.exemplos_da_janela("D", "01_01", 3, self.pool, self.banco))
        self.assertTrue(txt.startswith("<exemplos_de_forma>") and txt.endswith("</exemplos_de_forma>"))
        self.assertEqual(txt.count("Pergunta:"), 6)
        self.assertNotIn("dificuldade", txt.lower())
        self.assertNotRegex(txt, r"\b(facil|dificil)\b")

    def test_experimento_mesmas_janelas(self):
        raiz = Path(self.tmp.name) / "exp"
        externos = Path(self.tmp.name) / "qa_examples.jsonl"
        clientes = {}
        for cond in ex.CONDICOES:
            clientes[cond] = ClienteFalso()
            core.Piloto(raiz / cond, ["01_01", "02_02"], "falso:low", janelas_por_item=4, condicao=cond,
                        externos=externos, client=clientes[cond], progress=lambda *a, **k: None).run()
        res = core.comparar(raiz)
        self.assertEqual(set(res), set(ex.CONDICOES))
        focos = {c: sorted((j["item"], j["foco"]) for j in
                           (json.loads(p.read_text(encoding="utf-8")) for p in (raiz / c).glob("*/janelas/*.json")))
                 for c in ex.CONDICOES}
        self.assertTrue(all(f == focos["A"] for f in focos.values()))
        self.assertEqual(len(focos["A"]), 8)
        self.assertNotIn("<exemplos_de_forma>", clientes["A"].usuarios[0])
        self.assertIn("<exemplos_de_forma>", clientes["D"].usuarios[0])
        self.assertTrue((raiz / "COMPARACAO.md").exists())
        self.assertEqual(core.selecionar_focos(24, 20)[0], 0)
        self.assertEqual(core.selecionar_focos(24, 20)[-1], 23)
        self.assertEqual(len(core.selecionar_focos(57, 20)), 20)


if __name__ == "__main__":
    unittest.main()
