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


class ClienteModos(ClienteFalso):
    """Responde às três etapas: junto, planejamento e redação."""

    def __init__(self, n=4, dificeis=1, descartar=0, medias=1):
        super().__init__(n)
        self.dificeis, self.medias, self.descartar, self.tags = dificeis, medias, descartar, []

    def _trecho(self, user):
        texto_f = re.search(r"\[F\] [^\n]*\n(.+?)(?:\n\n\[A\d\]|\n</janela>)", user, re.S).group(1)
        return " ".join(texto_f.split()[:8])

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        self.chamadas += 1
        self.tags.append(tag)
        self.usuarios.append(user)
        trecho = self._trecho(user)
        difs = ["dificil"] * self.dificeis + ["media"] * self.medias + ["facil"] * (self.n - self.dificeis - self.medias)
        if tag == "piloto_redacao":
            plano = json.loads(re.search(r"<plano>\n(.+?)\n</plano>", user, re.S).group(1))
            manter = plano[: len(plano) - self.descartar]
            data = {"status": "ok" if len(manter) == len(plano) else ("parcial" if manter else "sem_questoes"),
                    "motivo": "" if len(manter) == len(plano) else "item sem pergunta válida",
                    "questoes": [{"id": it["id"], "pergunta": f"P {it['id']} {trecho}?", "resposta": "R."}
                                 for it in manter]}
        elif tag == "piloto_planejamento":
            data = {"status": "ok", "motivo": "", "itens": [
                {"id": k, "dificuldade": difs[k - 1], "tipo_demanda": "diagnosticar", "alvo": f"alvo {k}",
                 "resposta_esperada": "R.", "condicoes_necessarias": [], "exigencia_cognitiva": "x",
                 "fundamentos": [{"bloco": "F", "trecho": trecho}]} for k in range(1, self.n + 1)]}
        else:
            data = {"status": "ok", "motivo": "", "questoes": [
                {"id": k, "dificuldade": difs[k - 1], "tipo_demanda": "recordar", "conhecimento": f"c {k}",
                 "pergunta": f"P {k} {trecho}?", "resposta": "R.", "fundamentos": [{"bloco": "F", "trecho": trecho}]}
                for k in range(1, self.n + 1)]}
        if validate:
            validate(data)
        return data


class ModosTests(unittest.TestCase):
    def q(self, k, dif):
        return {"id": k, "dificuldade": dif, "tipo_demanda": "recordar", "conhecimento": "c", "pergunta": "p",
                "resposta": "r", "fundamentos": [{"bloco": "F", "trecho": "t"}]}

    def test_exige_dificil(self):
        sem = {"status": "ok", "motivo": "", "questoes": [self.q(k, "facil") for k in range(1, 5)]}
        with self.assertRaises(ValueError):
            core.validar(sem, 4, 4, 1)
        core.validar({**sem, "status": "parcial", "motivo": "foco sem mecanismo"}, 4, 4, 1)
        com = {"status": "ok", "motivo": "", "questoes": [self.q(1, "dificil")] + [self.q(k, "facil") for k in range(2, 5)]}
        core.validar(com, 4, 4, 1)
        with self.assertRaises(ValueError):
            core.validar({**com, "status": "parcial", "motivo": "x"}, 4, 4, 1)
        with self.assertRaises(ValueError):
            core.validar(com, 4, 4, 1, 1)   # falta a média
        com_media = {**com, "questoes": com["questoes"][:3] + [self.q(4, "media")]}
        core.validar(com_media, 4, 4, 1, 1)

    def test_validar_redacao(self):
        core.validar_redacao({"status": "ok", "motivo": "", "questoes": [
            {"id": 1, "pergunta": "p", "resposta": "r"}, {"id": 2, "pergunta": "p", "resposta": "r"}]}, [1, 2])
        for ruim in ({"status": "ok", "motivo": "", "questoes": [{"id": 1, "pergunta": "p", "resposta": "r"}]},
                     {"status": "parcial", "motivo": "x", "questoes": [{"id": 4, "pergunta": "p", "resposta": "r"}]},
                     {"status": "parcial", "motivo": "x", "questoes": [{"id": 2, "pergunta": "p", "resposta": "r"},
                                                                       {"id": 1, "pergunta": "p", "resposta": "r"}]}):
            with self.assertRaises(ValueError):
                core.validar_redacao(ruim, [1, 2, 3])

    def test_prompts_v11(self):
        for caminho in (core.PROMPT_JUNTO, core.PROMPT_PLANO, core.PROMPT_REDACAO):
            system, usuario, _ = core.carregar_prompt(4, 4, caminho, 1)
            self.assertNotIn("{{", system)
        system, _, _ = core.carregar_prompt(4, 4, core.PROMPT_JUNTO, 1)
        self.assertIn("elabore 4 questões", system)
        self.assertIn("pelo menos uma difícil", system)
        system, _, _ = core.carregar_prompt(4, 4, core.PROMPT_JUNTO, 1, 1)
        self.assertIn("sendo pelo menos uma média e uma difícil", system)
        plano, _, _ = core.carregar_prompt(4, 4, core.PROMPT_PLANO, 1, 1)
        self.assertIn("sendo pelo menos um médio e um difícil", plano)
        with self.assertRaises(ValueError):
            core.carregar_prompt(4, 4, core.PROMPT_JUNTO, 0)

    def test_experimento_modos(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            junto, sep = ClienteModos(), ClienteModos(descartar=1)
            comum = dict(minimo=4, maximo=4, min_dificeis=1, min_medias=1, condicao="C", janelas_por_item=3,
                         progress=lambda *a, **k: None)
            core.Piloto(raiz / "junto", ["01_01"], "falso:low", modo="junto", prompt=core.PROMPT_JUNTO,
                        client=junto, **comum).run()
            core.Piloto(raiz / "separado", ["01_01"], "falso:low", modo="separado", client=sep, **comum).run()
            self.assertEqual(junto.tags, ["piloto_janela"] * 3)
            self.assertEqual(sorted(sep.tags), ["piloto_planejamento"] * 3 + ["piloto_redacao"] * 3)
            self.assertTrue(all("<exemplos_de_forma>" in u for u, tg in zip(sep.usuarios, sep.tags)
                                if tg == "piloto_redacao"))
            self.assertTrue(all("<exemplos_de_forma>" not in u for u, tg in zip(sep.usuarios, sep.tags)
                                if tg == "piloto_planejamento"))
            res = core.comparar(raiz, ("junto", "separado"), titulo="teste")
            self.assertEqual(res["junto"]["total"]["questoes"], 12)
            self.assertEqual(res["separado"]["total"]["questoes"], 9)
            self.assertEqual(res["separado"]["total"]["itens_descartados_redacao"], 3)
            self.assertEqual(res["junto"]["total"]["janelas_com_dificil_pct"], 100.0)
            self.assertEqual(res["junto"]["total"]["janelas_com_media_pct"], 100.0)
            self.assertEqual(res["separado"]["total"]["status"]["parcial"], 3, "3 questões < mínimo de 4")


if __name__ == "__main__":
    unittest.main()
