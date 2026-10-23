"""Testes offline da instalação, limpeza e revisão dos exemplos externos (sem rede e sem Azure)."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pipeline.qa_references import preparar_exemplos as P


def par(q, a, fonte="pira_ptbr", i=0):
    return {"id": f"{fonte}:{i}", "question": q, "answer": a, "source": fonte}


class RegrasTests(unittest.TestCase):
    def test_filtros(self):
        casos = {
            ("Qual das seguintes substâncias é um ácido forte?", "HCl"): "depende_de_alternativas",
            ("Qual das reações a seguir é uma reação equilibrada?", "2 H2 + O2 → 2 H2O"): "depende_de_alternativas",
            ("Qual afirmação explica melhor o fenômeno observado?", "A segunda"): "depende_de_alternativas",
            ("Quais afirmações sobre o processo estão corretas?", "I e II"): "depende_de_alternativas",
            ("Segundo o texto, qual é a profundidade do campo?", "2000 metros de lâmina d'água"): "depende_de_texto_ou_imagem",
            ("O que mostra a figura sobre a corrente elétrica no circuito?", "Ela aumenta"): "depende_de_texto_ou_imagem",
            ("Is the ocean saltier near the equator than near the poles?", "yes"): "resposta_sim_nao",
            ("A força resultante sobre o corpo é igual a ____ quando ele está em equilíbrio?", "zero"): "lacuna",
            ("Qual é a velocidade final do bloco após dois segundos de queda?", "19,6 m/s"): "resposta_numerica_ou_formula",
            ("Os relógios em uma nave rápida parecem andar devagar quando observados", "da Terra"): "nao_e_pergunta",
            ("Por quê?", "Porque sim."): "tamanho_pergunta",
        }
        for (q, a), esperado in casos.items():
            self.assertEqual(P.motivo_regra(par(q, a)), esperado, q)
        self.assertIsNone(P.motivo_regra(par("Por que o fluoreto de hidrogênio é líquido a 15 °C, ao contrário dos outros halogenetos?",
                                             "Por causa das ligações de hidrogênio fortes entre as moléculas.")))
        self.assertIsNone(P.motivo_regra(par("Quantos barris de óleo há nas reservas do pós-sal estimadas?",
                                             "Entre 15 e 21 bilhões de barris")))

    def test_limpar_duplicatas_e_instalar_sem_rede(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            with mock.patch.object(P, "FONTES_DIR", tmp / "fontes"), mock.patch.object(P, "LEGADO", tmp / "legado.jsonl"):
                legado = [{"id": "pira_ptbr:1", "question": "Qual é a função do lastro em um navio petroleiro?",
                           "answer": "Garantir estabilidade e calado adequados.", "source_url": "u", "source_split": "train"},
                          {"id": "pira_ptbr:2", "question": "Qual é a função do lastro em um navio petroleiro?",
                           "answer": "Garantir estabilidade.", "source_url": "u", "source_split": "train"}]
                (tmp / "legado.jsonl").write_text("\n".join(json.dumps(x) for x in legado), encoding="utf-8")
                with mock.patch.object(P, "baixar_catalogo", side_effect=AssertionError("não deveria baixar")):
                    sit = P.instalar(["pira_ptbr"], progresso=lambda *a: None)
                    self.assertEqual(sit["pira_ptbr"]["origem"], "qa_examples.jsonl")
                    sit = P.instalar(["pira_ptbr"], progresso=lambda *a: None)
                    self.assertEqual(sit["pira_ptbr"]["origem"], "ja_instalada")
                mantidos, motivos, _ = P.limpar(["pira_ptbr"])
                self.assertEqual(len(mantidos), 1)
                self.assertEqual(motivos["pira_ptbr"]["duplicata"], 1)


class ClienteRevisao:
    def __init__(self):
        self.chamadas = 0

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        self.chamadas += 1
        itens = json.loads(user)
        data = {"avaliacoes": [{"id": i["id"], "manter": "sex" not in i["resposta"],
                                "criterio": "ok" if "sex" not in i["resposta"] else "forma"} for i in itens]}
        validate(data)
        return data


class RevisaoTests(unittest.TestCase):
    def test_revisar_lotes(self):
        itens = [par(f"Pergunta técnica número {k} sobre corrosão em dutos?", "sex" if k == 3 else "Resposta",
                     "qasc", k) for k in range(30)]
        cli = ClienteRevisao()
        mantidos, contagem = P.revisar(itens, "falso:low", lote=25, workers=2, progresso=lambda *a: None, cliente=cli)
        self.assertEqual(cli.chamadas, 2)
        self.assertEqual(len(mantidos), 29)
        self.assertEqual(contagem[("qasc", "forma")], 1)


class RedeTests(unittest.TestCase):
    def test_espera_em_429_e_falha_isolada(self):
        import io
        from urllib.error import HTTPError
        respostas = [HTTPError("u", 429, "Too Many Requests", {"Retry-After": "7"}, None),
                     io.BytesIO(b'{"ok": 1}')]

        class Resp:
            def __init__(self, b):
                self.b = b
            def __enter__(self):
                return self
            def __exit__(self, *a):
                return False
            def read(self):
                return self.b.read()

        def falso(req, timeout=0):
            r = respostas.pop(0)
            if isinstance(r, Exception):
                raise r
            return Resp(r)

        esperas = []
        with mock.patch.object(P, "urlopen", falso):
            self.assertEqual(P.get_json_paciente("https://exemplo.invalid/x", espera=esperas.append), {"ok": 1})
        self.assertEqual(esperas, [7.0])

        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            with mock.patch.object(P, "FONTES_DIR", tmp), mock.patch.object(P, "LEGADO", tmp / "x.jsonl"), \
                    mock.patch.object(P, "baixar_catalogo", side_effect=RuntimeError("HTTP Error 429")), \
                    mock.patch.object(P, "baixar_mmmlu", return_value=[par("Por que o gelo flutua na água líquida?", "Porque é menos denso.", "mmmlu_ptbr")]):
                sit = P.instalar(["qasc", "mmmlu_ptbr"], progresso=lambda *a: None)
        self.assertEqual(sit["qasc"]["origem"], "falha")
        self.assertEqual(sit["mmmlu_ptbr"]["origem"], "download")


if __name__ == "__main__":
    unittest.main()
