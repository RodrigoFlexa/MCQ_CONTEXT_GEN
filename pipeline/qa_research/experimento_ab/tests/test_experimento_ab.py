"""Testes offline do experimento A/B (clientes e embeddings simulados; nenhuma chamada de API)."""
import csv
import hashlib
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np

from pipeline.qa_research.experimento_ab import comum as C
from pipeline.qa_research.experimento_ab import dedup as D
from pipeline.qa_research.experimento_ab import geracao as GA
from pipeline.qa_research.experimento_ab.calibracao import Calibracao, auc, limiares
from pipeline.qa_research.piloto_janela.core import blocos, read_json
from pipeline.qa_research.tests.test_geracao_meta import Falso as FalsoV21
from pipeline.qa_research.tests.test_geracao_tipos import PERGUNTAS

ITEM = "03_03"
SILENCIO = dict(progress=lambda *a, **k: None)


class Emb:
    """Embedding simulado: saco de palavras com hashing (textos com as mesmas palavras ficam próximos)."""
    def __init__(self, dim=64):
        self.dim, self.chamadas = dim, 0

    def encode(self, textos):
        self.chamadas += 1
        out = []
        for t in textos:
            v = np.zeros(self.dim)
            for w in re.findall(r"\w+", t.lower()):
                v[int(hashlib.md5(w.encode()).hexdigest(), 16) % self.dim] += 1
            out.append(v / max(1e-9, np.linalg.norm(v)))
        return np.array(out)


class Juiz:
    """Juiz da deduplicação: redundante quando a última palavra da resposta coincide com a de alguma existente."""
    def __init__(self, falhar=()):
        self.chamadas, self.falhar = 0, set(falhar)

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        self.chamadas += 1
        d = json.loads(user)
        if d["nova"]["pergunta"] in self.falhar:
            raise RuntimeError("falha simulada do juiz")
        chave = lambda r: r.rstrip(".").split()[-1]
        alvo = next((e for e in d["existentes"] if chave(e["resposta"]) == chave(d["nova"]["resposta"])), None)
        r = ({"redundante": True, "com": alvo["id"], "manter": "existente", "motivo": "mesma resposta"} if alvo else
             {"redundante": False, "com": None, "manter": None, "motivo": "outro conhecimento"})
        if validate:
            validate(r)
        return r


class Falso(FalsoV21):
    """Cliente v21 simulado, aceitando também o contexto de capítulo; respostas repetem a cada 5 questões."""
    def __init__(self, faith=None):
        super().__init__()
        self.faith = faith or (lambda d: True)

    def janela(self, user):
        texto_f = re.search(r"\[F\] [^\n]*\n(.+?)(?:\n\n\[A\d+\]|\n</janela>|\n</capitulo>)", user, re.S).group(1)
        trecho = " ".join(texto_f.split()[:8])
        qs = []
        for k, t in enumerate(("conceito", "mecanismo", "procedimento", "diagnostico"), 1):
            self.n += 1
            p, cen = PERGUNTAS[t]
            qs.append({"id": k, "tipo": t, "cenario": cen, "conhecimento": f"r{self.n}",
                       "pergunta": p.format(k=f"{self.n} alfa{self.n} beta{self.n} gama{self.n}"),
                       "resposta": f"Elemento{self.n} especifico{self.n} relativo{self.n % 7}.",
                       "fundamentos": [{"bloco": "F", "trecho": trecho}]})
        return {"status": "ok", "motivo": "", "questoes": qs}

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        if tag.startswith("sust_"):
            self.chamadas += 1
            self.tags.append(tag)
            d = json.loads(user)
            if tag == "sust_reparo":
                r = {"status": "ok", "resposta": "Resposta curta sustentada.", "explicacao": "", "motivo": "corte"}
                if d["pergunta"].endswith("descartar?"):
                    r = {"status": "descartar", "resposta": "", "explicacao": "", "motivo": "sem suporte"}
            else:
                b = d["blocos"][0]
                ok = self.faith(d)
                r = {"cobertura_completa": True, "observacoes": "", "afirmacoes": [
                    {"afirmacao": d["gabarito"], "veredito": "sustentada" if ok else "insuficiente",
                     "evidencias": [{"bloco": b["id"], "trecho": b["texto"][:40]}] if ok else [],
                     "justificativa": "j"}]}
            if validate:
                validate(r)
            return r
        return super().json(system, user, tag, max_tokens, validate, item)


def calibracao_falsa(pasta: Path, auto=0.97, juiz=0.3, dim=64) -> Path:
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "media_3-large.json").write_text(json.dumps([0.0] * dim), encoding="utf-8")
    arq = pasta / "calibracao.json"
    arq.write_text(json.dumps({"embedding": "3-large", "media": "media_3-large.json", "limiar_auto": auto,
                               "limiar_juiz": juiz, "juiz": "juiz-falso"}), encoding="utf-8")
    return arq


class ContextoTests(unittest.TestCase):
    def test_capitulo_rotula_foco_e_apoios_e_janela_igual_v21(self):
        _, bs = blocos(ITEM, C.FONTE_DOCS / "refinado")
        foco = next(b["indice"] for b in bs if b["bloco"] == 2)
        cap = C.contexto_foco(bs, foco, "capitulo")
        self.assertEqual([r for r, _ in cap].count("F"), 1)
        self.assertTrue(all(b["capitulo"] == bs[foco]["capitulo"] for _, b in cap))
        self.assertEqual(len(cap), sum(b["capitulo"] == bs[foco]["capitulo"] for b in bs))
        self.assertEqual([r for r, _ in C.contexto_foco(bs, foco, "janela")], ["A1", "F", "A2"])

    def test_avaliacao_usa_capitulos_tocados_inclusive_janela_na_fronteira(self):
        _, bs = blocos(ITEM, C.FONTE_DOCS / "antigo")
        primeiro_cap2 = next(b["indice"] for b in bs if b["capitulo"] == 1)
        q = {"uid": "x", "foco": primeiro_cap2}
        caps = {bs[i]["capitulo"] for i in C.indices_avaliacao(q, bs, "janela")}
        self.assertEqual(caps, {0, 1})
        self.assertEqual({bs[i]["capitulo"] for i in C.indices_avaliacao(q, bs, "capitulo")}, {1})

    def test_prompt_capitulo_so_troca_contexto(self):
        base = GA.PROMPT_JANELA.read_text(encoding="utf-8")
        cap = GA.prompt_capitulo()
        self.assertNotIn("<janela>", cap)
        self.assertIn("<capitulo>\n{{JANELA}}\n</capitulo>", cap)
        self.assertEqual(len(base.splitlines()), len(cap.splitlines()))
        diferentes = [a for a, b in zip(base.splitlines(), cap.splitlines()) if a != b]
        self.assertEqual(len(diferentes), 6)   # 5 trocas; a última muda duas linhas (abre e fecha a tag)

    def test_validador_aceita_rotulos_do_capitulo_so_no_capitulo(self):
        d = Falso().janela("[F] t / s\ntexto do bloco foco com palavras suficientes aqui\n</capitulo>")
        d["questoes"][0]["fundamentos"].append({"bloco": "A3", "trecho": "outro"})
        GA.validar_unidade(d, {"F", "A1", "A2", "A3"})
        with self.assertRaises(ValueError):
            GA.validar_unidade(d, {"A1", "F", "A2"})


class DedupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)

    def q(self, k, resposta, pergunta=None):
        return {"uid": f"{ITEM}:j:r1:{k:03d}:1", "item": ITEM, "pergunta": pergunta or f"Pergunta {k} sobre tema{k}?",
                "resposta": resposta}

    def test_auto_juiz_nova_substituicao_e_falha_isolada(self):
        qs = [self.q(1, "estanqueidade do compartimento"), self.q(2, "estanqueidade do compartimento", "Pergunta 1 sobre tema1?"),
              self.q(3, "estanqueidade do compartimento"), self.q(4, "corrosão por oxigênio dissolvido"),
              self.q(5, "outra coisa", "Pergunta que falha?")]
        j = Juiz(falhar={"Pergunta que falha?"})
        falhas = []
        dd = D.DedupIncremental(self.tmp, Emb(), np.zeros(64), 0.99, 0.3, j, **SILENCIO)
        self.assertEqual(dd.processar(ITEM, qs, falha=lambda n, e: falhas.append(n)), 1)
        dec = {p.stem: read_json(p) for p in (self.tmp / ITEM).glob("*.json")}
        self.assertEqual(len(dec), 4)
        por = {d["uid"]: d for d in dec.values()}
        self.assertEqual(por[qs[1]["uid"]]["via"], "automatico")          # texto idêntico
        self.assertEqual(por[qs[2]["uid"]]["via"], "juiz")                # mesma resposta, outra pergunta
        self.assertEqual(por[qs[2]["uid"]]["decisao"], "redundante")
        self.assertEqual(por[qs[3]["uid"]]["decisao"], "nova")
        self.assertEqual(set(dd.redundantes(ITEM)), {qs[1]["uid"], qs[2]["uid"]})
        self.assertTrue(falhas and "dedup_03_03" in falhas[0])
        # retomada: só a questão que falhou é decidida
        j.falhar.clear()
        antes = j.chamadas
        self.assertEqual(dd.processar(ITEM, qs), 0)
        self.assertLessEqual(j.chamadas - antes, 1)
        self.assertEqual(len(list((self.tmp / ITEM).glob("*.json"))), 5)

    def test_substituicao_aponta_para_quem_ficou(self):
        class Troca(Juiz):
            def json(self, system, user, **kw):
                d = json.loads(user)
                r = {"redundante": True, "com": "E1", "manter": "nova", "motivo": "nova é melhor"}
                kw.get("validate", lambda x: None)(r)
                return r
        qs = [self.q(1, "a b c"), self.q(2, "a b c d"), self.q(3, "a b c d e")]
        dd = D.DedupIncremental(self.tmp, Emb(), np.zeros(64), 1.01, 0.1, Troca(), **SILENCIO)
        dd.processar(ITEM, qs)
        self.assertEqual(dd.redundantes(ITEM), {qs[0]["uid"]: qs[2]["uid"], qs[1]["uid"]: qs[2]["uid"]})

    def test_falha_de_embeddings_nao_derruba(self):
        class Quebrado:
            def encode(self, t):
                raise RuntimeError("embeddings fora do ar")
        nomes = []
        dd = D.DedupIncremental(self.tmp, Quebrado(), np.zeros(64), 0.99, 0.5, Juiz(), **SILENCIO)
        self.assertEqual(dd.processar(ITEM, [self.q(1, "x")], falha=lambda n, e: nomes.append(n)), 1)
        self.assertEqual(nomes, ["dedup_03_03_embeddings"])


class CalibracaoTests(unittest.TestCase):
    def test_auc_e_limiares(self):
        self.assertEqual(auc([0.9, 0.8, 0.2, 0.1], [1, 1, 0, 0]), 1.0)
        lim = limiares([0.99, 0.98, 0.97, 0.9, 0.5, 0.4, 0.3], [1, 1, 1, 0, 1, 0, 0])
        self.assertAlmostEqual(lim["limiar_auto"], 0.97)
        self.assertAlmostEqual(lim["limiar_juiz"], 0.5)
        self.assertIsNone(limiares([0.99, 0.98], [0, 1])["limiar_auto"])   # topo não redundante: nunca automático

    def test_calibracao_ponta_a_ponta_e_recalculo_com_rotulo_humano(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        fonte = tmp / "fonte"
        fonte.mkdir()
        rng = np.random.default_rng(0)
        aprov = []
        for it in ("01_01", "02_02"):
            for k in range(30):
                tema = rng.integers(0, 12)
                aprov.append({"uid": f"{it}:q{k}", "item": it, "pergunta": f"Qual o efeito do fator{tema} no sistema{k}?",
                              "resposta": f"Aumenta a perda no trocador{tema}."})
        removida = {**aprov[0], "uid": "01_01:rem", "redundante": aprov[0]["uid"]}
        C.gravar_jsonl(fonte / "aprovadas.jsonl", aprov)
        C.gravar_jsonl(fonte / "questoes.jsonl", aprov + [removida])
        juiz = Juiz()
        cl = {"referencia": juiz, "nano": Juiz(), "mini": Juiz()}
        cal = Calibracao(tmp / "cal", fonte=fonte, embeddings=["3-small", "3-large"], juizes={"nano": "n", "mini": "m"},
                         por_faixa=6, clientes=cl, embedders={"3-small": Emb(32), "3-large": Emb(64)}, **SILENCIO)
        self.assertEqual(cal.run(), 0)
        cfg = read_json(tmp / "cal" / "calibracao.json")
        self.assertIn(cfg["embedding"], ("3-small", "3-large"))
        self.assertEqual(cfg["juiz"], "n")   # o mais barato que concorda
        self.assertLessEqual(cfg["limiar_juiz"], cfg["limiar_auto"])
        self.assertTrue((tmp / "cal" / "CALIBRACAO.md").exists())
        pares = read_json(tmp / "cal" / "pares.json")["pares"]
        self.assertTrue(any(p["estrato"] == "dedup_antiga" for p in pares))
        # recálculo com rótulo humano: sem chamadas novas
        with (tmp / "cal" / "pares_rotulados.csv").open(encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        rows[0]["rotulo_humano"] = "nao" if rows[0]["rotulo_referencia"] == "sim" else "sim"
        with (tmp / "cal" / "rotulos_humanos.csv").open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        antes = juiz.chamadas
        cal2 = Calibracao(tmp / "cal", fonte=fonte, embeddings=["3-small", "3-large"], juizes={"nano": "n", "mini": "m"},
                          por_faixa=6, clientes=cl, embedders={"3-small": Emb(32), "3-large": Emb(64)}, **SILENCIO)
        cal2.run(recalcular=True)
        self.assertEqual(juiz.chamadas, antes)
        self.assertEqual(read_json(tmp / "cal" / "calibracao.json")["analise"]["rotulos_humanos"], 1)


class GeracaoTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        C.preparar_documentos(self.tmp / "exp", itens=[ITEM])
        self.cal = calibracao_falsa(self.tmp / "exp" / "calibracao")

    def gerar(self, nome, unidade, docs, f, juiz, reusar=(), sust=False, saida=None):
        cl = {p: f for p in ("relacoes", "combinacoes", "geracao", "auditoria", "refinador", "sustentacao", "reparo")}
        cl["dedup_juiz"] = juiz
        return GA.GeracaoAB(saida or self.tmp / "exp" / "bracos" / nome, [ITEM], docs=self.tmp / "exp" / "docs" / docs,
                            unidade=unidade, braco=nome, reusar=reusar, calibracao=self.cal, sustentacao=sust,
                            clientes=cl, embedder=Emb(), workers=4, **SILENCIO)

    def test_bracos_janela_e_capitulo_com_reuso_dedup_e_retomada(self):
        f, juiz = Falso(), Juiz()
        a = self.gerar("A", "janela", "antigo", f, juiz)
        self.assertEqual(a.run(), 0)
        dA = self.tmp / "exp" / "bracos" / "A"
        self.assertTrue((dA / "geracao_concluida.json").exists())
        res = read_json(dA / "resultado.json")
        self.assertEqual(res["unidade"], "janela")
        self.assertGreater(res["dedup_incremental"]["por_decisao"]["redundante"], 0)
        aprov = C.linhas(dA / "aprovadas.jsonl")
        self.assertTrue(aprov)
        red = {q["uid"] for q in C.linhas(dA / "questoes.jsonl") if q.get("redundante")}
        self.assertFalse(red & {q["uid"] for q in aprov})
        self.assertNotIn("meta_dedup", f.tags)    # dedup antiga (chamada única) não é usada
        # C: capítulo, reaproveita o inventário de A (nenhuma chamada de relações/encadeamentos)
        n_rel = f.tags.count("meta_relacoes")
        c = self.gerar("C", "capitulo", "antigo", f, juiz, reusar=[dA])
        self.assertEqual(c.run(), 0)
        self.assertEqual(f.tags.count("meta_relacoes"), n_rel)
        user_cap = [u for u, t in zip(f.usuarios, f.tags) if t == "meta_janela"][-1]
        self.assertIn("<capitulo>", user_cap)
        self.assertNotIn("<janela>", user_cap)
        jan = read_json(next((self.tmp / "exp" / "bracos" / "C" / "topicos" / ITEM / "janelas" / "r1").glob("*.json")))
        self.assertEqual(jan["unidade"], "capitulo")
        # retomada sem chamadas
        antes = f.chamadas
        self.assertEqual(self.gerar("C", "capitulo", "antigo", f, juiz, reusar=[dA]).run(), 0)
        self.assertEqual(f.chamadas, antes)
        # configuração diferente na mesma pasta é recusada
        with self.assertRaises(ValueError):
            self.gerar("C", "janela", "antigo", f, juiz, reusar=[dA]).run()

    def test_falha_do_juiz_fica_isolada_e_retoma(self):
        f = Falso()
        juiz = Juiz(falhar={"__nenhuma__"})
        g = self.gerar("B", "janela", "refinado", f, juiz)
        perguntas = []
        orig = juiz.json

        def falha_uma(system, user, **kw):
            d = json.loads(user)
            if not perguntas:
                perguntas.append(d["nova"]["pergunta"])
            if d["nova"]["pergunta"] == perguntas[0]:
                raise RuntimeError("falha simulada")
            return orig(system, user, **kw)
        juiz.json = falha_uma
        self.assertGreater(g.run(), 0)
        dB = self.tmp / "exp" / "bracos" / "B"
        self.assertFalse((dB / "geracao_concluida.json").exists())
        self.assertGreater(len(list((dB / "dedup_incremental" / ITEM).glob("*.json"))), 5)   # demais decididas
        juiz.json = orig
        self.assertEqual(self.gerar("B", "janela", "refinado", f, juiz).run(), 0)
        self.assertTrue((dB / "geracao_concluida.json").exists())

    def test_sustentacao_repara_descarta_e_mantem(self):
        f = Falso(faith=lambda d: "Resposta curta" in d["gabarito"] or int(hashlib.md5(d["pergunta"].encode()).hexdigest(), 16) % 3 > 0)
        juiz = Juiz()
        self.assertEqual(self.gerar("B", "janela", "refinado", f, juiz).run(), 0)
        origem = self.tmp / "exp" / "bracos" / "B"
        destino = self.tmp / "exp" / "bracos" / "B_sust"
        shutil.copytree(origem, destino, ignore=shutil.ignore_patterns(
            "dedup_incremental", "geracao_concluida.json", "aprovadas.jsonl", "finalizado.json", "resultado.json",
            "config.json", "RELATORIO.md"))
        antes = f.tags.count("meta_janela")
        g = self.gerar("B_sust", "janela", "refinado", f, juiz, sust=True)
        self.assertEqual(g.run(), 0)
        self.assertEqual(f.tags.count("meta_janela"), antes)   # mesmas questões: nada é gerado de novo
        res = read_json(destino / "resultado.json")["sustentacao"]
        self.assertGreater(res["sustentada"], 0)
        self.assertGreater(res["reparada"], 0)
        aprov = C.linhas(destino / "aprovadas.jsonl")
        rep = [q for q in aprov if q.get("sustentacao") == "reparada"]
        self.assertTrue(rep and all(q["resposta"] == "Resposta curta sustentada." and q["resposta_original"] for q in rep))


class AvaliacaoEComparacaoTests(unittest.TestCase):
    def test_avaliacao_com_capitulo_e_comparacao(self):
        from pipeline.qa_research.experimento_ab import avaliacao as AV
        from pipeline.qa_research.experimento_ab.metricas import comparar
        from pipeline.qa_research.tests.test_benchmark_gap import Answer, Faith
        from pipeline.qa_research.tests.test_especialista_finalizacao import Juiz as JuizResp
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        exp = tmp / "exp"
        C.preparar_documentos(exp, itens=[ITEM])
        cal = calibracao_falsa(exp / "calibracao")
        f, juiz = Falso(), Juiz()
        for nome, unidade, docs, reusar in (("A", "janela", "antigo", ()), ("C", "capitulo", "antigo", [exp / "bracos" / "A"])):
            cl = {p: f for p in ("relacoes", "combinacoes", "geracao", "auditoria", "refinador")}
            cl["dedup_juiz"] = juiz
            g = GA.GeracaoAB(exp / "bracos" / nome, [ITEM], docs=exp / "docs" / docs, unidade=unidade, braco=nome,
                             reusar=reusar, calibracao=cal, clientes=cl, embedder=Emb(), workers=4, **SILENCIO)
            self.assertEqual(g.run(), 0)
            a, b, c, fa = Answer(), Answer(), Answer(), Faith()
            st = AV.executar(exp / "bracos" / nome, exp / "avaliacao" / nome, workers=3, judge_workers=1,
                             clientes={"resp_gpt-4-1-nano": a, "resp_gpt-4-1-mini": b, "resp_gpt-4-1": c,
                                       "juiz": JuizResp(), "faithfulness": fa}, progress=lambda *x, **k: None)
            self.assertEqual(st, 0)
            ctx = C.linhas(exp / "avaliacao" / nome / "contextos.jsonl")
            _, bs = blocos(ITEM, exp / "docs" / docs)
            for q in ctx:   # contexto de avaliação = capítulos inteiros
                caps = {bs[b["indice_documento"]]["capitulo"] for b in q["blocos_contexto"]}
                self.assertEqual(len(q["blocos_contexto"]), sum(x["capitulo"] in caps for x in bs))
        out = comparar(exp)
        self.assertEqual(set(out["bracos"]), {"A", "C"})
        self.assertIn("unidade (antigo): C-A", out["efeitos"])
        self.assertEqual(out["bracos"]["A"]["sustentacao"]["taxa_totalmente_sustentadas"], 1.0)
        self.assertTrue((exp / "COMPARACAO.md").exists())
        self.assertTrue((exp / "por_questao.csv").exists())


if __name__ == "__main__":
    unittest.main()


class CLITests(unittest.TestCase):
    def test_fluxo_pela_cli_com_sustentacao_e_comparacao(self):
        from unittest.mock import patch
        from pipeline.qa_research.experimento_ab import __main__ as M
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        exp = tmp / "exp"
        f = Falso(faith=lambda d: "Resposta curta" in d["gabarito"] or len(d["pergunta"]) % 2 == 0)
        juiz = Juiz()

        def fabrica(model, effort, cache_path, *a, **kw):
            return juiz if Path(cache_path).stem == "dedup_juiz" else f

        with patch.object(C, "ITENS", (ITEM,)), patch("pipeline.inventario.llm.LLMClient", fabrica), \
                patch.object(C, "embedder", lambda *a, **k: Emb()):
            self.assertEqual(M.main(["preparar", "--experimento", str(exp)]), 0)
            calibracao_falsa(exp / "calibracao")
            with self.assertRaises(SystemExit):
                M.main(["gerar", "--braco", "C", "--experimento", str(exp)])   # exige A antes
            self.assertEqual(M.main(["gerar", "--braco", "A", "--experimento", str(exp), "--workers", "3"]), 0)
            self.assertEqual(M.main(["gerar", "--braco", "C", "--experimento", str(exp), "--workers", "3"]), 0)
            self.assertEqual(M.main(["sustentacao", "--braco", "A", "--experimento", str(exp), "--workers", "3"]), 0)
            cfg = read_json(exp / "bracos" / "A_sust" / "config.json")
            self.assertTrue(cfg["sustentacao"])
            self.assertEqual(cfg["origem"], C.relativo(exp / "bracos" / "A"))
            # retomada da etapa 4 sem chamadas novas
            antes = f.chamadas
            self.assertEqual(M.main(["sustentacao", "--braco", "A", "--experimento", str(exp), "--workers", "3"]), 0)
            self.assertEqual(f.chamadas, antes)
            self.assertEqual(M.main(["saturar", "--braco", "A", "--experimento", str(exp), "--workers", "3",
                                     "--max-rodadas", "2"]), 0)
            self.assertEqual(read_json(exp / "bracos" / "A_sat" / "config.json")["saturacao"],
                             {"max_rodadas": 2, "paciencia": 1})
            with self.assertRaises(SystemExit):
                M.main(["gerar", "--braco", "A_sat", "--experimento", str(exp)])
            self.assertEqual(M.main(["comparar", "--experimento", str(exp)]), 0)
        out = read_json(exp / "comparacao.json")
        self.assertEqual(set(out["bracos"]), {"A", "C", "A_sust", "A_sat"})
        self.assertIn("sustentação: A_sust-A", out["efeitos"])
        self.assertIn("saturação: A_sat-A", out["efeitos"])
        self.assertIn("1", out["bracos"]["A_sat"]["saturacao_resumo"]["conhecimentos_novos_por_rodada"])
        self.assertTrue(out["bracos"]["A_sust"]["checagem_sustentacao"]["reparada"] > 0)


class EmbedderDiretoTests(unittest.TestCase):
    def test_sem_tiktoken_cache_e_lotes(self):
        from types import SimpleNamespace as NS

        class API:
            def __init__(self):
                self.chamadas = []
                self.embeddings = self

            def create(self, model, input, dimensions, encoding_format):
                self.chamadas.append(list(input))
                assert all(isinstance(t, str) for t in input)   # texto direto, sem tokens
                return NS(data=[NS(index=i, embedding=list(Emb(dimensions).encode([t])[0])) for i, t in enumerate(input)],
                          usage=NS(total_tokens=10))

        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        api = API()
        e = C.EmbedderDireto("3-small", tmp, client=api, lote=2)
        textos = ["a b", "c d", "a b", "e f", "g h"]
        V = e.encode(textos)
        self.assertEqual(V.shape, (5, 1536))
        self.assertTrue(np.allclose(V[0], V[2]))
        self.assertEqual([len(c) for c in api.chamadas], [2, 2])   # 4 textos únicos em lotes de 2
        e.encode(textos)
        self.assertEqual(len(api.chamadas), 2)                      # tudo do cache
        self.assertTrue((tmp / "chamadas" / "embeddings_3-small.jsonl").exists())
        with self.assertRaises(ValueError):
            e.encode(["x" * (C.MAX_CARACTERES + 1)])
        e.close()


class FalsoSat(Falso):
    """Rodada 1: questões novas. Rodada 2: focos 'pares' trazem questões novas, 'ímpares' repetem as da 1ª visita.
    Rodada 3 em diante: todos repetem. O auditor aprova tudo (sem refino), para o ganho ser determinístico."""
    def __init__(self):
        super().__init__()
        self.visitas, self.primeira = {}, {}

    def janela(self, user):
        f = re.search(r"\[F\] [^\n]*\n(.+?)(?:\n\n\[A\d+\]|\n</janela>|\n</capitulo>)", user, re.S).group(1)
        v = self.visitas[f] = self.visitas.get(f, 0) + 1
        par = int(hashlib.md5(f.encode()).hexdigest(), 16) % 2 == 0
        if v == 1 or (v == 2 and par):
            d = super().janela(user)
            self.primeira.setdefault(f, d)
            return d
        return json.loads(json.dumps(self.primeira[f]))

    def auditoria(self, user):
        itens = json.loads(user)
        return {"avaliacoes": [{"id": i["id"], "tipo_confere": True, "tipo_sugerido": i["tipo_declarado"],
                                "referencia_valida": True, "atalho": False, "motivo": "nenhum", "justificativa": "j"}
                               for i in itens]}


class NuncaRedundante(Juiz):
    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        self.chamadas += 1
        r = {"redundante": False, "com": None, "manter": None, "motivo": "outro conhecimento"}
        if validate:
            validate(r)
        return r


class SaturacaoTests(unittest.TestCase):
    def test_focos_saturam_individualmente_e_retomada(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        exp = tmp / "exp"
        C.preparar_documentos(exp, itens=[ITEM])
        cal = calibracao_falsa(exp / "calibracao", auto=1.01)
        f, juiz = FalsoSat(), NuncaRedundante()
        cl = {p: f for p in ("relacoes", "combinacoes", "geracao", "auditoria", "refinador")}
        cl["dedup_juiz"] = juiz

        def g(nome, sat=None):
            return GA.GeracaoAB(exp / "bracos" / nome, [ITEM], docs=exp / "docs" / "antigo", unidade="janela", braco=nome,
                                calibracao=cal, saturacao=sat, clientes=cl, embedder=Emb(), workers=4, **SILENCIO)

        self.assertEqual(g("A").run(), 0)
        r1 = f.tags.count("meta_janela")
        shutil.copytree(exp / "bracos" / "A", exp / "bracos" / "A_sat", ignore=shutil.ignore_patterns(
            "geracao_concluida.json", "aprovadas.jsonl", "finalizado.json", "resultado.json", "config.json", "RELATORIO.md"))
        sat = g("A_sat", {"max_rodadas": 5, "paciencia": 1})
        self.assertEqual(sat.run(), 0)
        _, bs = blocos(ITEM, exp / "docs" / "antigo")
        pares = {b["indice"] for b in bs if int(hashlib.md5(b["texto"].encode()).hexdigest(), 16) % 2 == 0}
        res = read_json(exp / "bracos" / "A_sat" / "saturacao.json")
        novos = res["conhecimentos_novos_por_rodada"]
        self.assertGreater(novos["1"], 0)
        self.assertGreater(novos["2"], 0)
        self.assertEqual(novos["3"], 0)
        self.assertNotIn("4", novos)                       # parou sozinho, antes do teto de 5
        for k, v in res["focos"].items():
            foco = int(k.split(":")[1])
            self.assertEqual(v["visitas"], 3 if foco in pares else 2, k)
        # rodada 1 não foi refeita: só as rodadas extras chamaram o gerador
        self.assertEqual(f.tags.count("meta_janela") - r1, len(bs) + len(pares))
        aprov_a = {q["uid"] for q in C.linhas(exp / "bracos" / "A" / "aprovadas.jsonl")}
        aprov_s = {q["uid"] for q in C.linhas(exp / "bracos" / "A_sat" / "aprovadas.jsonl")}
        self.assertTrue(aprov_a < aprov_s)
        self.assertTrue((exp / "bracos" / "A_sat" / "geracao_concluida.json").exists())
        self.assertIn("saturacao", read_json(exp / "bracos" / "A_sat" / "config.json"))
        self.assertNotIn("saturacao", read_json(exp / "bracos" / "A" / "config.json"))
        antes = f.chamadas
        self.assertEqual(g("A_sat", {"max_rodadas": 5, "paciencia": 1}).run(), 0)
        self.assertEqual(f.chamadas, antes)

    def test_teto_de_rodadas(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        exp = tmp / "exp"
        C.preparar_documentos(exp, itens=[ITEM])
        cal = calibracao_falsa(exp / "calibracao", auto=1.01)
        f = Falso()   # sempre gera questões novas: nunca satura sozinho
        cl = {p: f for p in ("relacoes", "combinacoes", "geracao", "auditoria", "refinador")}
        cl["dedup_juiz"] = NuncaRedundante()
        g = GA.GeracaoAB(exp / "bracos" / "A_sat", [ITEM], docs=exp / "docs" / "antigo", unidade="janela", braco="A_sat",
                         calibracao=cal, saturacao={"max_rodadas": 3}, clientes=cl, embedder=Emb(), workers=4, **SILENCIO)
        self.assertEqual(g.run(), 0)
        res = read_json(exp / "bracos" / "A_sat" / "saturacao.json")
        self.assertEqual(set(res["conhecimentos_novos_por_rodada"]), {"1", "2", "3"})
        self.assertTrue(all(v["visitas"] <= 3 for v in res["focos"].values()))
