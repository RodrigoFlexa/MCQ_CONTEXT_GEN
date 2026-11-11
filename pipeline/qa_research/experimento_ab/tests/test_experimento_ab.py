"""Testes offline do experimento A/B (clientes e embeddings simulados; nenhuma chamada de API)."""
import csv
import hashlib
import json
import re
import shutil
import tempfile
import unittest
from collections import Counter, defaultdict
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


class FalsoV22(Falso):
    """Gerador v22 simulado. 1ª visita: 3 propostas (uma boa, uma longa demais para a régua, uma que o auditor recusa).
    2ª visita: focos 'pares' trazem uma questão nova; os demais devolvem zero. 3ª visita: zero."""
    def __init__(self, falhar_auditoria=None):
        super().__init__()
        self.visitas, self.falhar_auditoria = {}, falhar_auditoria
        self.usuarios_foco = []

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        if not tag.startswith("v22_"):
            return super().json(system, user, tag, max_tokens, validate, item)
        self.chamadas += 1
        self.tags.append(tag)
        d = getattr(self, tag[4:])(user)
        if validate:
            validate(d)
        return d

    def _q(self, tipo, trecho, bloco, extra=""):
        self.n += 1
        p, cen = PERGUNTAS[tipo]
        return {"tipo": tipo, "cenario": cen, "conhecimento": f"conhecimento {self.n}",
                "pergunta": p.format(k=f"{self.n} alfa{self.n} beta{self.n}{extra}"),
                "resposta": f"Elemento{self.n} especifico{self.n}.", "explicacao": "Porque o bloco afirma.",
                "fundamentos": [{"bloco": bloco, "trecho": trecho}]}

    def foco(self, user):
        self.usuarios_foco.append(user)
        f = re.search(r"\[F\] [^\n]*\n(.+?)(?:\n\n\[A\d+\]|\n</janela>)", user, re.S).group(1)
        trecho = " ".join(f.split()[:8])
        v = self.visitas[f] = self.visitas.get(f, 0) + 1
        par = int(hashlib.md5(f.encode()).hexdigest(), 16) % 2 == 0
        if v == 1:
            longa = self._q("mecanismo", trecho, "F")
            longa["resposta"] = " ".join(["palavra"] * 25)
            return {"motivo": "", "questoes": [self._q("conceito", trecho, "F"), longa,
                                               self._q("mecanismo", trecho, "F", extra=" ATALHO")]}
        if v == 2 and par:
            return {"motivo": "", "questoes": [self._q("procedimento", trecho, "F")]}
        return {"motivo": "conhecimentos de [F] já cobertos", "questoes": []}

    def composta(self, user):
        b1 = re.search(r"\[B1\] [^\n]*\n(.+?)(?:\n\n\[B\d+\]|\n</blocos>)", user, re.S).group(1)
        if "C1" in user.split("<encadeamento>")[1][:400]:
            return {"motivo": "encadeamento não sustenta questão boa", "questoes": []}
        q = self._q("diagnostico", " ".join(b1.split()[:8]), "B1")
        return {"motivo": "", "questoes": [q]}

    def auditoria(self, user):
        d = json.loads(user)
        if self.falhar_auditoria and self.falhar_auditoria in d["pergunta"]:
            raise RuntimeError("falha simulada do auditor")
        atalho = "ATALHO" in d["pergunta"]
        return {"sem_documento": True, "resposta_alternativa": "outra", "alternativa_excluida": True, "atalho": atalho,
                "sustentada": True, "elemento_unico": True, "tipo_sugerido": d["tipo_declarado"],
                "justificativa": "atalho" if atalho else "ok"}


class FalsoSegundaChance(FalsoV22):
    """1ª visita: só questões que o auditor recusa. 2ª visita (segunda chance): uma boa. 3ª: de novo só recusadas,
    e o foco fecha (a segunda chance é uma só). Compostas: a 1ª tentativa é recusada; a 2ª, aprovada."""
    def foco(self, user):
        self.usuarios_foco.append(user)
        f = re.search(r"\[F\] [^\n]*\n(.+?)(?:\n\n\[A\d+\]|\n</janela>)", user, re.S).group(1)
        trecho = " ".join(f.split()[:8])
        v = self.visitas[f] = self.visitas.get(f, 0) + 1
        if v == 2:
            return {"motivo": "", "questoes": [self._q("procedimento", trecho, "F")]}
        return {"motivo": "", "questoes": [self._q("mecanismo", trecho, "F", extra=" ATALHO")]}

    def composta(self, user):
        self.usuarios_composta = getattr(self, "usuarios_composta", []) + [user]
        b1 = re.search(r"\[B1\] [^\n]*\n(.+?)(?:\n\n\[B\d+\]|\n</blocos>)", user, re.S).group(1)
        extra = "" if "<tentativa_anterior>" in user else " ATALHO"
        return {"motivo": "", "questoes": [self._q("diagnostico", " ".join(b1.split()[:8]), "B1", extra=extra)]}


class V22Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.exp = self.tmp / "exp"
        C.preparar_documentos(self.exp, itens=[ITEM])
        self.cal = calibracao_falsa(self.exp / "calibracao", auto=1.01)
        f = Falso()
        cl = {p: f for p in ("relacoes", "combinacoes", "geracao", "auditoria", "refinador")}
        cl["dedup_juiz"] = NuncaRedundante()
        GA.GeracaoAB(self.exp / "bracos" / "B", [ITEM], docs=self.exp / "docs" / "refinado", unidade="janela", braco="B",
                     calibracao=self.cal, clientes=cl, embedder=Emb(), workers=4, **SILENCIO).run()

    def g(self, f, **kw):
        from pipeline.qa_research.experimento_ab.v22 import GeracaoV22
        cl = {p: f for p in ("relacoes", "combinacoes", "geracao", "auditoria")}
        cl["dedup_juiz"] = NuncaRedundante()
        return GeracaoV22(self.exp / "bracos" / "B_v22", [ITEM], docs=self.exp / "docs" / "refinado", braco="B_v22",
                          reusar=[self.exp / "bracos" / "B"], calibracao=self.cal, clientes=cl, embedder=Emb(),
                          workers=4, **{**SILENCIO, **kw})

    def test_fluxo_regua_auditor_saturacao_e_retomada(self):
        from pipeline.qa_research.experimento_ab.v22 import regua
        f = FalsoV22()
        self.assertEqual(self.g(f).run(), 0)
        d = self.exp / "bracos" / "B_v22"
        self.assertNotIn("meta_relacoes", f.tags)                 # inventário reaproveitado de B
        res = read_json(d / "resultado.json")
        _, bs = blocos(ITEM, self.exp / "docs" / "refinado")
        pares = {b["indice"] for b in bs if int(hashlib.md5(b["texto"].encode()).hexdigest(), 16) % 2 == 0}
        t = res["por_origem"]["janela"]
        self.assertEqual(t["reprovadas_regua"], len(bs))          # a longa de cada foco, só ela
        self.assertEqual(t["falhas_auditor"].get("atalho"), len(bs))
        self.assertEqual(t["finais"], len(bs) + len(pares))       # 1 boa por foco + 1 na 2ª visita dos pares
        vis = {int(k.split(":")[1]): v["visitas"] for k, v in res["saturacao"]["focos"].items()}
        self.assertEqual(vis, {i: (3 if i in pares else 2) for i in range(len(bs))})
        self.assertGreater(res["chamadas"]["vazias"], 0)
        comp = res["por_origem"]["composta"]
        self.assertGreater(comp["finais"], 0)
        # o prompt da 2ª visita traz os conhecimentos cobertos e as recusas do foco, com o motivo
        segunda = [u for u in f.usuarios_foco if "[recusada" in u][0]
        self.assertIn("conhecimento 1", segunda.split("<conhecimentos_cobertos>")[1])
        self.assertIn("recusada pela régua", segunda)
        self.assertIn("recusada (atalho)", segunda)
        aprov = C.linhas(d / "aprovadas.jsonl")
        self.assertTrue(all(len(q["resposta"].split()) <= 20 and q["explicacao"] for q in aprov))
        self.assertTrue((d / "geracao_concluida.json").exists())
        antes = f.chamadas
        self.assertEqual(self.g(f).run(), 0)
        self.assertEqual(f.chamadas, antes)
        # régua: questão sem fundamento literal de [F] é recusada sozinha
        q = {"tipo": "conceito", "cenario": False, "conhecimento": "c", "pergunta": "Qual é a função principal do componente x?",
             "resposta": "Separar fases.", "explicacao": "", "fundamentos": [{"bloco": "A1", "trecho": "texto do apoio"}]}
        self.assertTrue(regua(q, {"F": "texto do foco", "A1": "texto do apoio"}, ("conceito",), "F"))
        self.assertEqual(regua(q, {"F": "texto do foco", "A1": "texto do apoio"}, ("conceito",)), [])

    def test_segunda_chance_unica_para_foco_e_composta_recusados(self):
        f = FalsoSegundaChance()
        self.assertEqual(self.g(f).run(), 0)
        d = self.exp / "bracos" / "B_v22"
        res = read_json(d / "resultado.json")
        _, bs = blocos(ITEM, self.exp / "docs" / "refinado")
        n_cad = len(read_json(d / "topicos" / ITEM / "combinacoes.json")["combinacoes"])
        # foco: 1ª visita só recusas -> revisita; 2ª rende; 3ª só recusas -> fecha (sem nova segunda chance)
        vis = {int(k.split(":")[1]): v["visitas"] for k, v in res["saturacao"]["focos"].items()}
        self.assertEqual(vis, {i: 3 for i in range(len(bs))})
        self.assertEqual(res["segunda_chance"]["focos"], {"visitas": len(bs), "conhecimentos_novos": len(bs)})
        segunda = [u for u in f.usuarios_foco if "[recusada (atalho)" in u][0]
        self.assertIn("ATALHO", segunda.split("<questoes_deste_foco>")[1])
        # composta: 1ª tentativa recusada, 2ª recebe a anterior com o motivo e é aprovada; não há 3ª
        self.assertEqual(res["segunda_chance"]["compostas"], {"tentativas": n_cad, "finais": n_cad})
        t2 = [u for u in f.usuarios_composta if "<tentativa_anterior>" in u]
        self.assertEqual(len(t2), n_cad)
        self.assertIn("recusada (atalho)", t2[0].split("<tentativa_anterior>")[1])
        self.assertEqual(res["por_origem"]["composta"]["finais"], n_cad)
        antes = f.chamadas
        self.assertEqual(self.g(f).run(), 0)
        self.assertEqual(f.chamadas, antes)                       # retomada não refaz nada

    def test_falha_do_auditor_isolada_por_questao(self):
        f = FalsoV22(falhar_auditoria="alfa3 ")
        self.assertGreater(self.g(f).run(), 0)
        d = self.exp / "bracos" / "B_v22"
        self.assertFalse((d / "geracao_concluida.json").exists())
        self.assertGreater(len(list((d / "topicos" / ITEM / "auditoria_v22").glob("*.json"))), 5)
        f.falhar_auditoria = None
        self.assertEqual(self.g(f).run(), 0)
        self.assertTrue((d / "geracao_concluida.json").exists())

    def test_avaliacao_e_comparacao_do_v22(self):
        from pipeline.qa_research.experimento_ab import avaliacao as AV
        from pipeline.qa_research.experimento_ab.metricas import comparar
        from pipeline.qa_research.tests.test_benchmark_gap import Answer, Faith
        from pipeline.qa_research.tests.test_especialista_finalizacao import Juiz as JuizResp
        self.assertEqual(self.g(FalsoV22()).run(), 0)
        for nome in ("B", "B_v22"):
            st = AV.executar(self.exp / "bracos" / nome, self.exp / "avaliacao" / nome, workers=3, judge_workers=1,
                             clientes={"resp_gpt-4-1-nano": Answer(), "resp_gpt-4-1-mini": Answer(), "resp_gpt-4-1": Answer(),
                                       "juiz": JuizResp(), "faithfulness": Faith()}, progress=lambda *x, **k: None)
            self.assertEqual(st, 0)
        out = comparar(self.exp)
        self.assertIn("gerador v22: B_v22-B", out["efeitos"])
        self.assertIsNotNone(out["bracos"]["B_v22"]["acuracia"]["gpt-4-1"]["closedp"])
        self.assertIn("parcial = 0,5", (self.exp / "COMPARACAO.md").read_text(encoding="utf-8"))


class FalsoV23(FalsoV22):
    """Gerador v23 simulado: as questões da v22 com resposta padrão; a 1ª visita traz também uma de decisão."""
    def __init__(self, **kw):
        super().__init__(**kw)
        self.sistemas = []

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        if tag.startswith("v23_"):
            self.sistemas.append((tag, system))
            tag = "v22_" + tag[4:]
        return super().json(system, user, tag, max_tokens, validate, item)

    def _q(self, tipo, trecho, bloco, extra=""):
        q = super()._q(tipo, trecho, bloco, extra)
        return {**q, "resposta_padrao": f"Resposta atraente {self.n}.", "por_que_nao": "O conhecimento X a exclui."}

    def foco(self, user):
        d = super().foco(user)
        if len(d["questoes"]) == 3:     # 1ª visita: acrescenta uma de decisão (permitida nas janelas na v23)
            dec = self._q("decisao", d["questoes"][0]["fundamentos"][0]["trecho"], "F")
            dec["pergunta"] = f"Na situação {self.n} gama{self.n} delta{self.n}, que ajuste técnico deve ser aplicado ao sistema?"
            d["questoes"].append(dec)
        return d


class V23Tests(unittest.TestCase):
    def setUp(self):
        V22Tests.setUp(self)

    def g(self, f, **kw):
        from pipeline.qa_research.experimento_ab.v23 import GeracaoV23
        cl = {p: f for p in ("relacoes", "combinacoes", "geracao", "auditoria")}
        cl["dedup_juiz"] = NuncaRedundante()
        return GeracaoV23(self.exp / "bracos" / "B_v23", [ITEM], docs=self.exp / "docs" / "refinado", braco="B_v23",
                          reusar=[self.exp / "bracos" / "B"], calibracao=self.cal, clientes=cl, embedder=Emb(),
                          workers=4, **{**SILENCIO, **kw})

    def test_exemplos_fixos_trocam_o_mesmo_documento_e_limitam_externos(self):
        from pipeline.qa_research.experimento_ab.v23 import MAX_EXTERNOS, carregar_exemplos, selecionar_exemplos
        banco = carregar_exemplos()
        boas, ruins = selecionar_exemplos(banco, "03_03")
        ids = [e["id"] for e in boas]
        self.assertNotIn("03_03", {e["item"] for e in boas + ruins})
        self.assertEqual(len(boas), len(banco["boas"]))
        self.assertIn("R1", ids)          # procedimento do 03_03 trocado pela reserva de procedimento
        self.assertIn("R4", ids)          # diagnóstico do 03_03 trocado pela reserva de diagnóstico
        for item in ("02_02", "03_03", "07_01", "99_99"):
            b, _ = selecionar_exemplos(banco, item)
            self.assertLessEqual(sum(e.get("origem") == "dataset_mcq" for e in b), MAX_EXTERNOS)
        tipos = [e["tipo"] for e in banco["boas"]]
        self.assertGreaterEqual(tipos.count("decisao") + tipos.count("procedimento"), len(tipos) / 2)

    def test_regua_v23_exige_resposta_padrao_diferente(self):
        from pipeline.qa_research.experimento_ab.v23 import regua_v23
        q = {"tipo": "decisao", "cenario": True, "conhecimento": "c", "pergunta": "Na situação descrita com sinal alfa, que ajuste técnico deve ser feito no sistema?",
             "resposta": "Reduzir a vazão.", "explicacao": "Porque sim.", "resposta_padrao": "Reduzir a vazão.",
             "por_que_nao": "x", "fundamentos": [{"bloco": "F", "trecho": "texto do foco"}]}
        tipos = ("decisao",)
        self.assertTrue(any("resposta_padrao igual" in m for m in regua_v23(q, {"F": "texto do foco"}, tipos, "F")))
        q["resposta_padrao"] = "Aumentar a pressão."
        self.assertEqual(regua_v23(q, {"F": "texto do foco"}, tipos, "F"), [])
        del q["por_que_nao"]
        self.assertTrue(regua_v23(q, {"F": "texto do foco"}, tipos, "F")[0].startswith("use exatamente os campos"))

    def test_fluxo_v23_com_exemplos_no_sistema_e_decisao_no_foco(self):
        f = FalsoV23()
        self.assertEqual(self.g(f).run(), 0)
        d = self.exp / "bracos" / "B_v23"
        foco = [s for t, s in f.sistemas if t == "v23_foco"]
        self.assertTrue(foco and all("<questoes_boas>" in s and "<questoes_ruins>" in s for s in foco))
        self.assertTrue(all("Resposta padrão (errada aqui)" in s for s in foco))
        self.assertTrue(any(t == "v23_composta" and "<questoes_boas>" in s for t, s in f.sistemas))
        self.assertNotIn("<exemplos>", "".join(f.usuarios_foco))          # exemplos só no sistema
        aprov = C.linhas(d / "aprovadas.jsonl")
        self.assertTrue(aprov and all(q["resposta_padrao"] and q["por_que_nao"] for q in aprov))
        self.assertIn("decisao", {q["tipo"] for q in aprov if q["origem"] == "janela"})
        cfg = read_json(d / "config.json")
        self.assertEqual(cfg["schema"], "experimento-ab-geracao-v23")
        self.assertIn("exemplos_v23_sha256", cfg)
        antes = f.chamadas
        self.assertEqual(self.g(f).run(), 0)
        self.assertEqual(f.chamadas, antes)

    def test_painel_de_dificuldade_e_comparacao(self):
        from pipeline.qa_research.experimento_ab import avaliacao as AV
        from pipeline.qa_research.experimento_ab.metricas import comparar
        from pipeline.qa_research.experimento_ab.painel import estrato, executar as painel
        from pipeline.qa_research.tests.test_benchmark_gap import Answer, Faith
        from pipeline.qa_research.tests.test_especialista_finalizacao import Juiz as JuizResp
        self.assertEqual(self.g(FalsoV23()).run(), 0)
        for nome in ("B", "B_v23"):
            st = AV.executar(self.exp / "bracos" / nome, self.exp / "avaliacao" / nome, workers=3, judge_workers=1,
                             clientes={"resp_gpt-4-1-nano": Answer(), "resp_gpt-4-1-mini": Answer(), "resp_gpt-4-1": Answer(),
                                       "juiz": JuizResp(), "faithfulness": Faith()}, progress=lambda *x, **k: None)
            self.assertEqual(st, 0)
        aval = self.exp / "avaliacao" / "B_v23"
        st = painel(aval, workers=2, judge_workers=1, clientes={"resp_gpt-5-nano": Answer(), "resp_gpt-5-mini": Answer(), "resp_gpt-5": Answer(), "resp_gpt-5-4": Answer(),
                                                                "juiz": JuizResp()}, progress=lambda *x, **k: None)
        self.assertEqual(st, 0)
        res = read_json(aval / "painel" / "resumo.json")
        self.assertEqual(res["n"], len(C.linhas(self.exp / "bracos" / "B_v23" / "aprovadas.jsonl")))
        self.assertEqual(sum(res["estratos"].values()), res["n"])
        self.assertEqual(estrato({"a": "correta", "gpt-5": "parcial", "gpt-5-4": "correta"}), "dificil")
        self.assertEqual(estrato({"a": "incorreta", "gpt-5": "parcial", "gpt-5-4": "correta"}), "muito_dificil")
        self.assertEqual(estrato({"a": "correta", "gpt-5": "correta", "gpt-5-4": "incorreta"}), "facil")
        self.assertEqual(estrato({"a": "parcial", "gpt-5": "correta"}), "media")
        out = comparar(self.exp)
        self.assertIn("gerador v23: B_v23-B", out["efeitos"])
        self.assertIsNotNone(out["bracos"]["B_v23"]["painel"])
        md = (self.exp / "COMPARACAO.md").read_text(encoding="utf-8")
        self.assertIn("Painel sem contexto", md)
        self.assertIn("Decisão + procedimento", md)


class FiltroAntigoTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)

    def test_encurta_audita_e_retoma(self):
        from pipeline.qa_research.experimento_ab.antigo import FiltroAntigo
        gap = self.tmp / "gap"
        gap.mkdir()
        qs = [{"uid": f"01_01:j:r1:00{k}:1", "item": "01_01", "tipo": "diagnostico", "origem": "janela", "foco": k,
               "pergunta": f"Pergunta {k} sobre o sinal {k}?", "resposta": f"Causa {k}, porque o bloco explica longamente."}
              for k in range(3)]
        C.gravar_jsonl(self.tmp / "aprovadas.jsonl", qs)
        C.gravar_jsonl(gap / "faithfulness.jsonl", [{"uid": q["uid"], "status": s} for q, s in
                                                    zip(qs, ("totalmente_sustentado", "totalmente_sustentado", "suporte_insuficiente"))])
        C.gravar_jsonl(gap / "contextos.jsonl", [{"uid": q["uid"], "blocos_contexto": [{"id": "B1", "texto": "texto"}]} for q in qs])

        class Encurtar:
            chamadas = 0

            def json(self, system, user, validate=None, **kw):
                Encurtar.chamadas += 1
                d = json.loads(user)
                out = {"resposta": d["resposta_referencia"].split(",")[0] + ".", "explicacao": "Porque o bloco explica."}
                validate(out)
                return out

        class Auditor:
            chamadas = 0

            def json(self, system, user, validate=None, **kw):
                Auditor.chamadas += 1
                d = json.loads(user)
                ok = "Causa 0" in d["resposta_referencia"]
                out = {"sem_documento": True, "resposta_alternativa": "outra", "alternativa_excluida": True,
                       "atalho": not ok, "sustentada": True, "elemento_unico": True, "tipo_sugerido": "diagnostico",
                       "justificativa": "j"}
                validate(out)
                return out

        f = lambda: FiltroAntigo(self.tmp / "saida", fonte=self.tmp / "aprovadas.jsonl", gap=gap,  # noqa: E731
                                 clientes={"encurtar": Encurtar(), "auditoria": Auditor()}, workers=2, **SILENCIO)
        self.assertEqual(f().run(), 0)
        aprov = C.linhas(self.tmp / "saida" / "aprovadas.jsonl")
        self.assertEqual([q["uid"] for q in aprov], [qs[0]["uid"]])
        self.assertEqual(aprov[0]["resposta"], "Causa 0.")
        self.assertIn("porque", aprov[0]["resposta_original"])
        self.assertEqual(aprov[0]["foco"], 0)                  # vínculo de contexto preservado para o benchmark_gap
        res = read_json(self.tmp / "saida" / "resultado.json")
        self.assertEqual((res["sustentadas"], res["auditadas"], res["aprovadas"]), (2, 2, 1))
        antes = (Encurtar.chamadas, Auditor.chamadas)
        self.assertEqual(f().run(), 0)
        self.assertEqual((Encurtar.chamadas, Auditor.chamadas), antes)


class TravaTests(unittest.TestCase):
    def test_segunda_execucao_no_mesmo_braco_e_recusada(self):
        from pipeline.qa_research.experimento_ab.__main__ import _trava
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        with _trava(tmp, "B_v23"):
            with self.assertRaises(SystemExit):
                with _trava(tmp, "B_v23"):
                    pass
            with _trava(tmp, "B"):     # outro braço não é bloqueado
                pass


class CLIV23Tests(unittest.TestCase):
    def test_comandos_v23_painel_e_antigo_pela_cli(self):
        from unittest.mock import patch
        from pipeline.qa_research.experimento_ab import __main__ as M
        from pipeline.qa_research.experimento_ab import antigo as AN
        from pipeline.qa_research.experimento_ab import painel as PA
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        exp = tmp / "exp"
        atual, juiz = {"f": Falso()}, NuncaRedundante()      # v21 para o braço B; v23 depois

        def fabrica(model, effort, cache_path, *a, **kw):
            return juiz if Path(cache_path).stem == "dedup_juiz" else atual["f"]

        chamadas = []
        with patch.object(C, "ITENS", (ITEM,)), patch("pipeline.inventario.llm.LLMClient", fabrica), \
                patch.object(C, "embedder", lambda *a, **k: Emb()), \
                patch.object(PA, "executar", lambda aval, **kw: chamadas.append(("painel", Path(aval))) or 0), \
                patch.object(AN.FiltroAntigo, "run", lambda self: chamadas.append(("antigo", self.workers)) or 0), \
                patch.object(AN, "avaliar", lambda **kw: chamadas.append(("avaliar-antigo", kw["workers"])) or 0):
            self.assertEqual(M.main(["preparar", "--experimento", str(exp)]), 0)
            calibracao_falsa(exp / "calibracao", auto=1.01)
            with self.assertRaises(SystemExit):
                M.main(["v23", "--braco", "B", "--experimento", str(exp)])          # exige o inventário de B
            self.assertEqual(M.main(["gerar", "--braco", "B", "--experimento", str(exp), "--workers", "3"]), 0)
            atual["f"] = FalsoV23()
            self.assertEqual(M.main(["v23", "--braco", "B", "--experimento", str(exp), "--workers", "3"]), 0)
            self.assertTrue((exp / "bracos" / "B_v23" / "geracao_concluida.json").exists())
            with self.assertRaises(SystemExit):
                M.main(["v23", "--braco", "B_v22", "--experimento", str(exp)])     # só a partir do braço de origem
            self.assertEqual(M.main(["painel", "--braco", "B_v23", "--experimento", str(exp)]), 0)
            self.assertEqual(M.main(["painel", "--avaliacao", "pipeline/qa_research/relatorios/x",
                                     "--experimento", str(exp)]), 0)
            self.assertEqual(M.main(["antigo", "--experimento", str(exp), "--workers", "16"]), 0)
            self.assertEqual(M.main(["avaliar-antigo", "--experimento", str(exp), "--workers", "5"]), 0)
        self.assertEqual(chamadas, [("painel", exp / "avaliacao" / "B_v23"),
                                    ("painel", C.ROOT / "pipeline/qa_research/relatorios/x"),
                                    ("antigo", 16), ("avaliar-antigo", 5)])


class DatasetFinalTests(unittest.TestCase):
    def test_monta_exclui_deduplica_avalia_e_relata(self):
        from pipeline.qa_research.experimento_ab.final import DatasetFinal
        from pipeline.qa_research.tests.test_benchmark_gap import Answer, Faith
        from pipeline.qa_research.tests.test_especialista_finalizacao import Juiz as JuizResp
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        exp = tmp / "exp"
        C.preparar_documentos(exp, itens=[ITEM])
        cal = calibracao_falsa(exp / "calibracao", auto=0.97)
        docs = exp / "docs" / "refinado"

        def q(k, pergunta, resposta, tipo="diagnostico"):
            return {"uid": f"{ITEM}:j:r1:{k:03d}:1", "item": ITEM, "tipo": tipo, "cenario": True, "composicao": "simples",
                    "origem": "janela", "foco": k, "pergunta": pergunta, "resposta": resposta}

        nova = [q(0, "Após trocar o filtro, a pressão cai e a vazão some. Qual a causa?", "Entupimento do elemento."),
                q(1, "Por que o certificado do fabricante não basta para liberar o equipamento?", "Falta ensaio em campo.")]
        velha = [q(0, "Após trocar o filtro, a pressão cai e a vazão some. Qual a causa?", "Entupimento do elemento."),
                 q(2, "Qual técnica acompanha a perda metálica ao longo do tempo com leitura contínua?", "Sonda de resistência elétrica.", "procedimento"),
                 q(3, "Qual ajuste estabiliza a interface do separador em mar severo?", "Ganho menor no controle de nível.", "decisao")]
        fontes_ = []
        for nome, qs, marcador in (("v22", nova, "geracao_concluida.json"), ("antigo", velha, "filtro_concluido.json")):
            pasta = tmp / nome
            C.gravar_jsonl(pasta / "aprovadas.jsonl", qs)
            (pasta / marcador).write_text("{}", encoding="utf-8")
            fontes_.append({"nome": nome, "pasta": pasta, "marcador": marcador, "docs": docs, "obrigatoria": True})
        excl = tmp / "exclusoes.json"
        excl.write_text(json.dumps({"exclusoes": {f"antigo:{ITEM}:j:r1:003:1": "teste"}}), encoding="utf-8")
        d = DatasetFinal(tmp / "final", exp=exp, fontes_=fontes_, calibracao=cal, exclusoes=excl, embedder=Emb(),
                         juiz=NuncaRedundante(), **SILENCIO)
        self.assertEqual(d.montar(), 0)
        ds = C.linhas(tmp / "final" / "dataset.jsonl")
        uids = {x["uid"] for x in ds}
        self.assertEqual(uids, {f"v22:{ITEM}:j:r1:000:1", f"v22:{ITEM}:j:r1:001:1", f"antigo:{ITEM}:j:r1:002:1"})
        m = read_json(tmp / "final" / "montagem.json")
        self.assertEqual(m["por_fonte"]["antigo"], {"reunidas": 3, "excluidas": 1, "redundantes": 1, "finais": 1})
        self.assertEqual(m["sinalizadas_para_revisao"], [f"v22:{ITEM}:j:r1:001:1"])     # flagrada, não excluída
        self.assertTrue(all(x["contexto_tecnico"] and x["blocos_contexto"] for x in ds))
        cl = {"resp_gpt-4-1-nano": Answer(), "resp_gpt-4-1-mini": Answer(), "resp_gpt-4-1": Answer(),
              "juiz": JuizResp(), "faithfulness": Faith()}
        self.assertEqual(d.avaliar(workers=2, judge_workers=1, clientes=cl), 0)
        self.assertEqual(d.painel(workers=2, judge_workers=1, clientes={"resp_gpt-5-nano": Answer(), "resp_gpt-5-mini": Answer(), "resp_gpt-5": Answer(), "resp_gpt-5-4": Answer(),
                                                                       "juiz": JuizResp()}), 0)
        res = d.relatorio()
        self.assertEqual(res["n"], 3)
        self.assertIsNotNone(res["sustentados"])
        self.assertIn("gpt-4-1", res["acuracia"])
        self.assertEqual(res["painel"]["n"], 3)
        md = (tmp / "final" / "QUALIDADE.md").read_text(encoding="utf-8")
        self.assertIn("| Dificuldade | GPT-5 sem contexto (modelo forte independente) | ↓ |", md)
        # experimento do limite de palavras sobre o dataset final avaliado
        from pipeline.qa_research.experimento_ab import limite as LI
        cl_lim = {f"resp_{m}": Answer() for m in LI.MODELOS} | {"juiz": JuizResp()}
        self.assertEqual(LI.executar(tmp / "final", limite=20, n=3, workers=2, judge_workers=1, clientes=cl_lim,
                                     **SILENCIO), 0)
        comp = read_json(tmp / "final" / "limite_20" / "comparacao.json")
        self.assertEqual(comp["n_amostra"], 3)
        self.assertIn("20", comp["modelos"]["gpt-4-1"])
        self.assertIn("100", comp["modelos"]["gpt-4-1"])
        self.assertIn("diferenca_acuracia", comp["modelos"]["gpt-5"])
        self.assertIn("AUC F1 x juiz", (tmp / "final" / "limite_20" / "LIMITE.md").read_text(encoding="utf-8"))
        self.assertAlmostEqual(LI.f1("redução da repulsão elétrica", "redução da repulsão elétrica entre as gotas")[0], 0.75)
        self.assertAlmostEqual(LI.rouge_l("a válvula abriu tarde por atraso no alívio",
                                          "a válvula de alívio abriu com atraso"), 2 * (3 / 5) * (3 / 4) / (3 / 5 + 3 / 4))   # sem stopwords
        self.assertEqual(d.montar(), 0)                                # retomada: mesmas decisões, mesmo dataset
        excl.write_text(json.dumps({"exclusoes": {}}), encoding="utf-8")
        d2 = DatasetFinal(tmp / "final", exp=exp, fontes_=fontes_, calibracao=cal, exclusoes=excl, embedder=Emb(),
                          juiz=NuncaRedundante(), **SILENCIO)
        with self.assertRaises(ValueError):                            # dataset mudou depois de avaliado
            d2.montar()


class DedupBloqueioTests(unittest.TestCase):
    def test_bloqueio_do_juiz_vira_decisao_nova_registrada(self):
        from pipeline.inventario.llm import ContentFiltered
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)

        class Bloqueia:
            def json(self, *a, **k):
                raise ContentFiltered("bloqueio simulado")

        emb = Emb()
        dd = D.DedupIncremental(tmp, emb, np.zeros(64), limiar_auto=1.01, limiar_juiz=-1.0, juiz=Bloqueia(),
                                progress=lambda *a, **k: None)
        qs = [{"uid": f"x:{k}", "pergunta": "Qual a causa da queda de pressão no filtro?", "resposta": f"Entupimento {k}."}
              for k in range(2)]
        self.assertEqual(dd.processar("01_01", qs), 0)
        self.assertEqual(read_json(tmp / "01_01" / "x_1.json")["via"], "bloqueio_juiz")
        self.assertEqual(dd.redundantes("01_01"), {})


class CompletoTests(unittest.TestCase):
    def test_gerador_completo_usa_inventario_de_outubro_e_fontes_na_ordem(self):
        from pipeline.qa_research.experimento_ab import completo as CO
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        exp = tmp / "exp"
        C.preparar_documentos(exp, itens=[ITEM])
        calibracao_falsa(exp / "calibracao", auto=0.97)
        origem = tmp / "outubro"
        (origem / "topicos" / ITEM).mkdir(parents=True)
        (origem / "config.json").write_text(json.dumps({"itens": ["01_01", ITEM, "02_02"]}), encoding="utf-8")
        self.assertEqual(CO.itens_completos(origem), ["01_01"])          # os 3 do experimento ficam com o B_v23
        with self.assertRaises(ValueError):
            CO.gerador(exp, itens=[ITEM], origem=origem, saida=tmp / "g", docs=exp / "docs" / "antigo", **SILENCIO)
        (origem / "topicos" / ITEM / "combinacoes.json").write_text("{}", encoding="utf-8")
        g = CO.gerador(exp, itens=[ITEM], origem=origem, saida=tmp / "g", docs=exp / "docs" / "antigo",
                       docs_simultaneos=2, embedder=Emb(), **SILENCIO)
        self.assertEqual((g.VERSAO, g.reusar, g.docs_simultaneos), ("v23", [origem], 2))
        self.assertEqual([f["nome"] for f in CO.fontes_v2(exp, tmp / "g")], ["v23", "v23c", "v22", "antigo", "conceitos", "variada", "tipo_decisao", "tipo_diagnostico",
                          "tipo_procedimento"])
        self.assertEqual([f["obrigatoria"] for f in CO.fontes_v2(exp, tmp / "g")], [True] * 6 + [False] * 3)

    def test_dataset_v2_filtra_sustentacao_avalia_com_contexto_e_relata(self):
        from pipeline.qa_research.experimento_ab import completo as CO
        from pipeline.qa_research.tests.test_benchmark_gap import Answer, Faith
        from pipeline.qa_research.tests.test_especialista_finalizacao import Juiz as JuizResp
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        exp = tmp / "exp"
        C.preparar_documentos(exp, itens=[ITEM])
        cal = calibracao_falsa(exp / "calibracao", auto=0.97)
        docs = exp / "docs" / "refinado"

        def q(k, pergunta, resposta, tipo="diagnostico"):
            return {"uid": f"{ITEM}:j:r1:{k:03d}:1", "item": ITEM, "tipo": tipo, "cenario": True, "composicao": "simples",
                    "origem": "janela", "foco": k, "pergunta": pergunta, "resposta": resposta}

        fontes_ = []
        for nome, qs in (("v23", [q(0, "Após trocar o filtro, a pressão cai e a vazão some. Qual a causa?", "Entupimento do elemento.")]),
                         ("v23c", [q(1, "Qual ajuste estabiliza a interface do separador em mar severo?", "Ganho menor no controle de nível.", "decisao"),
                                   q(2, "Qual técnica acompanha a perda metálica com leitura contínua?", "SEM SUPORTE", "procedimento")])):
            pasta = tmp / nome
            C.gravar_jsonl(pasta / "aprovadas.jsonl", qs)
            (pasta / "geracao_concluida.json").write_text("{}", encoding="utf-8")
            fontes_.append({"nome": nome, "pasta": pasta, "marcador": "geracao_concluida.json", "docs": docs,
                            "obrigatoria": True})
        v1 = tmp / "v1"                                # auditoria do v1 reaproveitada para a mesma questão
        uid0 = f"v23:{ITEM}:j:r1:000:1"
        (v1 / "faithfulness").mkdir(parents=True)
        (v1 / "faithfulness" / (CO._nome_arq(uid0) + ".json")).write_text(json.dumps(
            {"uid": uid0, "avaliacao": {}, "status": "totalmente_sustentado", "afirmacoes": 1, "sustentada": 1,
             "contradita": 0, "insuficiente": 0, "fracao_sustentada": 1.0}), encoding="utf-8")

        class FaithParcial(Faith):
            def json(self, system, user, validate=None, **kw):
                d = super().json(system, user, validate=validate, **kw)
                if "SEM SUPORTE" in json.loads(user)["gabarito"]:
                    d["afirmacoes"][0]["veredito"] = "insuficiente"
                    d["afirmacoes"][0]["evidencias"] = []
                return d

        excl = tmp / "exclusoes.json"
        excl.write_text(json.dumps({"exclusoes": {}}), encoding="utf-8")
        modelos = {"gpt-4-1": "gpt-4-1-petrobras", "gpt-5": "gpt-5-petrobras:low", "gpt-5-4": "gpt-5-4-petrobras:low"}
        d = CO.DatasetCompleto(tmp / "final", exp=exp, fontes_=fontes_, calibracao=cal, exclusoes=excl, embedder=Emb(),
                               juiz=NuncaRedundante(), modelos=modelos, v1=v1, **SILENCIO)
        self.assertEqual(d.montar(), 0)
        self.assertEqual(len(C.linhas(tmp / "final" / "candidatos.jsonl")), 3)
        faith = FaithParcial()
        self.assertEqual(d.sustentar(workers=2, clientes={"faithfulness": faith}), 0)
        self.assertEqual(faith.calls, 2)                                   # a do v1 não é paga de novo
        ds = C.linhas(tmp / "final" / "dataset.jsonl")
        self.assertEqual({x["uid"] for x in ds}, {uid0, f"v23c:{ITEM}:j:r1:001:1"})
        resp = {f"resp_{m}": Answer() for m in modelos}
        self.assertEqual(d.avaliar(workers=2, judge_workers=1, clientes=resp | {"juiz": JuizResp()}), 0)
        contextos = [p["contexto"] for p in resp["resp_gpt-5"].payloads]
        self.assertEqual(sum(c is None for c in contextos), 3)             # sondagem + 2 sem contexto
        self.assertEqual(sum(bool(c) for c in contextos), 2)
        self.assertEqual(read_json(tmp / "final" / "config.json")["limite_palavras"], 20)
        res = d.relatorio()
        self.assertEqual(res["n"], 2)
        self.assertEqual(set(res["modelos"]), set(modelos))
        self.assertIn("f1", res["modelos"]["gpt-5"]["sem"])
        self.assertIsNotNone(res["estratos_pct"])
        md = (tmp / "final" / "QUALIDADE.md").read_text(encoding="utf-8")
        self.assertIn("| GPT-5.4 (referência) |", md)
        self.assertIn("2 de 3 candidatas", md)
        pares = tmp / "final" / "pares.csv"                 # resposta de modelo com NUL não derruba o relatório
        pares.write_text(pares.read_text(encoding="utf-8-sig").replace("gpt-5-4,", "gpt-5-4,\0", 1), encoding="utf-8-sig")
        self.assertEqual(d.relatorio()["n"], 2)
        # fonte nova depois da avaliação: as questões antigas continuam avaliadas e só a nova é paga
        nova = tmp / "nova"
        C.gravar_jsonl(nova / "aprovadas.jsonl", [q(5, "Que propriedade do MEG reduz sua perda para a corrente gasosa?",
                                                    "Baixa volatilidade.", "conceito")])
        (nova / "geracao_concluida.json").write_text("{}", encoding="utf-8")
        fontes_.append({"nome": "nova", "pasta": nova, "marcador": "geracao_concluida.json", "docs": docs,
                        "obrigatoria": True})
        d2 = CO.DatasetCompleto(tmp / "final", exp=exp, fontes_=fontes_, calibracao=cal, exclusoes=excl, embedder=Emb(),
                                juiz=NuncaRedundante(), modelos=modelos, v1=v1, **SILENCIO)
        self.assertEqual(d2.montar(), 0)
        self.assertEqual(d2.sustentar(workers=2, clientes={"faithfulness": faith}), 0)
        self.assertEqual(faith.calls, 3)
        antes = len(resp["resp_gpt-5"].payloads)
        self.assertEqual(d2.avaliar(workers=2, judge_workers=1, clientes=resp | {"juiz": JuizResp()}), 0)
        self.assertEqual(len([p for p in resp["resp_gpt-5"].payloads[antes:] if "MEG" in p["pergunta"]]), 2)
        self.assertFalse([p for p in resp["resp_gpt-5"].payloads[antes:] if "filtro" in p["pergunta"]])
        self.assertEqual(d2.relatorio()["n"], 3)
        # um modelo sai da avaliação: não responde mais, e os demais não são repetidos
        menos = {k: v for k, v in modelos.items() if k != "gpt-4-1"}
        d3 = CO.DatasetCompleto(tmp / "final", exp=exp, fontes_=fontes_, calibracao=cal, exclusoes=excl, embedder=Emb(),
                                juiz=NuncaRedundante(), modelos=menos, v1=v1, **SILENCIO)
        n41, n5 = len(resp["resp_gpt-4-1"].payloads), len(resp["resp_gpt-5"].payloads)
        self.assertEqual(d3.avaliar(workers=2, judge_workers=1, clientes=resp | {"juiz": JuizResp()}), 0)
        self.assertEqual(len(resp["resp_gpt-4-1"].payloads), n41)
        self.assertLessEqual(len(resp["resp_gpt-5"].payloads) - n5, 1)       # no máximo a sondagem
        self.assertEqual(set(d3.relatorio()["modelos"]), set(menos))
        with self.assertRaises(ValueError):                                 # versão diferente de um modelo comum
            CO.DatasetCompleto(tmp / "final", exp=exp, fontes_=fontes_, calibracao=cal, exclusoes=excl, embedder=Emb(),
                               juiz=NuncaRedundante(), modelos={**menos, "gpt-5": "gpt-5-petrobras:high"}, v1=v1,
                               **SILENCIO).avaliar(workers=2, judge_workers=1, clientes=resp | {"juiz": JuizResp()})


class FalsoConceito(FalsoV22):
    """Gerador de conceitos simulado: reaproveita as respostas da v22 e registra os prompts de sistema."""
    def __init__(self, **kw):
        super().__init__(**kw)
        self.sistemas = []

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        if tag.startswith("v23conceito_"):
            self.sistemas.append((tag, system))
            tag = "v22_" + tag[len("v23conceito_"):]
        return super().json(system, user, tag, max_tokens, validate, item)

    def _q(self, tipo, trecho, bloco, extra=""):
        q = super()._q(tipo, trecho, bloco, extra)
        return {**q, "resposta_padrao": f"Termo vizinho {self.n}.", "por_que_nao": "O traço X o exclui."}


class ConceitoTests(unittest.TestCase):
    def setUp(self):
        V22Tests.setUp(self)

    def g(self, f, **kw):
        from pipeline.qa_research.experimento_ab.conceito import GeracaoConceito
        cl = {p: f for p in ("relacoes", "combinacoes", "geracao", "auditoria")}
        cl["dedup_juiz"] = NuncaRedundante()
        return GeracaoConceito(self.exp / "conceitos", [ITEM], docs=self.exp / "docs" / "antigo", braco="conceitos",
                               calibracao=self.cal, clientes=cl, embedder=Emb(), workers=4, **{**SILENCIO, **kw})

    def test_gera_so_conceitos_sem_compostas_nem_inventario(self):
        f = FalsoConceito()
        self.assertEqual(self.g(f).run(), 0)
        d = self.exp / "conceitos"
        self.assertFalse({"meta_relacoes", "meta_combinacoes"} & set(f.tags))
        self.assertFalse(any("composta" in t for t in f.tags))
        aprov = C.linhas(d / "aprovadas.jsonl")
        self.assertTrue(aprov and {q["tipo"] for q in aprov} == {"conceito"} and {q["origem"] for q in aprov} == {"janela"})
        foco = [s for t, s in f.sistemas if t == "v23conceito_foco"]
        self.assertTrue(foco and all("nomeação" in s and "Stress-joint" in s and "<questoes_ruins>" in s for s in foco))
        aud = [s for t, s in f.sistemas if t == "v23conceito_auditoria"]
        self.assertTrue(aud and "vocabulário técnico" in aud[0])
        self.assertEqual(read_json(d / "config.json")["schema"], "experimento-ab-geracao-v23conceito")
        self.assertTrue((d / "geracao_concluida.json").exists())
        antes = f.chamadas
        self.assertEqual(self.g(f).run(), 0)
        self.assertEqual(f.chamadas, antes)

    def test_regua_aceita_so_termo_curto_de_conceito(self):
        g = self.g(FalsoConceito())
        q = {"tipo": "conceito", "cenario": False, "conhecimento": "nome de x",
             "pergunta": "Qual peça reduz a descontinuidade de rigidez no topo de um riser rígido?",
             "resposta": "Stress-joint.", "explicacao": "O bloco afirma.", "resposta_padrao": "Bend stiffener.",
             "por_que_nao": "É de riser flexível.", "fundamentos": [{"bloco": "F", "trecho": "texto do foco"}]}
        textos = {"F": "texto do foco"}
        self.assertEqual(g.regua(q, textos, g.TIPOS_FOCO, "F"), [])
        self.assertTrue(any("6 palavras" in m for m in g.regua({**q, "resposta": "uma duas tres quatro cinco seis sete"},
                                                              textos, g.TIPOS_FOCO, "F")))
        self.assertTrue(any("tipo deve ser" in m for m in g.regua({**q, "tipo": "mecanismo"}, textos, g.TIPOS_FOCO, "F")))
        cen = {**q, "cenario": True, "pergunta": "Num certificado com k informado, a equipe propõe somar o valor de ±U à "
                                               "indicação para compensar um desvio persistente observado em campo. Que "
                                               "grandeza do certificado está sendo usada indevidamente nessa proposta?"}
        self.assertEqual(g.regua(cen, textos, g.TIPOS_FOCO, "F"), [])      # cenário curto é permitido
        self.assertTrue(g.regua({**cen, "pergunta": cen["pergunta"] + " palavra" * 20}, textos, g.TIPOS_FOCO, "F"))

    def test_exemplos_de_conceito_validos_e_sem_o_mesmo_documento(self):
        from pipeline.qa_research.experimento_ab.conceito import EXEMPLOS_CONCEITO
        from pipeline.qa_research.experimento_ab.v23 import carregar_exemplos, selecionar_exemplos
        banco = carregar_exemplos(EXEMPLOS_CONCEITO)
        self.assertTrue(all(len(e["resposta"].split()) <= 6 for e in banco["boas"] + banco["reservas"]))
        for item in ("04_01", "07_01", "02_10"):
            boas, ruins = selecionar_exemplos(banco, item)
            self.assertNotIn(item, {e["item"] for e in boas + ruins})
            self.assertEqual(len(boas), len(banco["boas"]))


class FalsoVariada(FalsoConceito):
    """Gerador variado simulado: uma questão de conceito nova por visita, até a 4ª."""
    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        if tag.startswith("v23var_"):
            self.sistemas.append((tag, system))
            tag = "v22_" + tag[len("v23var_"):]
        return super().json(system, user, tag, max_tokens, validate, item)

    def foco(self, user):
        self.usuarios_foco.append(user)
        f = re.search(r"\[F\] [^\n]*\n(.+?)(?:\n\n\[A\d+\]|\n</janela>)", user, re.S).group(1)
        return {"motivo": "", "questoes": [self._q("conceito", " ".join(f.split()[:8]), "F")]}


class VariadaTests(unittest.TestCase):
    def setUp(self):
        V22Tests.setUp(self)
        self.ext = self.exp / "externos.jsonl"
        C.gravar_jsonl(self.ext, [{"id": f"{src}:{k}", "source": src, "question": f"Pergunta externa {src} {k}?",
                                   "answer": f"Resposta {k}."} for src in ("pira_ptbr", "mmmlu_ptbr", "arc_challenge", "qasc")
                                  for k in range(5)])
        self.conv = self.exp / "convertidas.jsonl"
        C.gravar_jsonl(self.conv, [{"uid": f"especialista_revisada:{k:04d}", "item": "05_02" if k % 3 else ITEM,
                                    "tipo": ("mecanismo", "decisao")[k % 2], "pergunta": f"Pergunta convertida {k}?",
                                    "resposta": "Curta." if k < 20 else " ".join(["longa"] * 20), "aprovada": True}
                                   for k in range(24)])

    def g(self, f, **kw):
        from pipeline.qa_research.experimento_ab.variada import GeracaoVariada
        cl = {p: f for p in ("relacoes", "combinacoes", "geracao", "auditoria")}
        cl["dedup_juiz"] = NuncaRedundante()
        return GeracaoVariada(self.exp / "variada", [ITEM], docs=self.exp / "docs" / "antigo", braco="variada",
                              calibracao=self.cal, clientes=cl, embedder=Emb(), workers=4,
                              **{**SILENCIO, "externos": self.ext, "convertidas": self.conv, **kw})

    def test_externos_nas_tres_primeiras_visitas_e_convertidas_na_quarta(self):
        f = FalsoVariada()
        self.assertEqual(self.g(f).run(), 0)
        d = self.exp / "variada"
        _, bs = blocos(ITEM, self.exp / "docs" / "antigo")
        vis = {int(k.split(":")[1]): v["visitas"] for k, v in read_json(d / "resultado.json")["saturacao"]["focos"].items()}
        self.assertEqual(set(vis.values()), {4})                   # 4 visitas mesmo sem saturar; nunca uma 5ª
        por_visita = {}
        for u in f.usuarios_foco:
            ex = u.split("<exemplos_de_forma>")[1].split("</exemplos_de_forma>")[0]
            n = len([x for x in f.usuarios_foco if x.split("<janela>")[1] == u.split("<janela>")[1] and
                     f.usuarios_foco.index(x) <= f.usuarios_foco.index(u)])
            por_visita.setdefault(n, []).append(ex)
        for n in (1, 2, 3):
            self.assertTrue(all("Pergunta externa" in ex and ex.count("Pergunta:") == 8 for ex in por_visita[n]))
        self.assertTrue(all("Pergunta convertida" in ex and "Pergunta externa" not in ex and "longa" not in ex
                            and ex.count("Pergunta:") == 6 for ex in por_visita[4]))
        self.assertNotEqual(por_visita[1][0], por_visita[2][0])      # exemplos mudam a cada visita
        foco = [s for t, s in f.sistemas if t == "v23var_foco"]
        self.assertTrue(foco and all("<questoes_ruins>" in s and "<questoes_boas>" not in s for s in foco))
        self.assertTrue(any(t == "v23var_auditoria" for t, _ in f.sistemas))
        aprov = C.linhas(d / "aprovadas.jsonl")
        self.assertTrue(aprov and {q["origem"] for q in aprov} == {"janela"})
        cfg = read_json(d / "config.json")
        self.assertEqual((cfg["schema"], cfg["saturacao"]["max_rodadas"]), ("experimento-ab-geracao-v23var", 4))
        antes = f.chamadas
        self.assertEqual(self.g(f).run(), 0)
        self.assertEqual(f.chamadas, antes)

    def test_convertidas_de_outros_documentos_e_tipos_da_geracao(self):
        from pipeline.qa_research.experimento_ab.variada import carregar_convertidas, sortear_convertidas
        banco = carregar_convertidas(self.conv)
        self.assertEqual(len(banco), 20)                              # gabarito longo fica fora
        esc = sortear_convertidas(banco, ITEM, 3, ("conceito", "mecanismo", "consequencia"))
        self.assertTrue(all(q["item"] != ITEM for q in esc))

    def test_sem_externos_falha_com_instrucao(self):
        with self.assertRaises(ValueError) as cm:
            self.g(FalsoVariada(), externos=self.exp / "nao_existe.jsonl")
        self.assertIn("preparar_exemplos", str(cm.exception))


class FalsoTipo(FalsoVariada):
    tipo = "diagnostico"

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        if tag.startswith("v23tipo_"):
            self.sistemas.append((tag, system))
            tag = "v22_" + tag[len("v23tipo_"):]
        return super().json(system, user, tag, max_tokens, validate, item)

    def foco(self, user):
        d = super().foco(user)
        for q in d["questoes"]:
            q.update(tipo=self.tipo, cenario=True,
                     pergunta="A vazão caiu e a pressão a montante subiu sem mudança de abertura. Qual a causa provável?")
        return d


class TipoUnicoTests(VariadaTests):
    def gt(self, f, tipo="diagnostico", **kw):
        from pipeline.qa_research.experimento_ab.tipo_unico import GeracaoTipo
        cl = {p: f for p in ("relacoes", "combinacoes", "geracao", "auditoria")}
        cl["dedup_juiz"] = NuncaRedundante()
        return GeracaoTipo(self.exp / f"tipo_{tipo}", [ITEM], tipo=tipo, docs=self.exp / "docs" / "antigo",
                           braco=f"tipo_{tipo}", calibracao=self.cal, clientes=cl, embedder=Emb(), workers=4,
                           **{**SILENCIO, "externos": self.ext, "convertidas": self.conv, **kw})

    def test_gera_so_o_tipo_pedido_com_definicao_no_prompt(self):
        f = FalsoTipo()
        self.assertEqual(self.gt(f).run(), 0)
        d = self.exp / "tipo_diagnostico"
        foco = [s for t, s in f.sistemas if t == "v23tipo_foco"]
        self.assertTrue(foco and all("<<" not in s and "`diagnostico`" in s and "causa primária" in s for s in foco))
        aprov = C.linhas(d / "aprovadas.jsonl")
        self.assertTrue(aprov and {q["tipo"] for q in aprov} == {"diagnostico"})
        self.assertEqual(read_json(d / "config.json")["tipo"], "diagnostico")
        with self.assertRaises(ValueError):
            self.gt(FalsoTipo(), tipo="conceito")

    def test_outro_tipo_e_recusado_pela_regua(self):
        f = FalsoTipo()
        f.tipo = "mecanismo"
        self.assertEqual(self.gt(f, tipo="procedimento").run(), 0)
        self.assertFalse(C.linhas(self.exp / "tipo_procedimento" / "aprovadas.jsonl"))


class RubricaTests(unittest.TestCase):
    def test_classifica_retoma_e_compara_com_o_painel(self):
        from pipeline.qa_research.experimento_ab import rubrica as RU
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        qs = [{"uid": f"v23c:{ITEM}:j:r1:{k:03d}:1", "item": ITEM, "fonte": "v23c", "tipo": t, "pergunta": f"P{k}?",
               "resposta": "R.", "resposta_padrao": "X."} for k, t in enumerate(["conceito", "diagnostico", "decisao"])]
        C.gravar_jsonl(tmp / "dataset.jsonl", qs)
        modelos = ("gpt-4-1", "gpt-5", "gpt-5-4")
        acerto = {0: ("correta",) * 3, 1: ("incorreta", "correta", "correta"), 2: ("incorreta",) * 3}
        with (tmp / "pares.csv").open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["uid", "modelo", "veredito_closed_book"])
            for k, q in enumerate(qs):
                for m, v in zip(modelos, acerto[k]):
                    w.writerow([q["uid"], m, v + ("\0" if k == 1 and m == "gpt-5" else "")])

        class Cli:
            def __init__(self):
                self.n = 0

            def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
                self.n += 1
                assert "D12" in system and "rubrica" in system.lower()
                p = json.loads(user)["pergunta"]
                d = {"P0?": {"criterios": ["F1", "F5"], "nivel": "facil", "justificativa": "lembrar"},
                     "P1?": {"criterios": ["M6"], "nivel": "media", "justificativa": "aplicar"},
                     "P2?": {"criterios": ["D2", "D5", "D12"], "nivel": "dificil", "justificativa": "integrar"}}[p]
                validate(d)
                return d

        cli = Cli()
        r = RU.Rubrica(tmp, cliente=cli, workers=2, **SILENCIO)
        self.assertEqual(r.classificar(), 0)
        res = r.relatorio()
        self.assertEqual((res["n"], res["concorda_regra"]), (3, 100.0))
        self.assertEqual(res["acuracia_por_nivel"]["gpt-4-1"], {"facil": 100.0, "media": 0.0, "dificil": 0.0})
        self.assertLess(res["spearman_nivel_x_acerto"], -0.9)
        self.assertEqual(res["cruzamento_estratos"]["dificil"]["muito_dificil"], 1)
        md = (tmp / "rubrica" / "RUBRICA.md").read_text(encoding="utf-8")
        self.assertIn("| GPT-5 |", md)
        self.assertIn("D12 resposta verdadeira em outra condição", md)
        self.assertEqual(RU.Rubrica(tmp, cliente=cli, **SILENCIO).classificar(), 0)
        self.assertEqual(cli.n, 3)                                          # retomada sem novas chamadas
        with self.assertRaises(ValueError):
            RU.validar({"criterios": ["Z9"], "nivel": "facil", "justificativa": "x"})


class BancoTests(unittest.TestCase):
    def test_poda_unicidade_teto_e_retomada(self):
        from pipeline.qa_research.experimento_ab import banco as BA
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        exp = tmp / "exp"
        C.preparar_documentos(exp, itens=[ITEM])
        calibracao_falsa(exp / "calibracao", auto=0.97)
        orig = tmp / "final"
        perguntas = {
            0: ("Qual técnica acompanha a perda de espessura sem parar o processo?", "Ultrassom contínuo."),
            1: ("O ar deve vir do ramo de instrumentos ou do de serviço?", "Do ramo de instrumentos."),
            2: ("Por que a calibração isolada não basta para validar a malha?", "Falta o teste de ponta a ponta."),
            3: ("Que causa explica a queda de vazão com pressão a montante subindo?", "Restrição na válvula."),
            4: ("Que fenômeno explica a perda de inibidor após a cloração?", "Oxidação do inibidor."),
            5: ("Que linha recebe o vent durante o carregamento nesta unidade?", "Linha 7 do header B."),
            6: ("Qual propriedade do MEG limita sua perda para o gás?", "Baixa volatilidade."),
            7: ("Que mecanismo reduz o oxigênio nas fibras ocas?", "Difusão pela membrana."),
        }
        qs = [{"uid": f"v23c:{ITEM}:j:r1:{k:03d}:1", "fonte": "v23c", "item": ITEM,
               "tipo": "consequencia" if k == 4 else "mecanismo", "cenario": False,
               "pergunta": p, "resposta": r, "explicacao": "e", "resposta_padrao": "x", "por_que_nao": "y",
               "contexto_tecnico": "texto do documento", "blocos_contexto": [{"texto": "texto do documento"}],
               "sinalizar": "forma 'por que X não basta/garante'" if k == 2 else None} for k, (p, r) in perguntas.items()]
        C.gravar_jsonl(orig / "dataset.jsonl", qs)
        modelos = ("gpt-4-1-mini", "gpt-4-1", "gpt-5-mini", "gpt-5", "gpt-5-4")
        with (orig / "pares.csv").open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["uid", "modelo", "resposta_closed_book", "veredito_closed_book", "resposta_open_book",
                        "veredito_open_book"])
            for k, q in enumerate(qs):
                for m in modelos:
                    fech = "incorreta" if k in (3, 4, 5) and m != "gpt-5-4" else "correta"
                    aberto = "incorreta" if k == 0 and m in ("gpt-5", "gpt-5-4") else "correta"
                    w.writerow([q["uid"], m, f"resposta {m} {k}", fech, "r", aberto])
        C.gravar_jsonl(orig / "rubrica" / "rubrica.jsonl", [{"uid": q["uid"], "nivel": "media", "criterios": ["M1"]}
                                                            for q in qs])

        class Juiz:
            def __init__(self):
                self.n = 0

            def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
                self.n += 1
                d = json.loads(user)
                k = int(re.search(r"\d+$", d["respostas"][0]["resposta"]).group())
                assert d["documento"] and d["resposta_padrao"] and "armadilha" in system
                assert len(d["respostas"]) == (5 if k == 0 else 3)              # suspeita: também com documento
                assert [r["com_documento"] for r in d["respostas"]].count(True) == (2 if k == 0 else 0)
                aval = {0: "incorreta", 3: "alternativa_valida", 4: "equivalente", 5: "incorreta"}[k]
                out = {"respostas": [{"id": r["id"], "avaliacao": aval if r["id"] == "R1" else "incorreta"}
                                     for r in d["respostas"]],
                       "gabarito_especifico": True, "gabarito_unico": True, "depende_documento": k == 5,
                       "justificativa": "ok"}
                validate(out)
                return out

        juiz = Juiz()
        b = BA.Banco(orig, tmp / "banco", teto=2, cliente=juiz, embedder=Emb(), exp=exp, **SILENCIO)
        self.assertEqual(b.executar(), 0)
        poda = {r["uid"].split(":")[4]: r["regra"] for r in C.linhas(tmp / "banco" / "poda.jsonl")}
        self.assertEqual({k: v for k, v in poda.items() if v != "R8"},     # 000: pegadinha funcionou, fica
                         {"001": "R2", "002": "R3", "003": "R5", "005": "R7"})
        self.assertEqual(list(poda.values()).count("R8"), 2)
        banco = C.linhas(tmp / "banco" / "banco.jsonl")
        self.assertEqual(len(banco), 2)
        self.assertEqual([x["id"] for x in banco], ["PQ-0001", "PQ-0002"])
        q4 = [x for x in banco if x["uid"].endswith(":004:1")]           # consequência: protegida do teto
        self.assertTrue(q4)
        if q4:                                                           # veredito corrigido pela revisão
            self.assertEqual(q4[0]["dificuldade"]["sem_contexto"]["gpt-5"], "correta")
            self.assertEqual(q4[0]["dificuldade"]["veredito_corrigido"], {"closed_book": ["gpt-5"]})
        res = read_json(tmp / "banco" / "resumo.json")
        self.assertFalse(res["provisorio"])
        self.assertEqual((res["unicidade_revisadas"], res["vereditos_corrigidos"]), (4, 1))
        self.assertEqual((res["suspeitas_r1"], res["suspeitas_mantidas"]), (1, 1))
        self.assertIn("| R5 |", (tmp / "banco" / "BANCO.md").read_text(encoding="utf-8"))
        n = juiz.n
        self.assertEqual(BA.Banco(orig, tmp / "banco", teto=2, cliente=juiz, embedder=Emb(), exp=exp,
                                  **SILENCIO).executar(), 0)
        self.assertEqual(juiz.n, n)                                         # retomada sem novas chamadas
        prov = BA.Banco(orig, tmp / "prov", teto=10, cliente=juiz, embedder=Emb(), exp=exp, **SILENCIO)
        self.assertEqual(prov.executar(revisar=False), 0)
        self.assertTrue(read_json(tmp / "prov" / "resumo.json")["provisorio"])
        self.assertEqual({r["regra"] for r in C.linhas(tmp / "prov" / "poda.jsonl") if r["uid"].endswith(":000:1")},
                         {"R1"})                                             # sem revisão, a suspeita fica fora


class SplitsTests(unittest.TestCase):
    def test_grupo_por_foco_e_documentos(self):
        from pipeline.qa_research.experimento_ab.splits import grupo_base
        self.assertEqual(grupo_base("variada:02_02:j:r3:018:2"), grupo_base("tipo_decisao:02_02:j:r1:018:1"))
        self.assertNotEqual(grupo_base("v23:02_02:j:r1:018:1"), grupo_base("variada:02_02:j:r1:018:1"))
        self.assertEqual(grupo_base("antigo:01_01:j:r1:003:2:ref"), "base:01_01:j:3")
        self.assertEqual(grupo_base("v23c:02_02:c:C21:t2:1"), "v23c:02_02:c:C21:t2:1")


class FalsoAblacao:
    """Gerador, auditor e sustentação simulados da ablação. Na 1ª tentativa, metade das vagas sai com um defeito que o
    auditor recusa; com <tentativas_anteriores> no prompt, o gerador corrige."""
    def __init__(self):
        self.chamadas, self.usuarios, self.sistemas = Counter(), defaultdict(list), defaultdict(list)

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        self.chamadas[tag] += 1
        self.usuarios[tag].append(user)
        self.sistemas[tag].append(system)
        f = None
        if "<janela>" in user:
            f = re.search(r"\[F\] [^\n]*\n(.+?)(?:\n\n\[A\d+\]|\n</janela>)", user, re.S).group(1)
        if tag == "ablacao_naive":
            n = int(re.search(r"Quantidade: (\d+)", user).group(1))
            d = {"questoes": [{"pergunta": f"Qual mecanismo explica o fenômeno {k} no separador?",
                               "resposta": f"Mecanismo {k}."} for k in range(n)]}
        elif tag == "ablacao_naive_vaga":
            vaga = re.search(r"Pedido: (V\d+)", user).group(1)
            d = {"questoes": [{"pergunta": f"Qual mecanismo explica o fenômeno da vaga {vaga} no separador?",
                               "resposta": f"Mecanismo {vaga}."}]}
        elif tag == "ablacao_regras_vaga":
            vaga = re.search(r"Pedido: (V\d+)", user).group(1)
            t = re.search(r"1 questão do tipo (\w+)", user).group(1)
            d = {"questoes": [{"tipo": t, "cenario": t in ("decisao", "diagnostico"), "conhecimento": f"c {vaga}",
                               "pergunta": f"Qual princípio de {t} explica o caso da vaga {vaga}?",
                               "resposta": f"Princípio {vaga}.", "explicacao": "e", "resposta_padrao": "p",
                               "por_que_nao": "q"}]}
        elif tag == "ablacao_regras":
            pedido = re.findall(r"(\d+) questões do tipo (\w+)", user)
            d = {"questoes": [{"tipo": t, "cenario": t in ("decisao", "diagnostico"), "conhecimento": f"c {t} {k}",
                               "pergunta": f"Qual princípio de {t} explica o caso {k} da planta?",
                               "resposta": f"Princípio {t} {k}.", "explicacao": "e", "resposta_padrao": "p",
                               "por_que_nao": "q"} for n, t in pedido for k in range(int(n))]}
        elif tag == "ablacao_documentos":
            d = {"motivo": "", "questoes": [{"pergunta": f"O que descreve {' '.join(f.split()[:6])}?",
                                             "resposta": " ".join(f.split()[:4])}]}
        elif tag == "ablacao_slot":
            tipo = re.search(r"do tipo `(\w+)`", system).group(1)
            ruim = "DEFEITO " if "<tentativas_anteriores>" not in user and int(hashlib.md5(f.encode()).hexdigest(), 16) % 2 else ""
            d = {"motivo": "", "questoes": [{
                "tipo": tipo, "cenario": tipo in ("decisao", "diagnostico"), "conhecimento": f"relação {f[:30]}",
                "pergunta": f"Qual elemento técnico {ruim}explica {' '.join(f.split()[:6])}?",
                "resposta": " ".join(f.split()[:4]), "explicacao": "Os blocos sustentam.",
                "resposta_padrao": "Outro elemento qualquer.", "por_que_nao": "O traço X o exclui.",
                "fundamentos": [{"bloco": "F", "trecho": " ".join(f.split()[:5])}]}]}
        elif tag == "ablacao_auditoria":
            ok = "DEFEITO" not in user
            d = {"sem_documento": True, "resposta_alternativa": "Outra coisa.", "alternativa_excluida": ok,
                 "atalho": False, "sustentada": True, "elemento_unico": True, "tipo_sugerido": "mecanismo",
                 "justificativa": "ok" if ok else "há outra resposta"}
        elif tag == "ablacao_faithfulness":
            b = json.loads(user)["blocos"][0]
            d = {"cobertura_completa": True, "observacoes": "",
                 "afirmacoes": [{"afirmacao": "a", "veredito": "sustentada", "justificativa": "j",
                                 "evidencias": [{"bloco": b["id"], "trecho": b["texto"][:20]}]}]}
        else:
            raise AssertionError(tag)
        if validate:
            validate(d)
        return d


class AblacaoTests(unittest.TestCase):
    def setUp(self):
        VariadaTests.setUp(self)
        _, self.bs = blocos(ITEM, self.exp / "docs" / "antigo")
        tipos = ("mecanismo", "decisao", "conceito")
        self.banco = self.exp / "banco.jsonl"
        C.gravar_jsonl(self.banco, [
            {"id": f"PQ-{k:04d}", "uid": f"{('variada', 'tipo_decisao', 'v22')[k % 3]}:{ITEM}:j:r1:{k % len(self.bs):03d}:1",
             "item": ITEM, "tipo": tipos[k % 3], "pergunta": f"Pergunta {k}?", "resposta": f"Resposta {k}."}
            for k in range(30)])

    def a(self, f, **kw):
        from pipeline.qa_research.experimento_ab.ablacao import Ablacao
        cl = {"geracao": f, "auditoria": f, "sustentacao": f, "dedup_juiz": NuncaRedundante()}
        return Ablacao(self.exp / "ablacao", banco=self.banco, exp=self.exp, docs=self.exp / "docs" / "antigo",
                       n=kw.pop("n", 8), externos=self.ext, convertidas=self.conv, clientes=cl, embedder=Emb(),
                       workers=4, **{**SILENCIO, **kw})

    def test_vagas_estratificadas_e_distintas(self):
        from pipeline.qa_research.experimento_ab.ablacao import selecionar
        v = selecionar(self.banco, 8)
        self.assertEqual(len(v), 8)
        self.assertEqual(len({(x["item"], x["foco"], x["tipo"]) for x in v}), 8)
        self.assertTrue(all(not x["ref_uid"].startswith("v22:") for x in v))   # só documentos base
        self.assertEqual(Counter(x["tipo"] for x in v), Counter({"mecanismo": 4, "decisao": 4}))
        with self.assertRaises(ValueError):
            selecionar(self.banco, 50)

    def test_sete_bracos_componentes_isolados(self):
        f = FalsoAblacao()
        ab = self.a(f)
        self.assertEqual(ab.executar(), 0)
        d = self.exp / "ablacao"
        bracos = ("naive_vaga", "regras_vaga", "naive", "documentos", "regras", "documentos_regras", "sem_retro",
                  "sem_externos", "completo")
        q = {b: C.linhas(d / f"questoes_{b}.jsonl") for b in bracos}
        self.assertEqual((f.chamadas["ablacao_naive"], f.chamadas["ablacao_regras"]), (1, 1))   # lote: uma por tópico
        # por vaga: uma chamada independente por vaga, sem documento, cada uma com o identificador da vaga
        self.assertEqual((f.chamadas["ablacao_naive_vaga"], f.chamadas["ablacao_regras_vaga"]), (8, 8))
        for tag in ("ablacao_naive_vaga", "ablacao_regras_vaga"):
            us_ = f.usuarios[tag]
            self.assertEqual(len(set(us_)), 8)
            self.assertTrue(all("<janela>" not in u and "Pedido: V" in u for u in us_))
        self.assertTrue(all("questão do tipo" in u for u in f.usuarios["ablacao_regras_vaga"]))
        self.assertEqual({x["vaga"] for x in q["naive_vaga"]}, {x["vaga"] for x in q["documentos"]})
        self.assertEqual({x["tipo"] for x in q["regras_vaga"]}, {"mecanismo", "decisao"})
        self.assertEqual(f.chamadas["ablacao_documentos"], 8)
        self.assertIn("4 questões do tipo decisao", f.usuarios["ablacao_regras"][0])
        self.assertNotIn("<janela>", f.usuarios["ablacao_regras"][0])
        self.assertTrue(all("Critérios" not in s for s in f.sistemas["ablacao_documentos"]))    # sem regras
        ruins = sum("DEFEITO" in x["pergunta"] for x in q["documentos_regras"])
        self.assertTrue(0 < ruins < 8)
        # 4 braços x 8 vagas na 1ª tentativa (nada compartilhado) + novas tentativas nos 2 braços com retro
        self.assertEqual(f.chamadas["ablacao_slot"], 32 + 2 * ruins)
        us, ss = f.usuarios["ablacao_slot"], f.sistemas["ablacao_slot"]
        # exemplos de forma só em sem_retro e completo; semente boas/ruins só nos braços com retroalimentação
        self.assertEqual(sum("<exemplos_de_forma>" in u for u in us), 16 + ruins)
        com_semente = [u for u, s_ in zip(us, ss) if "# Exemplos de referência" in s_]
        self.assertEqual(len(com_semente), 16 + 2 * ruins)
        self.assertTrue(all("<conhecimentos_cobertos>" in u for u in com_semente))
        self.assertFalse(any("<conhecimentos_cobertos>" in u for u, s_ in zip(us, ss) if "# Exemplos de referência" not in s_))
        # ondas de 5: as 3 vagas da 2ª onda já veem as aceitas e as recusadas da 1ª
        self.assertTrue(any("<exemplos_do_pipeline>" in u and "Aceitas:" in u for u in com_semente))
        self.assertEqual({x["onda"] for x in q["completo"]}, {1, 2})
        ac = {b: sum(x["aceita"] for x in v) for b, v in q.items()}
        self.assertEqual((ac["documentos_regras"], ac["sem_retro"]), (8 - ruins, 8 - ruins))
        self.assertEqual((ac["sem_externos"], ac["completo"], ac["naive"], ac["regras"], ac["documentos"],
                          ac["naive_vaga"], ac["regras_vaga"]), (8, 8, 8, 8, 8, 8, 8))
        self.assertEqual({x["tipo"] for x in q["regras"]}, {"mecanismo", "decisao"})
        r = read_json(d / "resultado.json")
        self.assertEqual(r["pareados"]["completo_vs_sem_retro"]["so_primeiro"], ruins)
        self.assertIn("documentos_regras_vs_documentos", r["pareados"])
        for k in ("regras_vaga_vs_naive_vaga", "documentos_vs_naive_vaga", "documentos_regras_vs_regras_vaga"):
            self.assertIn(k, r["pareados"])
        self.assertIn("validas_sem_exigir_fonte", r["bracos"]["naive_vaga"])
        self.assertIn("validas_sem_exigir_fonte", r["bracos"]["regras"])
        md = (d / "ABLACAO.md").read_text(encoding="utf-8")
        self.assertIn("Regras em lote (por tópico)", md)
        self.assertIn("Naive (uma por chamada)", md)
        antes = sum(f.chamadas.values())
        self.assertEqual(self.a(f).executar(), 0)                               # retomada: nada é refeito
        self.assertEqual(sum(f.chamadas.values()), antes)

    def test_naive_reaproveitado_da_v1(self):
        from pipeline.qa_research.experimento_ab import ablacao as A
        f = FalsoAblacao()
        v1 = self.exp / "v1"
        orig = A.SAIDA_V1
        try:
            A.SAIDA_V1 = v1
            ab = A.Ablacao(v1, banco=self.banco, exp=self.exp, docs=self.exp / "docs" / "antigo", n=8,
                           bracos=["naive"], externos=self.ext, convertidas=self.conv,
                           clientes={"geracao": f, "auditoria": f, "sustentacao": f, "dedup_juiz": NuncaRedundante()},
                           embedder=Emb(), workers=2, **SILENCIO)
            self.assertEqual(ab.executar(), 0)
            antes = sum(f.chamadas.values())
            self.assertEqual(self.a(f, bracos=["naive"]).executar(), 0)
            self.assertEqual(sum(f.chamadas.values()), antes)                     # nada do naive é refeito
            self.assertTrue((self.exp / "ablacao" / "naive" / "lotes" / f"{ITEM}.json").exists())
        finally:
            A.SAIDA_V1 = orig

    def test_um_braco_sozinho_e_config_fixa(self):
        f = FalsoAblacao()
        self.assertEqual(self.a(f, bracos=["completo"]).executar(), 0)
        self.assertFalse((self.exp / "ablacao" / "sem_retro").exists())         # nada compartilhado entre braços
        with self.assertRaises(ValueError):
            self.a(f, n=6)

    def test_metricas(self):
        from pipeline.qa_research.experimento_ab.ablacao import distinct, mattr, mcnemar, mtld, wilson
        self.assertEqual(distinct(["a b a b"], 1), 0.5)
        self.assertAlmostEqual(mattr(["a"] * 20, 5), 0.2)
        self.assertAlmostEqual(mattr(["a"] * 10 + ["b"] * 10, 5), 20 / 80)      # 4 das 16 janelas têm 2 tipos
        self.assertGreater(mtld([str(k) for k in range(100)]), mtld(["a", "b"] * 50))
        lo, hi = wilson(50, 100)
        self.assertTrue(lo < 50 < hi)
        self.assertEqual(mcnemar([True] * 5, [False] * 5)["so_primeiro"], 5)
        self.assertLess(mcnemar([True] * 10, [False] * 10)["p"], 0.01)


class FalsoV3:
    """Gerador, auditor e sustentação simulados da ablação v3: 2 questões por chamada; o auditor reprova as que têm
    DEFEITO (a 2ª de cada chamada nas visitas ímpares)."""
    def __init__(self):
        self.chamadas, self.usuarios, self.sistemas = Counter(), defaultdict(list), defaultdict(list)

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        self.chamadas[tag] += 1
        self.usuarios[tag].append(user)
        self.sistemas[tag].append(system)
        if tag.startswith("abl3_") and tag not in ("abl3_auditoria", "abl3_faithfulness"):
            c = tag[5:]
            pid = re.search(r"Pedido: (\S+)", user).group(1)
            v = int(pid.rsplit(":v", 1)[1])
            qs = []
            for k in (1, 2):
                ruim = "DEFEITO " if k == 2 and v % 2 else ""
                q = {"pergunta": f"Qual {ruim}mecanismo {c} explica o caso {pid} número {k}?", "resposta": f"Mecanismo {k}."}
                if c != "naive":
                    q.update(tipo="mecanismo", cenario=False, conhecimento=f"relação {pid} {k}", explicacao="e",
                             resposta_padrao="p", por_que_nao="q")
                if c not in ("naive", "regras"):
                    q["fundamentos"] = [{"bloco": "F", "trecho": "x"}]
                qs.append(q)
            d = {"questoes": qs, "motivo": ""}
        elif tag == "abl3_auditoria":
            ok = "DEFEITO" not in user
            d = {"sem_documento": True, "resposta_alternativa": "Outra coisa.", "alternativa_excluida": ok,
                 "atalho": False, "sustentada": True, "elemento_unico": True, "tipo_sugerido": "mecanismo",
                 "justificativa": "ok" if ok else "há outra resposta"}
        elif tag == "abl3_faithfulness":
            b = json.loads(user)["blocos"][0]
            d = {"cobertura_completa": True, "observacoes": "",
                 "afirmacoes": [{"afirmacao": "a", "veredito": "sustentada", "justificativa": "j",
                                 "evidencias": [{"bloco": b["id"], "trecho": b["texto"][:20]}]}]}
        else:
            raise AssertionError(tag)
        if validate:
            validate(d)
        return d


class AblacaoV3Tests(unittest.TestCase):
    def setUp(self):
        VariadaTests.setUp(self)

    def a(self, f, **kw):
        from pipeline.qa_research.experimento_ab.ablacao_v3 import AblacaoV3
        cl = {"geracao": f, "auditoria": f, "sustentacao": f, "dedup_juiz": NuncaRedundante()}
        return AblacaoV3(self.exp / "abl3", exp=self.exp, docs=self.exp / "docs" / "antigo", itens=[ITEM],
                         focos_por_topico=3, visitas=2, externos=self.ext, convertidas=self.conv, clientes=cl,
                         embedder=Emb(), workers=4, **{**SILENCIO, **kw})

    def test_prompts_da_escada(self):
        from pipeline.qa_research.experimento_ab.ablacao_v3 import CONFIGS, sistema_base
        s = {c: sistema_base(cfg) for c, cfg in CONFIGS.items()}
        self.assertNotIn("Critérios", s["naive"])
        self.assertIn("# Tipos", s["regras"])                        # tipos entram com as regras
        self.assertNotIn("[F]", s["regras"])                          # sem documento, nenhuma regra fala do texto
        self.assertIn("verificável na literatura", s["regras"])
        self.assertIn("[F]", s["documentos"])
        self.assertNotIn("exemplos_de_forma", s["documentos"])
        self.assertIn("exemplos_de_forma", s["externos"])
        self.assertNotIn("conhecimentos_cobertos", s["externos"])
        for t in ("conhecimentos_cobertos", "questoes_deste_foco", "boas_ja_avaliadas", "Exemplos de referência"):
            self.assertIn(t, s["retro"])
        self.assertTrue(all("{{" not in x for x in s.values()))
        # cada degrau contém o anterior (exceto a troca das regras sem documento pelas do documento)
        self.assertTrue(len(s["naive"]) < len(s["regras"]) < len(s["externos"]) < len(s["retro"]))

    def test_escada_sem_poda_e_retro_por_exemplos(self):
        f = FalsoV3()
        ab = self.a(f)
        self.assertEqual(ab.executar(("geracao", "sustentacao", "dedup", "relatorio")), 0)
        d = self.exp / "abl3"
        n_unid = len(ab.unidades)
        self.assertEqual(n_unid, 3 * 2)
        for c in ("naive", "regras", "documentos", "externos", "retro"):
            self.assertEqual(f.chamadas[f"abl3_{c}"], n_unid)           # mesmo número de chamadas
            self.assertEqual(len(C.linhas(d / f"questoes_{c}.jsonl")), 2 * n_unid)   # nada é podado nem refeito
            self.assertEqual(len(set(f.usuarios[f"abl3_{c}"])), n_unid)  # chamadas independentes (pedido no texto)
        self.assertEqual(f.chamadas["abl3_auditoria"], 5 * 2 * n_unid)
        us = dict(zip(["naive", "regras", "documentos", "externos", "retro"],
                      [f.usuarios[f"abl3_{c}"] for c in ("naive", "regras", "documentos", "externos", "retro")]))
        self.assertTrue(all("<janela>" not in u for u in us["naive"] + us["regras"]))
        self.assertTrue(all("<janela>" in u for u in us["documentos"]))
        self.assertTrue(all("<exemplos_de_forma>" in u for u in us["externos"] + us["retro"]))
        self.assertFalse(any("<exemplos_de_forma>" in u for u in us["documentos"]))
        self.assertFalse(any("<questoes_deste_foco>" in u for c in ("naive", "regras", "documentos", "externos")
                             for u in us[c]))
        # retroalimentação: a visita 2 vê as questões da visita 1 do mesmo foco, com o julgamento
        v2 = [u for u in us["retro"] if re.search(r"Pedido: \S+:v2", u)]
        self.assertTrue(v2 and all("reprovada (varias_respostas" in u and "[aprovada]" in u for u in v2))
        self.assertTrue(all("questoes_boas" in s_ for s_ in f.sistemas["abl3_retro"]))     # semente fixa
        r = read_json(d / "resultado.json")
        x = r["configs"]["retro"]
        self.assertEqual(x["geradas"], 2 * n_unid)
        self.assertAlmostEqual(x["aprovadas_auditor"]["pct"], 75.0)    # a 2ª questão das visitas ímpares falha
        self.assertAlmostEqual(x["validas"]["pct"], 75.0)
        self.assertIn("retro_vs_externos", r["comparacoes"])
        self.assertIsNone(r["configs"]["naive"]["cobertura_focos_validos"])
        # sem documento: auditoria com blocos buscados no corpus
        q = C.linhas(d / "questoes_naive.jsonl")[0]
        self.assertEqual([b["id"] for b in q["blocos_contexto"]][:2], ["B1", "B2"])
        antes = sum(f.chamadas.values())
        self.assertEqual(self.a(f).executar(("geracao", "sustentacao", "dedup", "relatorio")), 0)
        self.assertEqual(sum(f.chamadas.values()), antes)                # retomada: nada é refeito

    def test_amostra_dificuldade_estratificada(self):
        f = FalsoV3()
        ab = self.a(f)
        ab.executar(("geracao",))
        am = ab.amostra_dificuldade(5)
        self.assertEqual(Counter(q["config"] for q in am), Counter({c: 5 for c in ab.configs}))
        self.assertEqual(len({q["uid"] for q in am}), len(am))


class RetroV2Tests(unittest.TestCase):
    """Variantes da retroalimentação sem memória: só exemplos julgados de outros documentos."""
    def setUp(self):
        VariadaTests.setUp(self)
        (self.exp / "docs" / "manifesto.json").unlink()
        C.preparar_documentos(self.exp, itens=[ITEM, "07_01"])

    def a(self, f, configs, **kw):
        from pipeline.qa_research.experimento_ab.ablacao_v3 import AblacaoV3
        cl = {"geracao": f, "auditoria": f, "sustentacao": f, "dedup_juiz": NuncaRedundante()}
        return AblacaoV3(self.exp / "abl3", exp=self.exp, docs=self.exp / "docs" / "antigo", itens=[ITEM, "07_01"],
                         configs=configs, focos_por_topico=2, visitas=2, externos=self.ext, convertidas=self.conv,
                         clientes=cl, embedder=Emb(), workers=4, **{**SILENCIO, **kw})

    def test_sem_memoria_exemplos_de_outros_documentos(self):
        from pipeline.qa_research.experimento_ab.ablacao_v3 import BASE, sistema_base, CONFIGS
        f = FalsoV3()
        self.assertEqual(self.a(f, ["externos"]).executar(("geracao",)), 0)       # escada já rodada
        vs = ["retro_sem_memoria", "retro_sem_memoria_sem_externos"]
        ab = self.a(f, vs)
        self.assertEqual(ab.executar(("geracao",)), 0)
        d = self.exp / "abl3"
        self.assertEqual(read_json(d / "config.json")["configs"], BASE)          # a pasta da escada não muda
        self.assertEqual(set(read_json(d / "config_variantes.json")), set(vs))
        for c in vs:
            us, ss = f.usuarios[f"abl3_{c}"], f.sistemas[f"abl3_{c}"]
            self.assertEqual(len(us), len(ab.unidades))
            self.assertFalse(any("<conhecimentos_cobertos>" in u or "<questoes_deste_foco>" in u for u in us))
            self.assertTrue(all("<defeitos_frequentes>" in u and "<boas_ja_avaliadas>" in u for u in us))
            base = sistema_base(CONFIGS["externos" if c == "retro_sem_memoria" else "documentos"])
            self.assertTrue(all(s.startswith(base) and "Verificação antes de entregar" in s and "<questoes_boas>" in s
                                for s in ss))
            # sem memória: nada do próprio documento; as julgadas vêm do outro documento
            tardias = [u for u in us if re.search(r"Pedido: \S+:v2", u)]
            for u in tardias:
                item = re.search(r"Pedido: (\S+?):", u).group(1)
                outro = "07_01" if item == ITEM else ITEM
                ex = u.split("<defeitos_frequentes>")[1].split("</ruins_ja_avaliadas>")[0]
                self.assertNotIn(f"caso {item}:", ex)
                self.assertIn(f"caso {outro}:", ex)
                self.assertIn("Várias respostas (", ex)                      # defeito por extenso
                self.assertIn("Questões já julgadas em outros documentos", ex)
        self.assertTrue(all("<exemplos_de_forma>" in u for u in f.usuarios["abl3_retro_sem_memoria"]))
        self.assertFalse(any("<exemplos_de_forma>" in u for u in f.usuarios["abl3_retro_sem_memoria_sem_externos"]))
        # a sustentação das aprovadas roda a cada onda (as boas são só as totalmente válidas)
        aprov = [q for c in vs for q in ab.finais(c) if q["aprovada_auditor"]]
        self.assertTrue(aprov and all(q["sustentacao"] == "totalmente_sustentado" for q in aprov))
        antes = sum(f.chamadas.values())
        self.assertEqual(self.a(f, vs).executar(("geracao", "sustentacao")), 0)
        self.assertEqual(sum(f.chamadas.values()), antes)                # retomada: nada é refeito

    def test_sorteio_estratificado_e_defeitos_da_semente(self):
        import random as _r
        from pipeline.qa_research.experimento_ab.ablacao_v3 import codigo_semente, estratificado
        pool = [{"t": t, "a": a} for t in "xyz" for a in (0, 1) for _ in range(5)]
        out = estratificado(pool, 6, _r.Random(1), lambda e: e["t"], lambda e: e["a"] == 1)
        self.assertEqual(Counter(e["t"] for e in out), Counter({"x": 2, "y": 2, "z": 2}))
        self.assertEqual(Counter(e["a"] for e in out), Counter({0: 3, 1: 3}))
        self.assertEqual(len(estratificado(pool[:3], 10, _r.Random(1), lambda e: e["t"], lambda e: True)), 3)
        self.assertEqual(codigo_semente("Várias respostas: outra coisa."), "varias_respostas")
        self.assertEqual(codigo_semente("Eliminação: o enunciado iguala tudo."), "atalho")
        self.assertEqual(codigo_semente("Gabarito em lista: cobra itens."), "nao_unico")


class ExternosTests(unittest.TestCase):
    """Respostas do vLLM (Llama) julgadas no servidor pelo motor padrão, só nas questões do banco."""
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)

    def test_respostas_prontas_julgadas_so_no_banco(self):
        from pipeline.qa_research import benchmark_gap as G
        from pipeline.qa_research.experimento_ab import externos as E
        from pipeline.qa_research.experimento_ab import responder_vllm as R
        from pipeline.qa_research.tests.test_especialista_finalizacao import Juiz as JuizResp
        final, banco, resp = self.tmp / "final", self.tmp / "banco", self.tmp / "resp"
        for p in (final, banco, resp):
            p.mkdir()
        ds = [{"uid": f"v23c:{ITEM}:j:r1:00{k}:1", "item": ITEM, "tipo": "mecanismo", "fonte": "v23c", "composicao": "simples",
               "pergunta": f"Por que ocorre o fenômeno {k}?", "resposta": f"Mecanismo {k}.",
               "contexto_tecnico": f"Bloco técnico {k}.",
               "blocos_contexto": [{"id": "B1", "texto": f"Bloco técnico {k}.", "indice_documento": k}]}
              for k in range(4)]
        C.gravar_jsonl(final / "dataset.jsonl", ds)
        C.gravar_jsonl(banco / "banco.jsonl", ds[:3])                      # a 4ª ficou fora do banco
        # o que o responder_vllm grava: uma resposta por uid, identificada pela mensagem exata do usuário
        linhas_ = [{"uid": f"{arm}:{q['uid']}", "usuario_sha256": R.sha(R.usuario(
                    {**q, "contexto_tecnico": q["contexto_tecnico"] if arm == "open_book" else None})),
                    "resposta": f"Mecanismo {k}." if arm == "open_book" else ""}
                   for k, q in enumerate(ds[:3]) for arm in G.ARMS]
        C.gravar_jsonl(resp / "llama-3-1-8b.jsonl", linhas_)
        (resp / "llama-3-1-8b.meta.json").write_text(json.dumps({
            "modelo": "llama-3-1-8b", "hf": "meta-llama/Llama-3.1-8B-Instruct", "questoes": 6, "respondidas": 6,
            "sonda": {"usuario": R.usuario(None), "resposta": "Separa óleo, gás e água."}}), encoding="utf-8")
        pronto = E.RespostasProntas(resp / "llama-3-1-8b.jsonl", {"usuario": R.usuario(None), "resposta": "x"})
        st = E.executar(self.tmp / "saida", respostas=resp, final=final, banco=banco, workers=2, judge_workers=1,
                        clientes={"juiz": JuizResp(), "resp_llama-3-1-8b": pronto}, progress=lambda *a, **k: None)
        self.assertEqual(st, 0)
        self.assertEqual(pronto.chamadas, 7)                               # sonda + 3 questões x 2 condições
        self.assertEqual(len(C.linhas(self.tmp / "saida" / "dataset.jsonl")), 3)
        cfg = read_json(self.tmp / "saida" / "config.json")
        self.assertEqual(cfg["modelos"], {"llama-3-1-8b": "vllm/meta-llama/Llama-3.1-8B-Instruct"})
        self.assertTrue((self.tmp / "saida" / "QUALIDADE.md").exists())
        with self.assertRaises(KeyError):
            pronto.json("s", R.usuario({"pergunta": "Outra?", "contexto_tecnico": None}))

    def test_extrair_resposta(self):
        from pipeline.qa_research.experimento_ab.responder_vllm import extrair
        self.assertEqual(extrair('{"resposta": "Cavitação."}'), ("Cavitação.", "json"))
        self.assertEqual(extrair('```json\n{"resposta": "Golpe de aríete"}\n```'), ("Golpe de aríete", "json"))
        self.assertEqual(extrair('Claro! {"resposta": "Hidrato"} pronto')[1], "extraida")
        self.assertEqual(extrair("Hidrato de metano"), ("Hidrato de metano", "texto"))
