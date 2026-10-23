"""Piloto de geração de questões por janela: três blocos consecutivos, um foco, um único prompt.

Somente geração. Não há refinamento, auditoria nem descarte: o código apenas confere a
estrutura do JSON (para que a resposta seja utilizável) e registra métricas descritivas.
"""
from __future__ import annotations

import csv
import hashlib
from collections import Counter
import json
import os
import re
import threading
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QA = ROOT / "pipeline" / "qa_research"
PROMPT = QA / "prompt_janela_qa_10.md"
PROMPT_JUNTO = QA / "prompt_janela_qa_11.md"
PROMPT_COMPOSICAO = QA / "prompt_janela_qa_12.md"
COMPOSICAO_PADRAO = {"facil": 1, "media": 2, "dificil": 1}
PROMPT_PLANO = QA / "prompt_janela_planejamento_qa_11.md"
PROMPT_REDACAO = QA / "prompt_janela_redacao_qa_11.md"
DOCS = QA / "relatorios" / "dez_areas_final_v2"
PROGRAMA = QA / "configs" / "dez_areas_v1" / "programa.json"

STATUS = ("ok", "parcial", "sem_questoes")
MODOS = ("junto", "separado")
CAMPOS_PLANO = ("id", "dificuldade", "tipo_demanda", "alvo", "resposta_esperada", "condicoes_necessarias",
                "exigencia_cognitiva", "fundamentos")
NUM_F = {1: "uma", 2: "duas", 3: "três", 4: "quatro"}
NUM_M = {1: "um", 2: "dois", 3: "três", 4: "quatro"}


def texto_composicao(comp: dict) -> str:
    """Ex.: {'facil': 1, 'media': 2, 'dificil': 1} -> '4 questões: uma fácil, duas médias e uma difícil'."""
    nomes = {"facil": ("fácil", "fáceis"), "media": ("média", "médias"), "dificil": ("difícil", "difíceis")}
    partes = [f"{NUM_F[n]} {nomes[d][0] if n == 1 else nomes[d][1]}" for d, n in comp.items() if n]
    lista = partes[0] if len(partes) == 1 else ", ".join(partes[:-1]) + " e " + partes[-1]
    return f"{sum(comp.values())} questões: {lista}"


def exigencia(min_medias: int, min_dificeis: int, masculino: bool = False) -> str:
    """Ex.: 'uma média e uma difícil' (questões) ou 'um médio e um difícil' (alvos)."""
    num = NUM_M if masculino else NUM_F
    partes = []
    if min_medias:
        adj = ("médio" if masculino else "média") if min_medias == 1 else ("médios" if masculino else "médias")
        partes.append(f"{num[min_medias]} {adj}")
    if min_dificeis:
        partes.append(f"{num[min_dificeis]} {'difícil' if min_dificeis == 1 else 'difíceis'}")
    return " e ".join(partes)
DIFICULDADES = ("facil", "media", "dificil")
DEMANDAS = ("recordar", "inferir", "diagnosticar", "comparar", "decidir")
ROTULOS = ("A1", "F", "A2")
CAMPOS = ("id", "dificuldade", "tipo_demanda", "conhecimento", "pergunta", "resposta", "fundamentos")
SEM_PREFERENCIA = "Nenhuma preferência."
ALVO_DIFICULDADE = {"facil": 0.5, "media": 0.3, "dificil": 0.2}
TETO_PERGUNTA = {"facil": 35, "media": 60, "dificil": 90}  # tamanho pedido no prompt v11, só medido


# ------------------------------------------------------------------ utilidades
def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def atomic_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".{os.getpid()}.{threading.get_ident()}.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def palavras(texto: str) -> int:
    return len(texto.split())


def normalizar(texto: str) -> str:
    t = unicodedata.normalize("NFKC", texto).lower()
    t = t.translate(str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "–": "-", "—": "-"}))
    t = re.sub(r"\s+", " ", t).strip()
    return t.strip(" .;:,\"'")


# ------------------------------------------------------------------ entradas
def tema(item: str) -> dict:
    programa = read_json(PROGRAMA)
    row = next((r for r in programa["items"] if r["id"] == item), None)
    if row is None:
        raise ValueError(f"Item fora do programa: {item}")
    perfil = read_json(ROOT / row["profile"])
    escopo = re.sub(r"\bAs questões devem abordar\b", "As questões podem abordar",
                    perfil["topic"]["escopo"], count=1, flags=re.I)
    return {"item": item, "area": row["area"], "tema": row["subtopico"],
            "titulo": perfil["topic"]["titulo"], "escopo": escopo}


def blocos(item: str, docs: Path = DOCS) -> tuple[dict, list[dict]]:
    doc = read_json(docs / item / "documento.json")
    out = []
    for ci, cap in enumerate(doc["capitulos"]):
        for bi, b in enumerate(cap["blocos"]):
            out.append({"indice": len(out), "capitulo": ci, "bloco": bi, "titulo_capitulo": cap["titulo"],
                        "subtitulo": b["subtitulo"], "texto": b["texto"]})
    if len(out) < 3:
        raise ValueError(f"{item}: documento com menos de três blocos")
    return doc, out


def janela(bs: list[dict], i: int) -> list[tuple[str, dict]]:
    """Três blocos consecutivos na ordem do documento; nas pontas, os dois vizinhos do mesmo lado."""
    inicio = min(max(i - 1, 0), len(bs) - 3)
    trio = bs[inicio:inicio + 3]
    apoios = iter(("A1", "A2"))
    return [("F" if b["indice"] == i else next(apoios), b) for b in trio]


def render_janela(jan: list[tuple[str, dict]]) -> str:
    return "\n\n".join(f"[{r}] {b['titulo_capitulo']} / {b['subtitulo']}\n{b['texto']}" for r, b in jan)


def carregar_prompt(minimo: int, maximo: int, caminho: Path = PROMPT, min_dificeis: int = 0,
                    min_medias: int = 0, composicao: dict | None = None) -> tuple[str, str, str]:
    texto = caminho.read_text(encoding="utf-8")
    if "{{COMPOSICAO}}" in texto:
        if not composicao:
            raise ValueError(f"{caminho.name} exige uma composição de dificuldades")
        texto = texto.replace("{{COMPOSICAO}}", texto_composicao(composicao))
    if "{{EXIGENCIA" in texto and (min_dificeis not in NUM_F or min_medias not in (0, *NUM_F)):
        raise ValueError(f"{caminho.name} exige --min-dificeis entre 1 e 4 (e --min-medias entre 0 e 4)")
    pos = texto.find("\n<tema>")
    if pos < 0:
        raise ValueError("Prompt sem a seção de dados <tema>")
    system = (texto[:pos].strip()
              .replace("{{MINIMO_QUESTOES}}", str(minimo))
              .replace("{{MINIMO_MENOS_UM}}", str(minimo - 1))
              .replace("{{MAXIMO_QUESTOES}}", str(maximo))
              .replace("{{QUANTIDADE}}", str(minimo) if minimo == maximo else f"de {minimo} a {maximo}")
              .replace("{{EXIGENCIA}}", exigencia(min_medias, min_dificeis))
              .replace("{{EXIGENCIA_M}}", exigencia(min_medias, min_dificeis, masculino=True)))
    if "{{" in system:
        raise ValueError("Marcador não preenchido nas instruções: " + re.findall(r"\{\{\w+\}\}", system)[0])
    return system, texto[pos:].strip(), sha(texto)


def preencher(modelo_usuario: str, t: dict, orientacao: str, existentes: str, jan, exemplos: str = "",
              plano: str = "") -> str:
    valores = {"AREA": t["area"], "TEMA": t["tema"], "FRASE_ESPECIALISTA_COM_PODEM": t["escopo"],
               "ORIENTACAO_DIFICULDADE": orientacao, "QUESTOES_EXISTENTES": existentes,
               "EXEMPLOS": exemplos, "PLANO": plano, "JANELA": render_janela(jan)}
    out = modelo_usuario
    for k, v in valores.items():
        out = out.replace("{{" + k + "}}", v)
    if "{{" in out:
        raise ValueError("Marcador não preenchido nos dados: " + re.findall(r"\{\{\w+\}\}", out)[0])
    return re.sub(r"\n{3,}", "\n\n", out)


def selecionar_focos(n_blocos: int, quantidade: int | None) -> list[int]:
    """Focos espaçados uniformemente ao longo do documento (mesmos para todas as condições)."""
    if not quantidade or quantidade >= n_blocos:
        return list(range(n_blocos))
    if quantidade == 1:
        return [n_blocos // 2]
    return sorted({round(k * (n_blocos - 1) / (quantidade - 1)) for k in range(quantidade)})


def existentes_por_foco(anteriores: Path | None) -> dict:
    if anteriores is None:
        return {}
    out: dict[tuple[str, int], list[str]] = {}
    with (anteriores / "questoes.jsonl").open(encoding="utf-8") as f:
        for linha in f:
            q = json.loads(linha)
            out.setdefault((q["item"], q["foco"]), []).append(f"- {q['conhecimento']} | Resposta: {q['resposta']}")
    return out


# ------------------------------------------------------------------ validação estrutural
def _fundamentos(fs, k: int, nome: str = "Questão") -> None:
    if not isinstance(fs, list) or not fs:
        raise ValueError(f"{nome} {k}: informe ao menos um fundamento.")
    for f in fs:
        if not isinstance(f, dict) or set(f) != {"bloco", "trecho"} or f["bloco"] not in ROTULOS \
                or not isinstance(f["trecho"], str) or not f["trecho"].strip():
            raise ValueError(f"{nome} {k}: fundamento deve ser {{\"bloco\": A1|F|A2, \"trecho\": texto}}.")


def _quantidade(status: str, n: int, dificeis: int, minimo: int, maximo: int, min_dificeis: int,
                vazio: str, motivo: str, nome: str, medias: int = 0, min_medias: int = 0) -> None:
    if n > maximo:
        raise ValueError(f"Entregue no máximo {maximo} {nome}.")
    completo = n >= minimo and dificeis >= min_dificeis and medias >= min_medias
    if status == "ok" and not completo:
        exig = f"pelo menos {minimo} {nome}" + (f" com {min_medias} média(s)" if min_medias else "") \
            + (f" e {min_dificeis} difícil(eis)" if min_dificeis else "")
        raise ValueError(f"status ok exige {exig}; caso contrário, use parcial e explique em motivo.")
    if status == "parcial" and (n == 0 or completo):
        raise ValueError(f"status parcial exige de 1 a {maximo} {nome} sem atingir a quantidade ou as dificuldades exigidas.")
    if status == vazio and n:
        raise ValueError(f"status {vazio} exige lista vazia.")
    if status != "ok" and not motivo.strip():
        raise ValueError("Explique em motivo por que [F] não sustenta mais.")


def validar(data: dict, minimo: int, maximo: int, min_dificeis: int = 0, min_medias: int = 0,
            composicao: dict | None = None) -> None:
    """Somente formato: erros aqui fazem o cliente pedir ao modelo a correção do JSON."""
    if not isinstance(data, dict) or set(data) != {"status", "motivo", "questoes"}:
        raise ValueError("Use exatamente as chaves status, motivo e questoes.")
    status, motivo, qs = data["status"], data["motivo"], data["questoes"]
    if status not in STATUS:
        raise ValueError("status deve ser ok, parcial ou sem_questoes.")
    if not isinstance(motivo, str) or not isinstance(qs, list):
        raise ValueError("motivo deve ser texto e questoes deve ser lista.")
    for k, q in enumerate(qs, 1):
        if not isinstance(q, dict) or set(q) != set(CAMPOS):
            raise ValueError(f"Questão {k}: use exatamente os campos {', '.join(CAMPOS)}.")
        if q["id"] != k:
            raise ValueError(f"Questão {k}: id deve ser {k}.")
        if q["dificuldade"] not in DIFICULDADES:
            raise ValueError(f"Questão {k}: dificuldade inválida.")
        if q["tipo_demanda"] not in DEMANDAS:
            raise ValueError(f"Questão {k}: tipo_demanda inválido.")
        for campo in ("conhecimento", "pergunta", "resposta"):
            if not isinstance(q[campo], str) or not q[campo].strip():
                raise ValueError(f"Questão {k}: {campo} vazio.")
        _fundamentos(q["fundamentos"], k)
    if composicao:
        _composicao(status, qs, composicao, motivo)
        return
    _quantidade(status, len(qs), sum(q["dificuldade"] == "dificil" for q in qs), minimo, maximo, min_dificeis,
                "sem_questoes", motivo, "questões", sum(q["dificuldade"] == "media" for q in qs), min_medias)


def _composicao(status: str, qs: list[dict], comp: dict, motivo: str) -> None:
    contagem = {d: sum(q["dificuldade"] == d for q in qs) for d in DIFICULDADES}
    excesso = [d for d in DIFICULDADES if contagem[d] > comp.get(d, 0)]
    if excesso:
        raise ValueError(f"Não ultrapasse a composição pedida ({texto_composicao(comp)}); excesso em: "
                         + ", ".join(excesso) + ".")
    exata = all(contagem[d] == comp.get(d, 0) for d in DIFICULDADES)
    if status == "ok" and not exata:
        raise ValueError(f"status ok exige exatamente {texto_composicao(comp)}; caso contrário, use parcial.")
    if status == "parcial" and (not qs or exata):
        raise ValueError("status parcial exige ao menos uma questão, sem completar a composição.")
    if status == "sem_questoes" and qs:
        raise ValueError("status sem_questoes exige lista vazia.")
    if status != "ok" and not motivo.strip():
        raise ValueError("Explique em motivo por que [F] não sustenta a composição pedida.")


def validar_plano(data: dict, minimo: int, maximo: int, min_dificeis: int = 0, min_medias: int = 0) -> None:
    if not isinstance(data, dict) or set(data) != {"status", "motivo", "itens"}:
        raise ValueError("Use exatamente as chaves status, motivo e itens.")
    status, motivo, itens = data["status"], data["motivo"], data["itens"]
    if status not in ("ok", "parcial", "sem_alvos"):
        raise ValueError("status deve ser ok, parcial ou sem_alvos.")
    if not isinstance(motivo, str) or not isinstance(itens, list):
        raise ValueError("motivo deve ser texto e itens deve ser lista.")
    for k, it in enumerate(itens, 1):
        if not isinstance(it, dict) or set(it) != set(CAMPOS_PLANO):
            raise ValueError(f"Item {k}: use exatamente os campos {', '.join(CAMPOS_PLANO)}.")
        if it["id"] != k:
            raise ValueError(f"Item {k}: id deve ser {k}.")
        if it["dificuldade"] not in DIFICULDADES or it["tipo_demanda"] not in DEMANDAS:
            raise ValueError(f"Item {k}: dificuldade ou tipo_demanda inválido.")
        for campo in ("alvo", "resposta_esperada", "exigencia_cognitiva"):
            if not isinstance(it[campo], str) or not it[campo].strip():
                raise ValueError(f"Item {k}: {campo} vazio.")
        if not isinstance(it["condicoes_necessarias"], list) or \
                not all(isinstance(c, str) for c in it["condicoes_necessarias"]):
            raise ValueError(f"Item {k}: condicoes_necessarias deve ser lista de textos.")
        _fundamentos(it["fundamentos"], k, "Item")
    _quantidade(status, len(itens), sum(i["dificuldade"] == "dificil" for i in itens), minimo, maximo,
                min_dificeis, "sem_alvos", motivo, "alvos", sum(i["dificuldade"] == "media" for i in itens),
                min_medias)


def validar_redacao(data: dict, ids: list[int]) -> None:
    if not isinstance(data, dict) or set(data) != {"status", "motivo", "questoes"}:
        raise ValueError("Use exatamente as chaves status, motivo e questoes.")
    status, motivo, qs = data["status"], data["motivo"], data["questoes"]
    if status not in STATUS or not isinstance(motivo, str) or not isinstance(qs, list):
        raise ValueError("status deve ser ok, parcial ou sem_questoes; motivo texto; questoes lista.")
    vistos = []
    for q in qs:
        if not isinstance(q, dict) or set(q) != {"id", "pergunta", "resposta"}:
            raise ValueError("Cada questão deve ter exatamente id, pergunta e resposta.")
        if q["id"] not in ids or q["id"] in vistos:
            raise ValueError(f"id {q['id']} não está no plano ou está repetido.")
        vistos.append(q["id"])
        for campo in ("pergunta", "resposta"):
            if not isinstance(q[campo], str) or not q[campo].strip():
                raise ValueError(f"Questão {q['id']}: {campo} vazio.")
    if vistos != sorted(vistos):
        raise ValueError("Mantenha a ordem do plano.")
    n = len(qs)
    if status == "ok" and n != len(ids):
        raise ValueError("status ok exige todos os itens do plano; caso contrário, use parcial e explique.")
    if status == "parcial" and not 1 <= n < len(ids):
        raise ValueError("status parcial exige ao menos um e não todos os itens.")
    if status == "sem_questoes" and n:
        raise ValueError("status sem_questoes exige lista vazia.")
    if status != "ok" and not motivo.strip():
        raise ValueError("Explique em motivo os IDs deixados de fora e o impedimento.")


# ------------------------------------------------------------------ métricas descritivas
def verificar(q: dict, textos: dict[str, str]) -> dict:
    alvo = {r: normalizar(t) for r, t in textos.items()}
    literais = [normalizar(f["trecho"]) in alvo.get(f["bloco"], "") for f in q["fundamentos"]]
    return {
        "fundamentos_literais": all(literais),
        "ancora_em_F": any(ok and f["bloco"] == "F" for ok, f in zip(literais, q["fundamentos"])),
        "usa_apoio": any(f["bloco"] != "F" for f in q["fundamentos"]),
        "palavras_pergunta": palavras(q["pergunta"]),
        "palavras_resposta": palavras(q["resposta"]),
        "resposta_ate_50": palavras(q["resposta"]) <= 50,
    }


def _tokens(texto: str) -> set[str]:
    return {w for w in re.findall(r"\w+", normalizar(texto)) if len(w) > 3}


def semelhanca(texto: str, exemplos: list[dict]) -> float:
    """Maior Jaccard lexical entre a questão gerada e os exemplos recebidos na chamada."""
    t = _tokens(texto)
    vals = [len(t & e) / len(t | e) for e in (_tokens(x["pergunta"] + " " + x["resposta"]) for x in exemplos)
            if t and e]
    return round(max(vals), 3) if vals else 0.0


def quase_duplicadas(qs: list[dict], limiar: float = 0.6) -> list[dict]:
    """Pares no mesmo documento com alta sobreposição lexical (Jaccard) de pergunta + resposta."""
    toks = [(q, _tokens(q["pergunta"] + " " + q["resposta"])) for q in qs]
    out = []
    for (a, ta), (b, tb) in combinations(toks, 2):
        if a["item"] != b["item"] or not ta or not tb:
            continue
        j = len(ta & tb) / len(ta | tb)
        if j >= limiar:
            out.append({"item": a["item"], "a": a["uid"], "b": b["uid"], "jaccard": round(j, 3)})
    return sorted(out, key=lambda r: -r["jaccard"])


# ------------------------------------------------------------------ execução
class Piloto:
    def __init__(self, saida: Path, itens: list[str], modelo: str, *, minimo: int = 6, maximo: int = 8,
                 max_tokens: int = 16000, orientacao: str = SEM_PREFERENCIA, anteriores: Path | None = None,
                 workers: int = 4, limite: int | None = None, docs: Path = DOCS, prompt: Path = PROMPT,
                 client=None, dry_run: bool = False, progress=print, condicao: str = "A",
                 janelas_por_item: int | None = None, externos: Path | None = None,
                 especialista: Path | None = None, modo: str = "junto", min_dificeis: int = 0, min_medias: int = 0,
                 prompt_plano: Path = PROMPT_PLANO, prompt_redacao: Path = PROMPT_REDACAO,
                 composicao: dict | None = None, limpos: Path | None = None):
        if minimo < 1 or maximo < minimo:
            raise ValueError("Use 1 <= minimo <= maximo")
        if modo not in MODOS:
            raise ValueError(f"Modo desconhecido: {modo}")
        if min_dificeis < 0 or min_medias < 0 or min_dificeis + min_medias > minimo:
            raise ValueError("Use min_dificeis + min_medias <= minimo")
        self.modo, self.min_dificeis, self.min_medias = modo, min_dificeis, min_medias
        self.composicao = dict(composicao) if composicao else None
        if self.composicao and (minimo != sum(self.composicao.values()) or maximo != minimo):
            raise ValueError("Com composição, use minimo = maximo = total da composição")
        self.caminho_limpos, self.fonte_externos = (Path(limpos) if limpos else None), None
        self.prompt_plano, self.prompt_redacao = Path(prompt_plano), Path(prompt_redacao)
        from . import exemplos as ex
        if condicao not in ex.CONDICOES:
            raise ValueError(f"Condição desconhecida: {condicao}")
        self.ex, self.condicao, self.janelas_por_item = ex, condicao, janelas_por_item
        self.caminho_externos = Path(externos) if externos else ex.EXTERNOS
        self.caminho_especialista = Path(especialista) if especialista else ex.ESPECIALISTA
        self.pool_externos = self.banco_especialista = None
        self.saida, self.itens, self.modelo = Path(saida), itens, modelo
        self.minimo, self.maximo, self.max_tokens = minimo, maximo, max_tokens
        self.orientacao, self.anteriores = orientacao, (Path(anteriores) if anteriores else None)
        self.workers, self.limite, self.docs, self.prompt = workers, limite, Path(docs), Path(prompt)
        self.client, self.dry_run, self.progress = client, dry_run, progress
        self.lock = threading.Lock()

    def _prompts(self) -> dict:
        """Instruções (system), modelo dos dados (user) e hash de cada etapa do modo."""
        if self.modo == "junto":
            etapas = {"junto": self.prompt}
        else:
            etapas = {"planejamento": self.prompt_plano, "redacao": self.prompt_redacao}
        return {nome: carregar_prompt(self.minimo, self.maximo, caminho, self.min_dificeis, self.min_medias,
                                      self.composicao)
                for nome, caminho in etapas.items()}

    def _config(self, prompt_sha: str) -> None:
        etapas = ({"junto": self.prompt} if self.modo == "junto" else
                  {"planejamento": self.prompt_plano, "redacao": self.prompt_redacao})
        cfg = {"schema": "piloto-janela-v1", "modelo": self.modelo, "minimo": self.minimo,
               "maximo": self.maximo, "max_tokens": self.max_tokens, "orientacao": self.orientacao,
               "anteriores": str(self.anteriores) if self.anteriores else None,
               "documentos": self.docs.resolve().relative_to(ROOT).as_posix(),
               "prompt": {k: v.resolve().relative_to(ROOT).as_posix() for k, v in etapas.items()}
               if self.modo == "separado" else self.prompt.resolve().relative_to(ROOT).as_posix(),
               "prompt_sha256": prompt_sha,
               "condicao": self.condicao, "janelas_por_item": self.janelas_por_item}
        if self.modo != "junto" or self.min_dificeis or self.min_medias:
            cfg.update(modo=self.modo, min_dificeis=self.min_dificeis, min_medias=self.min_medias)
        if self.composicao:
            cfg.update(modo=self.modo, composicao=self.composicao)
        if self.fonte_externos:
            arq = Path(self.fonte_externos)
            cfg["exemplos_externos"] = {"arquivo": arq.resolve().relative_to(ROOT).as_posix()
                                        if arq.resolve().is_relative_to(ROOT) else str(arq),
                                        "sha256": hashlib.sha256(arq.read_bytes()).hexdigest()}
        path = self.saida / "config.json"
        if path.exists():
            antigo = read_json(path)
            fixos = {k: v for k, v in antigo.items() if k not in ("itens", "criado_em")}
            if fixos != cfg:
                diff = sorted(k for k in set(fixos) | set(cfg) if fixos.get(k) != cfg.get(k))
                raise ValueError(f"Configuração diferente da pasta existente ({', '.join(diff)}); use outra --saida")
            cfg["itens"] = sorted(set(antigo.get("itens", [])) | set(self.itens))
            cfg["criado_em"] = antigo.get("criado_em")
        else:
            cfg["itens"] = sorted(self.itens)
            cfg["criado_em"] = datetime.now(timezone.utc).isoformat()
        if not self.dry_run:
            atomic_json(path, cfg)

    def _cliente(self):
        if self.client is None:
            from pipeline.inventario.llm import LLMClient, load_dotenv
            load_dotenv(ROOT)
            model, effort = self.modelo.rsplit(":", 1) if ":" in self.modelo else (self.modelo, "")
            self.client = LLMClient(model, effort, self.saida / ".local" / "geracao.sqlite3",
                                    self.saida / "chamadas_llm.jsonl", provider="azure", max_attempts=3,
                                    timeout=600, max_tokens_cap=32000, max_calls=100000,
                                    response_dir=self.saida / ".local" / "respostas_brutas")
        return self.client

    def tarefas(self) -> list[dict]:
        out = []
        for item in self.itens:
            t = tema(item)
            doc, bs = blocos(item, self.docs)
            if doc["titulo"] != t["titulo"]:
                raise ValueError(f"{item}: documento não corresponde ao tópico do programa")
            focos = selecionar_focos(len(bs), self.janelas_por_item)
            for i in focos[: self.limite or None]:
                out.append({"item": item, "tema": t, "blocos": bs, "foco": i})
        return out

    def _carregar_exemplos(self) -> None:
        if self.condicao in ("B", "D") and self.pool_externos is None:
            self.pool_externos = self.ex.carregar_externos(self.caminho_externos)
        if self.condicao in ("E", "EC") and self.pool_externos is None:
            self.pool_externos, self.fonte_externos = self.ex.carregar_limpos(self.caminho_limpos)
        if self.condicao in ("C", "D", "EC") and self.banco_especialista is None:
            self.banco_especialista = self.ex.carregar_especialista(self.caminho_especialista)

    def _exemplos(self, t) -> list[dict]:
        return self.ex.exemplos_da_janela(self.condicao, t["item"], t["foco"],
                                          self.pool_externos, self.banco_especialista)

    def run(self) -> dict:
        prompts = self._prompts()
        prompt_sha = sha("|".join(p[2] for p in prompts.values()))
        system, modelo_usuario = prompts[next(iter(prompts))][:2]
        self._carregar_exemplos()
        self._config(prompt_sha)
        anteriores = existentes_por_foco(self.anteriores)
        tarefas = self.tarefas()
        pendentes = [t for t in tarefas if not self._arquivo(t).exists()]
        self.progress(f"Janelas: {len(tarefas)} | já concluídas: {len(tarefas) - len(pendentes)} | "
                      f"a gerar: {len(pendentes)}", flush=True)
        if self.dry_run:
            for t in pendentes:
                path = self.saida / "prompts_dry_run" / t["item"] / f"{t['foco']:03d}.txt"
                path.parent.mkdir(parents=True, exist_ok=True)
                user = self._usuario(t, modelo_usuario, anteriores)
                path.write_text(f"### SYSTEM\n{system}\n\n### USER\n{user}\n", encoding="utf-8")
            self.progress(f"Prompts gravados em {self.saida / 'prompts_dry_run'}", flush=True)
            return {}
        cliente = self._cliente()
        inicio, feitos, falhas = time.time(), 0, 0

        def um(t):
            if self.modo == "separado":
                return self._gerar_separado(t, cliente, prompts, prompt_sha, anteriores)
            return self._gerar(t, cliente, system, modelo_usuario, prompt_sha, anteriores)

        with ThreadPoolExecutor(max_workers=max(1, self.workers)) as pool:
            futuros = {pool.submit(um, t): t for t in pendentes}
            for fut in as_completed(futuros):
                t = futuros[fut]
                ok = fut.result()
                feitos += 1
                falhas += 0 if ok else 1
                gasto = time.time() - inicio
                eta = gasto / feitos * (len(pendentes) - feitos)
                self.progress(f"[{feitos}/{len(pendentes)}] {t['item']} bloco {t['foco']:03d} "
                              f"{'ok' if ok else 'FALHA'} | falhas {falhas} | restam ~{eta / 60:.1f} min",
                              flush=True)
        return resumir(self.saida)

    def _arquivo(self, t) -> Path:
        return self.saida / t["item"] / "janelas" / f"{t['foco']:03d}.json"

    def _usuario(self, t, modelo_usuario, anteriores) -> str:
        jan = janela(t["blocos"], t["foco"])
        linhas = anteriores.get((t["item"], t["foco"]), [])
        return preencher(modelo_usuario, t["tema"], self.orientacao, "\n".join(linhas) or "Nenhuma.", jan,
                         self.ex.render(self._exemplos(t)))

    def _gerar(self, t, cliente, system, modelo_usuario, prompt_sha, anteriores) -> bool:
        jan = janela(t["blocos"], t["foco"])
        exemplos = self._exemplos(t)
        user = self._usuario(t, modelo_usuario, anteriores)
        inicio = time.time()
        try:
            data = cliente.json(system, user, tag="piloto_janela", max_tokens=self.max_tokens,
                                validate=lambda d: validar(d, self.minimo, self.maximo, self.min_dificeis,
                                                           self.min_medias, self.composicao),
                                item=t["item"])
        except Exception as exc:  # noqa: BLE001 - a janela fica pendente para nova tentativa
            self._falha(t, exc)
            return False
        return self._salvar(t, jan, exemplos, user, prompt_sha, inicio, data["status"], data["motivo"],
                            data["questoes"])

    def _falha(self, t, exc) -> None:
        atomic_json(self.saida / t["item"] / "falhas" / f"{t['foco']:03d}.json",
                    {"erro": type(exc).__name__, "mensagem": str(exc)[:2000],
                     "em": datetime.now(timezone.utc).isoformat()})

    def _gerar_separado(self, t, cliente, prompts, prompt_sha, anteriores) -> bool:
        jan = janela(t["blocos"], t["foco"])
        exemplos = self._exemplos(t)
        linhas = anteriores.get((t["item"], t["foco"]), [])
        existentes = "\n".join(linhas) or "Nenhuma."
        sys_p, mod_p, _ = prompts["planejamento"]
        sys_r, mod_r, _ = prompts["redacao"]
        user_p = preencher(mod_p, t["tema"], self.orientacao, existentes, jan)
        inicio = time.time()
        try:
            plano = cliente.json(sys_p, user_p, tag="piloto_planejamento", max_tokens=self.max_tokens,
                                 validate=lambda d: validar_plano(d, self.minimo, self.maximo, self.min_dificeis,
                                                                  self.min_medias),
                                 item=t["item"])
            redacao = {"status": "sem_questoes", "motivo": "plano sem alvos", "questoes": []}
            user_r = ""
            if plano["itens"]:
                para_redacao = [{k: it[k] for k in ("id", "dificuldade", "alvo", "resposta_esperada",
                                                    "condicoes_necessarias", "fundamentos")} for it in plano["itens"]]
                user_r = preencher(mod_r, t["tema"], self.orientacao, existentes, jan, self.ex.render(exemplos),
                                   json.dumps(para_redacao, ensure_ascii=False, indent=2))
                ids = [it["id"] for it in plano["itens"]]
                redacao = cliente.json(sys_r, user_r, tag="piloto_redacao", max_tokens=self.max_tokens,
                                       validate=lambda d: validar_redacao(d, ids), item=t["item"])
        except Exception as exc:  # noqa: BLE001
            self._falha(t, exc)
            return False
        por_id = {it["id"]: it for it in plano["itens"]}
        questoes = [{"id": q["id"], "dificuldade": por_id[q["id"]]["dificuldade"],
                     "tipo_demanda": por_id[q["id"]]["tipo_demanda"], "conhecimento": por_id[q["id"]]["alvo"],
                     "pergunta": q["pergunta"], "resposta": q["resposta"],
                     "fundamentos": por_id[q["id"]]["fundamentos"]} for q in redacao["questoes"]]
        dificeis = sum(q["dificuldade"] == "dificil" for q in questoes)
        medias = sum(q["dificuldade"] == "media" for q in questoes)
        status = ("ok" if len(questoes) >= self.minimo and dificeis >= self.min_dificeis and medias >= self.min_medias
                  else "parcial" if questoes else "sem_questoes")
        motivo = " | ".join(m for m in (plano["motivo"], redacao["motivo"]) if m.strip())
        return self._salvar(t, jan, exemplos, user_p + "\n" + user_r, prompt_sha, inicio, status, motivo, questoes,
                            extra={"status_plano": plano["status"], "status_redacao": redacao["status"],
                                   "itens_planejados": len(plano["itens"]),
                                   "itens_descartados_redacao": len(plano["itens"]) - len(questoes),
                                   "plano": plano})

    def _salvar(self, t, jan, exemplos, user, prompt_sha, inicio, status, motivo, questoes, extra=None) -> bool:
        textos = {r: b["texto"] for r, b in jan}
        foco = t["blocos"][t["foco"]]
        registro = {
            "item": t["item"], "foco": t["foco"], "capitulo": foco["capitulo"], "bloco": foco["bloco"],
            "titulo_capitulo": foco["titulo_capitulo"], "subtitulo": foco["subtitulo"],
            "janela": [{"rotulo": r, "indice": b["indice"], "subtitulo": b["subtitulo"]} for r, b in jan],
            "palavras_janela": sum(palavras(b["texto"]) for _, b in jan),
            "modelo": self.modelo, "modo": self.modo, "condicao": self.condicao, "prompt_sha256": prompt_sha,
            "usuario_sha256": sha(user), "segundos": round(time.time() - inicio, 2),
            "exemplos": [{"id": e["id"], "fonte": e["fonte"], "dificuldade": e["dificuldade"]} for e in exemplos],
            "status": status, "motivo": motivo,
            "questoes": [{**q, "verificacoes": {**verificar(q, textos), "semelhanca_exemplos":
                          semelhanca(q["pergunta"] + " " + q["resposta"], exemplos)}}
                         for q in questoes],
            **(extra or {}),
        }
        atomic_json(self._arquivo(t), registro)
        falha = self.saida / t["item"] / "falhas" / f"{t['foco']:03d}.json"
        if falha.exists():
            falha.unlink()
        return True


# ------------------------------------------------------------------ resumo
def _pct(n, d):
    return round(100 * n / d, 1) if d else 0.0


def _inicio(pergunta: str) -> str:
    return " ".join(re.findall(r"\w+", normalizar(pergunta))[:2])


def _metricas(janelas: list[dict], questoes: list[dict], composicao: dict | None = None) -> dict:
    nq = len(questoes)
    inicios = Counter(_inicio(q["pergunta"]) for q in questoes)
    dif = {d: sum(q["dificuldade"] == d for q in questoes) for d in DIFICULDADES}
    return {
        "janelas": len(janelas),
        "status": {s: sum(j["status"] == s for j in janelas) for s in STATUS},
        "questoes": nq,
        "questoes_por_janela": round(nq / len(janelas), 2) if janelas else 0,
        "dificuldade": dif,
        "dificuldade_pct": {d: _pct(v, nq) for d, v in dif.items()},
        "dificuldade_alvo_pct": {d: 100 * v for d, v in ALVO_DIFICULDADE.items()},
        "tipo_demanda": {d: sum(q["tipo_demanda"] == d for q in questoes) for d in DEMANDAS},
        "fundamentos_literais_pct": _pct(sum(q["verificacoes"]["fundamentos_literais"] for q in questoes), nq),
        "ancora_em_F_pct": _pct(sum(q["verificacoes"]["ancora_em_F"] for q in questoes), nq),
        "usa_apoio_pct": _pct(sum(q["verificacoes"]["usa_apoio"] for q in questoes), nq),
        "resposta_ate_50_pct": _pct(sum(q["verificacoes"]["resposta_ate_50"] for q in questoes), nq),
        "palavras_pergunta_media": round(sum(q["verificacoes"]["palavras_pergunta"] for q in questoes) / nq, 1) if nq else 0,
        "palavras_resposta_media": round(sum(q["verificacoes"]["palavras_resposta"] for q in questoes) / nq, 1) if nq else 0,
        "segundos_por_janela": round(sum(j["segundos"] for j in janelas) / len(janelas), 1) if janelas else 0,
        "semelhanca_exemplos_media": round(sum(_sem(q) for q in questoes) / nq, 3) if nq else 0,
        "semelhanca_exemplos_max": max((_sem(q) for q in questoes), default=0),
        "semelhanca_exemplos_ge_030_pct": _pct(sum(_sem(q) >= 0.3 for q in questoes), nq),
        "janelas_com_media_pct": _pct(sum(any(q["dificuldade"] == "media" for q in j["questoes"])
                                          for j in janelas), len(janelas)),
        "janelas_com_dificil_pct": _pct(sum(any(q["dificuldade"] == "dificil" for q in j["questoes"])
                                            for j in janelas), len(janelas)),
        "itens_descartados_redacao": sum(j.get("itens_descartados_redacao", 0) for j in janelas),
        "palavras_pergunta_por_nivel": {d: round(sum(q["verificacoes"]["palavras_pergunta"] for q in questoes
                                                     if q["dificuldade"] == d) / dif[d], 1) if dif[d] else 0
                                        for d in DIFICULDADES},
        "inicios_distintos": len(inicios),
        "inicio_mais_comum": (f"{inicios.most_common(1)[0][0]} ({_pct(inicios.most_common(1)[0][1], nq)}%)"
                              if inicios else ""),
        "composicao_exata_pct": (_pct(sum(all(sum(q["dificuldade"] == d for q in j["questoes"]) == composicao.get(d, 0)
                                              for d in DIFICULDADES) for j in janelas), len(janelas))
                                 if composicao else None),
        "acima_do_teto_pct": _pct(sum(q["verificacoes"]["palavras_pergunta"] > TETO_PERGUNTA[q["dificuldade"]]
                                      for q in questoes), nq),
    }


def _sem(q: dict) -> float:
    return q["verificacoes"].get("semelhanca_exemplos", 0.0)


def _uso(saida: Path) -> dict:
    path = saida / "chamadas_llm.jsonl"
    u = {"chamadas_ok": 0, "tentativas_com_erro": 0, "reparos_de_formato": 0, "prompt_tokens": 0, "completion_tokens": 0}
    if not path.exists():
        return u
    for linha in path.read_text(encoding="utf-8").splitlines():
        r = json.loads(linha)
        if not str(r.get("tag", "")).startswith("piloto_"):
            continue
        u["prompt_tokens"] += r.get("prompt_tokens", 0) or 0
        u["completion_tokens"] += r.get("completion_tokens", 0) or 0
        if r.get("ok"):
            u["chamadas_ok"] += 1
        else:
            u["tentativas_com_erro"] += 1
            u["reparos_de_formato"] += r.get("kind") == "validacao"
    return u


def resumir(saida: Path) -> dict:
    saida = Path(saida)
    janelas = [read_json(p) for p in sorted(saida.glob("*/janelas/*.json"))]
    falhas = sorted(p.relative_to(saida).as_posix() for p in saida.glob("*/falhas/*.json"))
    questoes = []
    for j in janelas:
        for q in j["questoes"]:
            questoes.append({"uid": f"{j['item']}-{j['foco']:03d}-{q['id']}", "item": j["item"], "foco": j["foco"],
                             "capitulo": j["capitulo"], "bloco": j["bloco"], "subtitulo": j["subtitulo"],
                             "status_janela": j["status"], **q})
    dups = quase_duplicadas(questoes)
    itens = sorted({j["item"] for j in janelas})
    cfg = read_json(saida / "config.json") if (saida / "config.json").exists() else {}
    comp = cfg.get("composicao")
    resumo = {
        "saida": saida.resolve().relative_to(ROOT).as_posix() if saida.resolve().is_relative_to(ROOT) else str(saida),
        "config": read_json(saida / "config.json") if (saida / "config.json").exists() else None,
        "total": _metricas(janelas, questoes, comp),
        "por_item": {i: _metricas([j for j in janelas if j["item"] == i], [q for q in questoes if q["item"] == i],
                                  comp)
                     for i in itens},
        "quase_duplicadas": {"limiar_jaccard": 0.6, "pares": len(dups),
                             "questoes_envolvidas": len({u for d in dups for u in (d["a"], d["b"])}),
                             "exemplos": dups[:30]},
        "falhas_pendentes": falhas,
        "uso": _uso(saida),
    }
    atomic_json(saida / "resumo.json", resumo)
    with (saida / "questoes.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for q in questoes:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")
    campos = ["uid", "item", "foco", "subtitulo", "dificuldade", "tipo_demanda", "conhecimento", "pergunta",
              "resposta", "fundamentos_literais", "ancora_em_F", "usa_apoio", "palavras_resposta"]
    with (saida / "questoes.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for q in questoes:
            w.writerow({**{k: q.get(k, "") for k in campos}, **{k: q["verificacoes"][k] for k in
                        ("fundamentos_literais", "ancora_em_F", "usa_apoio", "palavras_resposta")}})
    _markdown(saida, resumo, janelas)
    return resumo


def _markdown(saida: Path, resumo: dict, janelas: list[dict]) -> None:
    t = resumo["total"]
    linhas = ["# Piloto de geração por janela", "",
              f"Modo: {(resumo['config'] or {}).get('modo', 'junto')} · "
              f"Condição: {(resumo['config'] or {}).get('condicao', 'A')} · "
              f"Modelo: `{(resumo['config'] or {}).get('modelo')}` · mínimo {(resumo['config'] or {}).get('minimo')}"
              f" · máximo {(resumo['config'] or {}).get('maximo')} questões por janela.", "",
              "| Métrica | Total | " + " | ".join(resumo["por_item"]) + " |",
              "|---|---:|" + "---:|" * len(resumo["por_item"])]

    def linha(nome, f):
        return f"| {nome} | {f(t)} | " + " | ".join(str(f(m)) for m in resumo["por_item"].values()) + " |"

    linhas += [
        linha("Janelas", lambda m: m["janelas"]),
        linha("Status ok / parcial / sem", lambda m: "{ok} / {parcial} / {sem_questoes}".format(**m["status"])),
        linha("Questões", lambda m: m["questoes"]),
        linha("Questões por janela", lambda m: m["questoes_por_janela"]),
        linha("Fácil / média / difícil (%)",
              lambda m: "{facil} / {media} / {dificil}".format(**m["dificuldade_pct"])),
        linha("Fundamentos literais (%)", lambda m: m["fundamentos_literais_pct"]),
        linha("Âncora válida em F (%)", lambda m: m["ancora_em_F_pct"]),
        linha("Usa bloco de apoio (%)", lambda m: m["usa_apoio_pct"]),
        linha("Resposta ≤ 50 palavras (%)", lambda m: m["resposta_ate_50_pct"]),
        linha("Palavras: pergunta / resposta",
              lambda m: f"{m['palavras_pergunta_media']} / {m['palavras_resposta_media']}"),
        linha("Segundos por janela", lambda m: m["segundos_por_janela"]),
        linha("Semelhança com exemplos: média / máx", lambda m: f"{m['semelhanca_exemplos_media']} / "
                                                                f"{m['semelhanca_exemplos_max']}"),
    ]
    u, d = resumo["uso"], resumo["quase_duplicadas"]
    linhas += ["", f"Alvo de dificuldade: 50 / 30 / 20. Tipos de demanda (total): "
               + ", ".join(f"{k} {v}" for k, v in t["tipo_demanda"].items()) + ".",
               f"Quase duplicadas (Jaccard ≥ {d['limiar_jaccard']} no mesmo documento): {d['pares']} pares, "
               f"{d['questoes_envolvidas']} questões.",
               f"Chamadas: {u['chamadas_ok']} ok, {u['tentativas_com_erro']} tentativas com erro "
               f"({u['reparos_de_formato']} reparos de formato). Tokens: {u['prompt_tokens']} entrada, "
               f"{u['completion_tokens']} saída.",
               f"Janelas com falha pendente: {len(resumo['falhas_pendentes'])}.", ""]
    (saida / "RESUMO.md").write_text("\n".join(linhas), encoding="utf-8")

    q = ["# Questões geradas", ""]
    for j in janelas:
        q += [f"## {j['item']} · bloco {j['foco']:03d} · {j['subtitulo']}", "",
              f"Status: `{j['status']}`" + (f" · {j['motivo']}" if j["motivo"] else ""), ""]
        if j.get("exemplos"):
            q += ["Exemplos recebidos: " + ", ".join(f"{e['id']} ({e['dificuldade']})" for e in j["exemplos"]), ""]
        for x in j["questoes"]:
            v = x["verificacoes"]
            marcas = [] if v["ancora_em_F"] else ["sem âncora literal em F"]
            if v["usa_apoio"]:
                marcas.append("usa apoio")
            q += [f"**{x['id']}. [{x['dificuldade']} · {x['tipo_demanda']}]** {x['pergunta']}", "",
                  f"Resposta: {x['resposta']}" + (f"  \n_{'; '.join(marcas)}_" if marcas else ""), ""]
    (saida / "QUESTOES.md").write_text("\n".join(q), encoding="utf-8")


# ------------------------------------------------------------------ comparação entre condições
DESCRICAO_CONDICOES = {
    "A": "sem exemplos",
    "B": "3 externos (Pirá, ARC-Challenge, HotpotQA)",
    "C": "3 aprovadas pelo especialista, de outras áreas",
    "D": "B + C (6 exemplos)",
}


DESCRICAO_MODOS = {
    "E": "6 exemplos externos",
    "EC": "6 exemplos externos + 3 questões já geradas (especialista)",
    "junto": "planejamento e redação no mesmo prompt",
    "separado": "planejamento e redação em chamadas separadas",
}


def comparar(raiz: Path, condicoes=("A", "B", "C", "D"), descricoes=None, titulo=None) -> dict:
    raiz = Path(raiz)
    descricoes = descricoes or {**DESCRICAO_CONDICOES, **DESCRICAO_MODOS}
    res = {c: resumir(raiz / c) for c in condicoes if (raiz / c / "config.json").exists()}
    linhas = [f"# {titulo or 'Experimento de exemplos de forma'}", "",
              "Mesmas janelas em todas as variantes.", "",
              "| Métrica | " + " | ".join(f"{c}: {descricoes.get(c, c)}" for c in res) + " |",
              "|---|" + "---:|" * len(res)]

    def linha(nome, f):
        return f"| {nome} | " + " | ".join(str(f(r["total"])) for r in res.values()) + " |"

    linhas += [
        linha("Janelas", lambda m: m["janelas"]),
        linha("ok / parcial / sem", lambda m: "{ok} / {parcial} / {sem_questoes}".format(**m["status"])),
        linha("Questões", lambda m: m["questoes"]),
        linha("Questões por janela", lambda m: m["questoes_por_janela"]),
        linha("Fácil / média / difícil (%) · alvo 50/30/20",
              lambda m: "{facil} / {media} / {dificil}".format(**m["dificuldade_pct"])),
        linha("Recordar / inferir / diagnosticar / comparar / decidir",
              lambda m: " / ".join(str(m["tipo_demanda"][d]) for d in DEMANDAS)),
        linha("Fundamentos literais (%)", lambda m: m["fundamentos_literais_pct"]),
        linha("Âncora válida em F (%)", lambda m: m["ancora_em_F_pct"]),
        linha("Usa bloco de apoio (%)", lambda m: m["usa_apoio_pct"]),
        linha("Resposta ≤ 50 palavras (%)", lambda m: m["resposta_ate_50_pct"]),
        linha("Palavras: pergunta / resposta",
              lambda m: f"{m['palavras_pergunta_media']} / {m['palavras_resposta_media']}"),
        linha("Semelhança com exemplos: média / máx",
              lambda m: f"{m['semelhanca_exemplos_media']} / {m['semelhanca_exemplos_max']}"),
        linha("Semelhança ≥ 0,30 (%)", lambda m: m["semelhanca_exemplos_ge_030_pct"]),
        linha("Segundos por janela", lambda m: m["segundos_por_janela"]),
        linha("Janelas com ao menos uma média / uma difícil (%)",
              lambda m: f"{m.get('janelas_com_media_pct', 0)} / {m.get('janelas_com_dificil_pct', 0)}"),
        linha("Palavras da pergunta: fácil / média / difícil",
              lambda m: " / ".join(str(m.get("palavras_pergunta_por_nivel", {}).get(d, 0)) for d in DIFICULDADES)),
        linha("Acima do tamanho pedido (%) · 35/60/90", lambda m: m.get("acima_do_teto_pct", 0)),
        linha("Itens do plano descartados na redação", lambda m: m.get("itens_descartados_redacao", 0)),
        linha("Janelas com a composição exata (%)", lambda m: m.get("composicao_exata_pct")),
        linha("Inícios de pergunta distintos (2 primeiras palavras)", lambda m: m.get("inicios_distintos", 0)),
        linha("Início mais comum", lambda m: m.get("inicio_mais_comum", "")),
    ]
    linhas += ["| Quase duplicadas (pares) | " + " | ".join(str(r["quase_duplicadas"]["pares"]) for r in res.values())
               + " |",
               "| Tokens entrada / saída | " + " | ".join(f"{r['uso']['prompt_tokens']} / {r['uso']['completion_tokens']}"
                                                        for r in res.values()) + " |",
               "| Falhas pendentes | " + " | ".join(str(len(r["falhas_pendentes"])) for r in res.values()) + " |",
               "", "A semelhança com exemplos é a sobreposição lexical (Jaccard) com os pares recebidos na chamada. "
               "Exemplos em inglês (ARC, HotpotQA) quase não se sobrepõem por palavras; para eles, a leitura de "
               "`QUESTOES.md` é que mostra se a estrutura foi copiada.", ""]
    (raiz / "COMPARACAO.md").write_text("\n".join(linhas), encoding="utf-8")
    atomic_json(raiz / "comparacao.json", {c: r["total"] for c, r in res.items()})
    return res
