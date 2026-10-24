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

    def dedup(self, user):
        itens = json.loads(user)
        # marca como redundante a 2ª questão em diante quando há pelo menos 3
        if len(itens) >= 3:
            return {"grupos": [{"manter": itens[0]["id"], "remover": [itens[1]["id"]], "motivo": "mesmo conhecimento"}]}
        return {"grupos": []}

    def refino(self, user):
        import re as _re
        tipo = _re.search(r"Tipo: (\w+)", user).group(1)
        self.n += 1
        p, cen = PERGUNTAS[tipo]
        return {"status": "ok", "motivo": "", "tipo": tipo, "cenario": cen,
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
            for item in ("08_02", "06_06"):                                      # tópicos prontos para a avaliação
                d = Path(tmp) / "out" / "topicos" / item
                self.assertTrue((d / "finalizado.json").exists())
                n = len((d / "aprovadas.jsonl").read_text(encoding="utf-8").splitlines())
                self.assertEqual(n, res["topicos"][item]["validas"])
            self.assertTrue((Path(tmp) / "out" / "geracao_concluida.json").exists())


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
            # cada questão tem no máximo TENTATIVAS_REFINO refinos; cada chamada vira um arquivo
            self.assertEqual(f.tags.count("meta_refino"), res["refinador"]["tentadas"])
            self.assertIn(2, {int(k) for k in res["refinador"]["por_tentativa"]})
            refinos = [u for u, tag in zip(f.usuarios, f.tags) if tag == "meta_refino"]
            self.assertTrue(all("<ja_cobertas>" in u and "<exemplos_aprovados>" in u for u in refinos))
            self.assertTrue(any("<historico>" in u for u in refinos))

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


class V19Tests(unittest.TestCase):
    def test_dedup_e_texto_fonte_nas_refinadas(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Falso()
            cl = {p: f for p in rodadas.MODELOS}
            g = rodadas.GeracaoMeta(Path(tmp) / "out", ["08_02"], reusar=None, banco_inicial=None, clientes=cl,
                                    workers=2, progress=lambda *a, **k: None)
            self.assertEqual(g.run(), 0)
            dedup = json.loads((Path(tmp) / "out" / "topicos" / "08_02" / "dedup.json").read_text(encoding="utf-8"))
            self.assertEqual(len(dedup["grupos"]), 1)
            res = json.loads((Path(tmp) / "out" / "resultado.json").read_text(encoding="utf-8"))
            self.assertEqual(sum(b["redundantes"] for b in res["por_rodada"].values()), 1)
            auditorias = [u for u, tag in zip(f.usuarios, f.tags) if tag == "meta_auditoria"]
            self.assertTrue(any("texto_fonte" in u for u in auditorias))
            antes = f.chamadas
            rodadas.GeracaoMeta(Path(tmp) / "out", ["08_02"], reusar=None, banco_inicial=None, clientes=cl, workers=2,
                                progress=lambda *a, **k: None).run()
            self.assertEqual(f.chamadas, antes)   # dedup não é refeito se as aprovadas não mudaram


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

    def test_referencia_a_fonte_barrada(self):
        from pipeline.qa_research.tipos import problemas_tipo
        self.assertTrue(problemas_tipo("conceito", False, "Qual técnica descrita nos blocos avalia detritos de desgaste?",
                                       "Ferrografia."))
        self.assertTrue(problemas_tipo("consequencia", True, "Num FPSO, a linha mudou. Qual efeito técnico, único sob "
                                       "essas condições, aparece?", "Caminho de comunicação entre sistemas."))
        self.assertFalse(problemas_tipo("diagnostico", True, "Durante a preparação de uma linha drenada, reaparece fluido "
                                        "no trecho quando a bomba parte. Qual a causa?", "Válvula de bloqueio passando."))

    def test_refino_cosmetico_recusado(self):
        orig = {"pergunta": "Que informação do sistema de manutenção serve de base comum ao planejamento e à programação?",
                "resposta": "As datas programadas das atividades."}
        d = {"status": "ok", "motivo": "", "cenario": False,
             "pergunta": "Qual informação do sistema de gestão de manutenção serve de base comum ao planejamento e à programação?",
             "resposta": "Datas programadas das atividades."}
        with self.assertRaisesRegex(ValueError, "quase igual"):
            rodadas.validar_refino(d, "conceito", orig)
        d2 = {**d, "pergunta": "Que registro do sistema de manutenção permite medir o atraso acumulado do backlog?"}
        rodadas.validar_refino(d2, "conceito", orig)


class RefinoForteTests(unittest.TestCase):
    """Experimento de refino sobre o piloto v19 versionado, com clientes falsos."""

    class Cliente:
        def __init__(self):
            self.usuarios = []

        def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
            self.usuarios.append((tag, user))
            if tag == "refino_forte":
                r = 2 if "<historico>" in user else 1
                uid = rodadas._h(user) % 100000
                d = {"status": "ok", "motivo": "", "tipo": "mecanismo", "cenario": False,
                     "pergunta": (f"Por que o fenômeno {uid} ocorre em separadores {uid}?" if r == 1 else
                                  f"Na rodada 2, qual elo técnico {uid} explica a corrosão observada em tanques {uid}?"),
                     "resposta": (f"Porque a causa {uid} atua." if r == 1 else f"Porque a camada aquosa {uid} sustenta pilhas.")}
            elif tag == "refino_auditoria":
                itens = json.loads(user)
                ok = [("rodada 2" in x["pergunta"] or k % 2 == 0) for k, x in enumerate(itens)]
                d = {"avaliacoes": [{"id": x["id"], "tipo_confere": True, "tipo_sugerido": "mecanismo",
                                     "motivo": "nenhum" if o else "trivial", "referencia_valida": True,
                                     "atalho": not o, "justificativa": "j"} for x, o in zip(itens, ok)]}
                assert all("texto_fonte" in x for x in itens)
            else:
                d = {"grupos": []}
            if validate:
                validate(d)
            return d

    def test_rodadas_historico_e_ganho_liquido(self):
        from pipeline.qa_research.geracao_tipos.refino_forte import ExperimentoRefino
        c = self.Cliente()
        with tempfile.TemporaryDirectory() as t:
            e = ExperimentoRefino(Path(t), bracos={"forte": "x"}, rodadas=2, workers=2,
                                  clientes={"refinador_forte": c, "auditoria": c}, progress=lambda *a, **k: None)
            n = len(e.candidatas())
            self.assertGreater(n, 100)
            self.assertEqual(e.run(), 0)
            res = json.loads((Path(t) / "resultado.json").read_text(encoding="utf-8"))
            b = res["bracos"]["forte"]
            self.assertEqual(b["recuperadas"], n)        # quem falhou na 1ª foi aprovado na 2ª
            self.assertEqual(b["ganho_liquido"], n)
            self.assertTrue(b["rodadas"][1]["tentadas"] > 0)
            self.assertTrue(any("<exemplos_aprovados>" in u and "<blocos>" in u for tg, u in c.usuarios if tg == "refino_forte"))
            self.assertTrue((Path(t) / "REFINO.md").exists())

    def test_braco_cob_recebe_aprovadas_dos_mesmos_blocos(self):
        from pipeline.qa_research.geracao_tipos.refino_forte import ExperimentoRefino
        c = self.Cliente()
        with tempfile.TemporaryDirectory() as t:
            e = ExperimentoRefino(Path(t), bracos={"forte_cob": "x"}, rodadas=1, workers=2,
                                  clientes={"refinador_forte_cob": c, "auditoria": c}, progress=lambda *a, **k: None)
            q = e.candidatas()[0]
            cob = e.cobertas("forte_cob", 1, q)
            self.assertTrue(all(e.blocos_de(x) & e.blocos_de(q) for x in cob))
            self.assertEqual(e.run(), 0)
            refinos = [u for tg, u in c.usuarios if tg == "refino_forte"]
            self.assertTrue(refinos and all("<ja_cobertas>" in u for u in refinos))

    def test_validacao_v3(self):
        from pipeline.qa_research.geracao_tipos.refino_forte import validar_refino_v3
        d = {"status": "ok", "motivo": "", "tipo": "diagnostico", "cenario": False,
             "pergunta": "Qual a causa da queda de pressão?", "resposta": "Filtro obstruído."}
        with self.assertRaises(ValueError):   # diagnóstico exige cenário
            validar_refino_v3(d, "conceito")
        with self.assertRaises(ValueError):
            validar_refino_v3({**d, "tipo": "inventado"}, "conceito")


class AvaliacaoTests(unittest.TestCase):
    class Cliente:
        def __init__(self, falha=False):
            self.falha, self.lotes = falha, []

        def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
            if self.falha:
                raise RuntimeError("DeploymentNotFound")
            if tag.startswith(("resposta_", "teste_")):
                d = {"resposta": "Separar óleo, gás e água." if "trifásico" in user else "resposta " + user[:20]}
            else:
                itens = json.loads(user)
                self.lotes.append(len(itens))
                d = {"avaliacoes": [{"id": x["id"], "veredito": ("correta" if k % 2 == 0 else "parcial"),
                                     "justificativa": "j"} for k, x in enumerate(itens)]}
            if validate:
                validate(d)
            return d

    def _rodada(self, tmp, itens=("01_01", "02_02"), n=11):
        r = Path(tmp) / "rod"
        for it in itens:
            d = r / "topicos" / it
            d.mkdir(parents=True)
            qs = [{"uid": f"{it}:j:{k}", "item": it, "tipo": ("conceito", "diagnostico")[k % 2],
                   "composicao": "simples", "pergunta": f"Pergunta {it} {k}?", "resposta": "Ref."} for k in range(n)]
            (d / "aprovadas.jsonl").write_text("\n".join(json.dumps(q) for q in qs), encoding="utf-8")
        return r

    def test_lotes_tabela_e_modelo_indisponivel(self):
        from pipeline.qa_research.geracao_tipos.avaliacao import AvaliacaoModelos
        with tempfile.TemporaryDirectory() as tmp:
            r = self._rodada(tmp)
            (r / "topicos" / "01_01" / "finalizado.json").write_text("{}", encoding="utf-8")   # só um tópico pronto
            juiz = self.Cliente()
            cl = {"resp_a": self.Cliente(), "resp_b": self.Cliente(falha=True), "juiz": juiz}
            e = AvaliacaoModelos(r, respondentes={"a": "x:low", "b": "y"}, lote_juiz=5, workers=2, clientes=cl,
                                 progress=lambda *a, **k: None)
            e.saida.mkdir(parents=True)
            e.checar_modelos()
            self.assertEqual(list(e.respondentes), ["a"])
            e.passagem(final=False)
            self.assertEqual(sorted(juiz.lotes), [5, 5])           # 11 respostas: o lote incompleto espera
            e.passagem(final=True)
            self.assertEqual(sorted(juiz.lotes), [1, 5, 5])
            res = json.loads((e.saida / "acuracia.json").read_text(encoding="utf-8"))
            self.assertEqual(res["geral"]["a"]["n"], 11)
            self.assertEqual(res["por_tipo"]["conceito"]["a"]["n"], 6)
            md = (e.saida / "ACURACIA.md").read_text(encoding="utf-8")
            self.assertIn("Por tipo de questão", md)
            self.assertEqual(len((e.saida / "avaliacoes.jsonl").read_text(encoding="utf-8").splitlines()), 11)

    def test_pares_em_sequencia(self):
        from pipeline.qa_research.geracao_tipos.avaliacao import AvaliacaoModelos
        ordem = []

        class Registra(self.Cliente):
            def __init__(self, nome):
                super().__init__()
                self.nome = nome

            def json(self, system, user, tag="", **kw):
                if tag.startswith("resposta_"):
                    ordem.append(self.nome)
                return super().json(system, user, tag=tag, **kw)

        with tempfile.TemporaryDirectory() as tmp:
            r = self._rodada(tmp, n=6)
            for it in ("01_01", "02_02"):
                (r / "topicos" / it / "finalizado.json").write_text("{}", encoding="utf-8")
            cl = {f"resp_{m}": Registra(m) for m in "abcd"}
            cl["juiz"] = self.Cliente()
            e = AvaliacaoModelos(r, respondentes={m: m for m in "abcd"}, grupos=[("a", "b"), ("c", "d")], bloco=5,
                                 workers=2, clientes=cl, progress=lambda *a, **k: None)
            self.assertEqual(e.run(), 0)
            self.assertEqual(set(ordem[:24]), {"a", "b"})     # o 1º par termina antes do 2º começar
            self.assertEqual(set(ordem[24:]), {"c", "d"})
            res = json.loads((e.saida / "acuracia.json").read_text(encoding="utf-8"))
            self.assertTrue(all(res["geral"][m]["n"] == 12 for m in "abcd"))

    def test_espera_marcador_da_geracao(self):
        from pipeline.qa_research.geracao_tipos.avaliacao import AvaliacaoModelos
        with tempfile.TemporaryDirectory() as tmp:
            r = self._rodada(tmp, n=4)
            for it in ("01_01", "02_02"):
                (r / "topicos" / it / "finalizado.json").write_text("{}", encoding="utf-8")
            (r / "geracao_encerrada").write_text("", encoding="utf-8")
            cl = {"resp_a": self.Cliente(), "juiz": self.Cliente()}
            e = AvaliacaoModelos(r, respondentes={"a": "x"}, lote_juiz=8, workers=2, intervalo=1, clientes=cl,
                                 progress=lambda *a, **k: None)
            self.assertEqual(e.run(esperar=True), 0)
            res = json.loads((e.saida / "acuracia.json").read_text(encoding="utf-8"))
            self.assertEqual(res["geral"]["a"]["n"], 8)


if __name__ == "__main__":
    unittest.main()
