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
from types import SimpleNamespace

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


def embedder(nome: str, pasta: Path, max_chamadas: int = 20000, client=None, tokenizer=None):
    """AzureEmbedder do repositório (cache sqlite por conteúdo, entrada sem truncamento, log de chamadas)."""
    from pipeline.qa_research.embeddings import AzureEmbedder
    from pipeline.qa_research.runtime import PersistentBudget
    e = EMBEDDINGS[nome]
    cfg = SimpleNamespace(timeout=120, max_attempts=4, embedding_model=e["modelo"], embedding_deployment=e["deployment"],
                          embedding_dimensions=e["dimensoes"], embedding_model_version="1",
                          embedding_window_tokens=8191, embedding_overlap_tokens=128, embedding_batch_size=64,
                          embedding_batch_tokens=60000, index_dir=str(Path(pasta) / ".local" / "indice"),
                          output=str(Path(pasta)))
    orc = PersistentBudget(Path(pasta) / ".local" / f"orcamento_embeddings_{nome}.json", max_chamadas)
    return AzureEmbedder(cfg, orc, client=client, tokenizer=tokenizer)
