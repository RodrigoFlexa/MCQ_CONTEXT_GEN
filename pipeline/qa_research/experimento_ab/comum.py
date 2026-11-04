"""Definições compartilhadas do experimento A/B (documento x unidade de contexto).

Braços (mesmo gerador v21, mesmos 3 documentos, nada herdado de rodadas anteriores):
  A: documento antigo,   janela de 3 blocos
  B: documento refinado, janela de 3 blocos
  C: documento antigo,   capítulo do bloco foco   (reaproveita o inventário de A: mesmo documento)
  D: documento refinado, capítulo do bloco foco   (reaproveita o inventário de B: mesmo documento)
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pipeline.qa_research.piloto_janela.core import QA, ROOT, atomic_json, blocos, janela, read_json

ITENS = ("02_02", "03_03", "07_01")
BRACOS = {
    "A": {"docs": "antigo", "unidade": "janela", "reusar": None},
    "B": {"docs": "refinado", "unidade": "janela", "reusar": None},
    "C": {"docs": "antigo", "unidade": "capitulo", "reusar": "A"},
    "D": {"docs": "refinado", "unidade": "capitulo", "reusar": "B"},
}
UNIDADES = ("janela", "capitulo")
EXPERIMENTO = QA / "relatorios" / "experimento_ab_v1"
FONTE_DOCS = QA / "relatorios" / "qa_continuo_v2" / "contextos"   # snapshot dos documentos usados no piloto
GERACAO_FINAL = QA / "relatorios" / "geracao_final_20261024T204734Z"
E5_CACHE = ROOT / "docs" / "analise_diversidade_geracao_final_20261024" / "embeddings_perguntas.npz"
PROMPTS = Path(__file__).resolve().parent / "prompts"
PROMPTS_GAP = QA / "benchmark_gap_prompts"

# Embeddings disponíveis no servidor (deployment, modelo, dimensão). O ada-002 fica fora: geração anterior.
EMBEDDINGS = {
    "3-small": {"deployment": "embedding-3-small-global", "modelo": "text-embedding-3-small", "dimensoes": 1536},
    "3-large": {"deployment": "embedding-3-large-global", "modelo": "text-embedding-3-large", "dimensoes": 3072},
}
# Rótulo de referência da calibração e juízes candidatos da deduplicação (do mais barato ao mais caro).
REFERENCIA = "gpt-5-4-petrobras:high"
JUIZES = {"gpt-5-4-nano": "gpt-5-4-nano-petrobras:low", "gpt-4-1-mini": "gpt-4-1-mini-petrobras",
          "gpt-5-mini": "gpt-5-mini-petrobras:low"}
SUSTENTACAO = "gpt-5-4-petrobras:medium"   # mesmo juiz da auditoria de sustentação do benchmark_gap
REPARO = "gpt-5-4-petrobras:high"


def prompt(nome: str) -> str:
    return (PROMPTS / f"{nome}.md").read_text(encoding="utf-8").strip()


def prompt_gap(nome: str) -> str:
    return (PROMPTS_GAP / f"{nome}.md").read_text(encoding="utf-8").strip()


def sha(obj) -> str:
    texto = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def linhas(path: Path) -> list[dict]:
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def gravar_jsonl(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    tmp.replace(path)


def texto_questao(q: dict) -> str:
    """Texto usado nos embeddings: a redundância é de conhecimento, então pergunta e resposta entram juntas."""
    return f"Pergunta: {q['pergunta']}\nResposta: {q['resposta']}"


# ------------------------------------------------------------------ contexto por unidade
def contexto_foco(bs: list[dict], foco: int, unidade: str) -> list[tuple[str, dict]]:
    """Blocos que o gerador vê para um bloco foco, com os rótulos do prompt.

    janela: três blocos consecutivos (F e vizinhos A1/A2, como na v21).
    capitulo: todos os blocos do capítulo do foco, em ordem; F no foco e A1..An nos demais.
    """
    if unidade == "janela":
        return janela(bs, foco)
    if unidade != "capitulo":
        raise ValueError(f"Unidade inválida: {unidade}")
    cap = bs[foco]["capitulo"]
    out, k = [], 0
    for b in bs:
        if b["capitulo"] != cap:
            continue
        if b["indice"] == foco:
            out.append(("F", b))
        else:
            k += 1
            out.append((f"A{k}", b))
    return out


def indices_geracao(q: dict, bs: list[dict], unidade: str) -> list[int]:
    """Índices dos blocos que o gerador recebeu para esta questão (janela/capítulo do foco ou blocos da composta)."""
    if q.get("foco") is not None:
        return [b["indice"] for _, b in contexto_foco(bs, q["foco"], unidade)]
    ids = q.get("blocos") or []
    if not ids or len(set(ids)) != len(ids) or any(type(i) is not int or not 0 <= i < len(bs) for i in ids):
        raise ValueError("Questão sem vínculo de contexto válido: " + q.get("uid", "?"))
    return list(ids)


def indices_avaliacao(q: dict, bs: list[dict], unidade: str) -> list[int]:
    """Contexto comum da avaliação: os capítulos inteiros tocados pelo contexto de geração.

    O mesmo critério vale para os quatro braços; assim comparamos a geração, e não o tamanho do contexto dado ao
    respondente. Uma janela que cruza a fronteira de capítulos leva os dois capítulos.
    """
    caps = {bs[i]["capitulo"] for i in indices_geracao(q, bs, unidade)}
    return [b["indice"] for b in bs if b["capitulo"] in caps]


def relativo(p: Path) -> str:
    """Caminho relativo à raiz do repositório (resultados legíveis no servidor e na máquina local)."""
    p = Path(p).resolve()
    return p.relative_to(ROOT).as_posix() if ROOT in p.parents else str(p)


def resolver(p: str) -> Path:
    q = Path(p)
    return q if q.is_absolute() else ROOT / q


def palavras_documento(bs: list[dict]) -> int:
    return sum(len(b["texto"].split()) for b in bs)


# ------------------------------------------------------------------ preparação dos documentos
def preparar_documentos(saida: Path, itens=ITENS, fonte: Path = FONTE_DOCS) -> dict:
    """Copia o snapshot antigo/refinado para a pasta do experimento e registra os hashes (sem chamadas de API)."""
    saida = Path(saida)
    manifesto = {"fonte": str(fonte.relative_to(ROOT)) if ROOT in fonte.resolve().parents else str(fonte),
                 "itens": list(itens), "documentos": {}}
    for cond in ("antigo", "refinado"):
        for item in itens:
            doc = read_json(fonte / cond / item / "documento.json")
            _, bs = blocos(item, fonte / cond)
            manifesto["documentos"][f"{cond}/{item}"] = {
                "sha256": sha(doc), "blocos": len(bs), "capitulos": len(doc["capitulos"]),
                "palavras": palavras_documento(bs)}
    destino = saida / "docs"
    arq = destino / "manifesto.json"
    if arq.exists() and read_json(arq)["documentos"] != manifesto["documentos"]:
        raise ValueError("Documentos mudaram em relação à preparação existente; use outra pasta de experimento")
    for cond in ("antigo", "refinado"):
        for item in itens:
            atomic_json(destino / cond / item / "documento.json", read_json(fonte / cond / item / "documento.json"))
    atomic_json(arq, manifesto)
    return manifesto


def docs_do_braco(exp: Path, braco: str) -> Path:
    return Path(exp) / "docs" / BRACOS[braco]["docs"]


# ------------------------------------------------------------------ clientes
def cliente_llm(modelo: str, pasta: Path, papel: str):
    from pipeline.inventario.llm import LLMClient, load_dotenv
    load_dotenv(ROOT)
    model, effort = modelo.rsplit(":", 1) if ":" in modelo else (modelo, "")
    return LLMClient(model, effort, Path(pasta) / ".local" / f"{papel}.sqlite3", Path(pasta) / "chamadas" / f"{papel}.jsonl",
                     provider="azure", max_attempts=3, timeout=600, max_tokens_cap=32000, max_calls=200000,
                     response_dir=Path(pasta) / ".local" / "respostas" / papel)


MAX_CARACTERES = 20000   # bem abaixo do limite de 8.191 tokens; questões têm poucas centenas de caracteres


class EmbedderDireto:
    """Embeddings Azure de textos curtos, enviados como string (sem tokenizador local e sem tiktoken).

    Cache sqlite por conteúdo (deployment + dimensão + texto), lotes de 64, novas tentativas em erro transitório,
    orçamento persistente de chamadas e log em <pasta>/chamadas/embeddings_<nome>.jsonl.
    """

    def __init__(self, nome: str, pasta: Path, max_chamadas: int = 20000, client=None, sleep=None, lote: int = 64):
        import sqlite3
        import threading
        import time
        from pipeline.qa_research.runtime import PersistentBudget
        e = EMBEDDINGS[nome]
        self.nome, self.deployment, self.dimensoes, self.lote = nome, e["deployment"], e["dimensoes"], lote
        self.sleep = sleep or time.sleep
        self.lock = threading.RLock()
        pasta = Path(pasta)
        if client is None:
            from pipeline.inventario.llm import load_dotenv
            load_dotenv(ROOT)
            from azure_openai_backend import AzureOpenAIBackend, AzureSettings
            from openai import AzureOpenAI
            s = AzureSettings.load()
            s.require()
            kw = dict(api_key=s.azure_api_key, api_version=s.azure_api_version, timeout=120, max_retries=0)
            kw["base_url" if s.use_base_url else "azure_endpoint"] = s.azure_endpoint
            http = AzureOpenAIBackend._build_http_client(s.ca_bundle, 120)
            if http is not None:
                kw["http_client"] = http
            client = AzureOpenAI(**kw)
        self.client = client
        self.orcamento = PersistentBudget(pasta / ".local" / f"orcamento_embeddings_{nome}.json", max_chamadas)
        (pasta / ".local").mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(pasta / ".local" / f"embeddings_{nome}.sqlite3", check_same_thread=False, timeout=60)
        self.db.execute("CREATE TABLE IF NOT EXISTS v (k TEXT PRIMARY KEY, x BLOB NOT NULL)")
        self.db.commit()
        self.log = pasta / "chamadas" / f"embeddings_{nome}.jsonl"

    def _chave(self, texto: str) -> str:
        return sha(f"{self.deployment}|{self.dimensoes}|{texto}")

    def _get(self, k):
        import numpy as np
        row = self.db.execute("SELECT x FROM v WHERE k=?", (k,)).fetchone()
        return None if row is None else np.frombuffer(row[0], dtype=np.float32).copy()

    def _pedir(self, textos):
        import random
        import time
        from datetime import datetime, timezone
        import numpy as np
        from pipeline.inventario.llm import CallFailed, is_fatal, is_transient, retry_after
        ultimo = None
        for tentativa in range(4):
            self.orcamento.reserve()
            reg = {"em": datetime.now(timezone.utc).isoformat(), "deployment": self.deployment, "itens": len(textos),
                   "tentativa": tentativa + 1}
            inicio = time.monotonic()
            try:
                r = self.client.embeddings.create(model=self.deployment, input=list(textos), dimensions=self.dimensoes,
                                                  encoding_format="float")
                vals = {}
                for it in r.data:
                    v = np.asarray(it.embedding, dtype=np.float32)
                    if it.index in vals or not 0 <= it.index < len(textos) or v.shape != (self.dimensoes,) \
                            or not np.isfinite(v).all() or np.linalg.norm(v) < 1e-12:
                        raise ValueError("Resposta de embeddings inválida")
                    vals[it.index] = v / np.linalg.norm(v)
                if len(vals) != len(textos):
                    raise ValueError("Resposta de embeddings incompleta")
                reg["tokens"] = getattr(getattr(r, "usage", None), "total_tokens", None)
                return [vals[i] for i in range(len(textos))]
            except Exception as exc:  # noqa: BLE001 - classificado abaixo
                reg["erro"] = f"{type(exc).__name__}: {str(exc)[:300]}"
                ultimo = exc
                if is_fatal(exc) or not is_transient(exc) or tentativa == 3:
                    raise
            finally:
                reg["segundos"] = round(time.monotonic() - inicio, 3)
                self.log.parent.mkdir(parents=True, exist_ok=True)
                with self.log.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(reg, ensure_ascii=False) + "\n")
            self.sleep(min(60, max(retry_after(ultimo), 2 ** tentativa + random.random())))
        raise CallFailed("Embeddings indisponíveis") from ultimo

    def encode(self, textos):
        import numpy as np
        with self.lock:
            textos = list(textos)
            if not textos:
                return np.empty((0, self.dimensoes), dtype=np.float32)
            for t in textos:
                if not isinstance(t, str) or not t.strip():
                    raise ValueError("Embedding de texto vazio não é permitido")
                if len(t) > MAX_CARACTERES:
                    raise ValueError(f"Texto longo demais para embedding direto ({len(t)} caracteres)")
            chaves = [self._chave(t) for t in textos]
            pend = list(dict.fromkeys(t for t, k in zip(textos, chaves) if self._get(k) is None))
            for i in range(0, len(pend), self.lote):
                parte = pend[i:i + self.lote]
                for t, v in zip(parte, self._pedir(parte)):
                    self.db.execute("INSERT OR REPLACE INTO v VALUES (?,?)", (self._chave(t), v.astype(np.float32).tobytes()))
                self.db.commit()
            return np.stack([self._get(k) for k in chaves])

    def close(self):
        self.db.close()


def embedder(nome: str, pasta: Path, max_chamadas: int = 20000, client=None):
    return EmbedderDireto(nome, pasta, max_chamadas=max_chamadas, client=client)


def sem_nul(f):
    """Linhas de um CSV sem o caractere NUL: um modelo pode devolvê-lo dentro da resposta, e o módulo csv recusa a
    linha inteira ("line contains NUL")."""
    return (linha.replace("\0", "") for linha in f)
