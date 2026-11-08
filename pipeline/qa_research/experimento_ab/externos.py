"""Juiz padrão sobre respostas de modelos que não estão no Azure (Llama via vLLM na DL-28).

As respostas chegam prontas em relatorios/respostas_externas/<modelo>.jsonl (responder_vllm.py). Aqui elas entram no
mesmo motor de avaliação do dataset final v2 (LI.AvaliacaoCurta, juiz GPT-5.4 medium, lotes de 8, mesmo prompt), por
um cliente que devolve a resposta já gravada para a mesma mensagem do usuário. A avaliação fica numa pasta própria
(relatorios/avaliacao_externos), só com as questões do banco final v1: a avaliação dos modelos GPT e os estratos de
dificuldade do banco não mudam.
"""
from __future__ import annotations

from pathlib import Path

from pipeline.inventario.textutil import read_json

from . import comum as C
from .banco import SAIDA as BANCO
from .completo import SAIDA as FINAL_V2, DatasetCompleto
from .responder_vllm import SAIDA as RESPOSTAS, sha, usuario

SAIDA = C.QA / "relatorios" / "avaliacao_externos"


class RespostasProntas:
    """Cliente no lugar do respondente: a resposta gravada para a mesma mensagem do usuário (sha256)."""
    def __init__(self, arq: Path, sonda: dict | None = None):
        self.por_usuario = {r["usuario_sha256"]: r["resposta"] for r in C.linhas(arq)}
        if sonda:
            self.por_usuario.setdefault(sha(sonda["usuario"]), sonda["resposta"])
        self.chamadas = 0

    def json(self, system, user, tag="", max_tokens=0, validate=None, item=None):
        self.chamadas += 1
        k = sha(user)
        if k not in self.por_usuario:
            raise KeyError(f"sem resposta gravada para esta questão ({k[:12]}); rode o responder_vllm de novo")
        d = {"resposta": self.por_usuario[k].strip() or "(sem resposta)"}   # vazia: o juiz marca como incorreta
        if validate:
            validate(d)
        return d

    def close(self):
        pass


def disponiveis(pasta: Path = RESPOSTAS) -> dict:
    """modelo -> meta, só os que têm respostas para todas as questões pedidas."""
    out = {}
    for meta_arq in sorted(Path(pasta).glob("*.meta.json")):
        if meta_arq.name.endswith("_teste.meta.json"):     # teste rápido (--limite) não entra na avaliação
            continue
        meta = read_json(meta_arq)
        arq = meta_arq.with_name(meta["modelo"] + ".jsonl")
        if arq.exists() and meta.get("respondidas") == meta.get("questoes") and len(C.linhas(arq)) == meta["questoes"]:
            out[meta["modelo"]] = meta
    return out


def executar(saida: Path = SAIDA, respostas: Path = RESPOSTAS, final: Path = FINAL_V2, banco: Path = BANCO,
             workers: int = 8, judge_workers: int = 2, clientes: dict | None = None, progress=print) -> int:
    metas = disponiveis(respostas)
    if not metas:
        raise ValueError(f"Nenhuma resposta completa em {C.relativo(Path(respostas))}; rode antes, na DL-28: "
                         "bash pipeline/qa_research/rodar_llama_dl28.sh")
    uids = {q["uid"] for q in C.linhas(Path(banco) / "banco.jsonl")}
    dataset = [q for q in C.linhas(Path(final) / "dataset.jsonl") if q["uid"] in uids]
    saida = Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    C.gravar_jsonl(saida / "dataset.jsonl", dataset)
    # o nome do "deployment" registra o checkpoint usado; o cliente pronto substitui a chamada ao Azure
    modelos = {m: f"vllm/{meta['hf']}" for m, meta in metas.items()}
    cl = dict(clientes or {})
    for m, meta in metas.items():
        cl.setdefault("resp_" + m, RespostasProntas(Path(respostas) / f"{m}.jsonl", meta.get("sonda")))
    progress(f"[externos] {len(dataset)} questões x 2 condições | modelos: " +
             ", ".join(f"{m} ({meta['hf']})" for m, meta in metas.items()), flush=True)
    d = DatasetCompleto(saida, modelos=modelos, fontes_=[], progress=progress)
    st = d.avaliar(workers=workers, judge_workers=judge_workers, clientes=cl)
    if st == 0:
        d.relatorio()
        progress(f"[externos] {C.relativo(saida / 'QUALIDADE.md')}", flush=True)
    return st

