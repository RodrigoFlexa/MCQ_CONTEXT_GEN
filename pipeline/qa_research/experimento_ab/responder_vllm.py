"""Respostas de modelos abertos (Llama) às questões do banco final, com vLLM local (sem API e sem o juiz).

Roda na máquina com GPU (DL-28). Usa exatamente o protocolo dos modelos já avaliados: o mesmo prompt de sistema
(respondente_curta, resposta de até 20 palavras) e a mesma mensagem do usuário, o JSON {"pergunta", "contexto"} com o
contexto nulo (sem documento) ou com os blocos de origem (com documento), tirados de petroquest_final_v2/questoes.jsonl.
Só as questões do banco final v1 (petroquest_banco_v1/banco.jsonl) são respondidas, nas duas condições.
Temperatura 0 e saída em JSON guiado quando a versão do vLLM permite.

Saída: pipeline/qa_research/relatorios/respostas_externas/<nome>.jsonl (uma linha por uid) e <nome>.meta.json.
Retomável: uids já respondidos não são repetidos. O juiz roda depois no servidor (comando avaliar-externos).
Arquivo independente do resto do pipeline: só precisa do vLLM instalado.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from pathlib import Path

QA = Path(__file__).resolve().parents[1]
QUESTOES = QA / "relatorios" / "petroquest_final_v2" / "questoes.jsonl"
BANCO = QA / "relatorios" / "petroquest_banco_v1" / "banco.jsonl"
PROMPT = Path(__file__).resolve().parent / "prompts" / "respondente_curta.md"
SAIDA = QA / "relatorios" / "respostas_externas"
LIMITE = 20
SONDA = {"pergunta": "Qual a função de um separador trifásico?", "contexto": None}   # a mesma do servidor
MODELOS = {
    "llama-3-1-8b": {"hf": "meta-llama/Llama-3.1-8B-Instruct"},
    # 70B: bf16 precisa de ~140 GB só de pesos (2 GPUs de 80 GB); com GPUs menores, a versão FP8 (~70 GB)
    "llama-3-3-70b": {"hf": "meta-llama/Llama-3.3-70B-Instruct", "hf_fp8": "RedHatAI/Llama-3.3-70B-Instruct-FP8-dynamic"},
}
ESQUEMA = {"type": "object", "properties": {"resposta": {"type": "string"}}, "required": ["resposta"],
           "additionalProperties": False}


def sistema(limite: int = LIMITE) -> str:
    return PROMPT.read_text(encoding="utf-8").strip().format(limite=limite)


def usuario(q: dict | None) -> str:
    """Mesma serialização do servidor (limite.AvaliacaoCurta.responder_um)."""
    if q is None:
        return json.dumps(SONDA, ensure_ascii=False)
    return json.dumps({"pergunta": q["pergunta"], "contexto": q.get("contexto_tecnico")}, ensure_ascii=False)


def sha(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def linhas(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def questoes(banco: Path = BANCO, todas: Path = QUESTOES) -> list[dict]:
    """As duas condições (closed_book e open_book) das questões do banco final."""
    uids = {q["uid"] for q in linhas(banco)}
    out = [q for q in linhas(todas) if q["uid"].split(":", 1)[1] in uids]
    faltam = len(uids) * 2 - len(out)
    if faltam:
        raise SystemExit(f"{faltam} questões do banco não estão em {todas}; atualize o repositório (git pull)")
    return out


def extrair(texto: str) -> tuple[str, str]:
    """(resposta, como foi obtida): JSON válido, campo extraído do texto ou o texto inteiro."""
    t = texto.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    try:
        d = json.loads(t)
        if isinstance(d, dict) and isinstance(d.get("resposta"), str):
            return d["resposta"].strip(), "json"
    except json.JSONDecodeError:
        pass
    m = re.search(r'"resposta"\s*:\s*"((?:[^"\\]|\\.)*)"', t)
    if m:
        return json.loads(f'"{m.group(1)}"').strip(), "extraida"
    return t, "texto"


def parametros(max_tokens: int):
    from vllm import SamplingParams
    base = dict(temperature=0.0, max_tokens=max_tokens)
    try:                                              # vLLM >= 0.10
        from vllm.sampling_params import StructuredOutputsParams
        return SamplingParams(**base, structured_outputs=StructuredOutputsParams(json=ESQUEMA)), "structured_outputs"
    except (ImportError, TypeError):
        pass
    try:                                              # vLLM 0.6 a 0.9
        from vllm.sampling_params import GuidedDecodingParams
        return SamplingParams(**base, guided_decoding=GuidedDecodingParams(json=ESQUEMA)), "guided_decoding"
    except (ImportError, TypeError):
        return SamplingParams(**base), "nenhum"


def escolher_hf(nome: str, forcar: str | None) -> str:
    if forcar:
        return forcar
    cfg = MODELOS[nome]
    if "hf_fp8" not in cfg:
        return cfg["hf"]
    import torch
    n = torch.cuda.device_count()
    mem = min(torch.cuda.get_device_properties(i).total_memory for i in range(n)) / 2 ** 30
    # pesos bf16 de 70B (~132 GiB) + cache: só com pelo menos 2 x 80 GB
    return cfg["hf"] if n * mem >= 150 else cfg["hf_fp8"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modelo", choices=sorted(MODELOS))
    ap.add_argument("--hf", help="checkpoint do Hugging Face (substitui a escolha automática)")
    ap.add_argument("--tp", type=int, default=0, help="tensor parallel (padrão: todas as GPUs visíveis)")
    ap.add_argument("--memoria", type=float, default=0.92, help="fração da memória de cada GPU para o vLLM")
    ap.add_argument("--max-model-len", type=int, default=4096, help="a maior mensagem tem ~2,5 mil tokens")
    ap.add_argument("--max-tokens", type=int, default=200)
    ap.add_argument("--lote", type=int, default=1024, help="questões por chamada ao vLLM (grava a cada lote)")
    ap.add_argument("--limite", type=int, default=0, help="só as N primeiras (teste rápido)")
    a = ap.parse_args(argv)

    import torch
    from vllm import LLM, __version__ as versao_vllm

    qs = questoes()
    if a.limite:
        qs = qs[: a.limite]
    SAIDA.mkdir(parents=True, exist_ok=True)
    arq, meta_arq = SAIDA / f"{a.modelo}.jsonl", SAIDA / f"{a.modelo}.meta.json"
    feitos = {r["uid"] for r in linhas(arq)} if arq.exists() else set()
    pendentes = [q for q in qs if q["uid"] not in feitos]
    hf = escolher_hf(a.modelo, a.hf)
    tp = a.tp or torch.cuda.device_count()
    sp, guiado = parametros(a.max_tokens)
    meta = {"modelo": a.modelo, "hf": hf, "vllm": versao_vllm, "tensor_parallel": tp, "gpus": [
        torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())], "temperatura": 0.0,
        "max_tokens": a.max_tokens, "saida_guiada": guiado, "limite_palavras": LIMITE,
        "prompt_sha256": sha(sistema()), "questoes": len(qs)}
    if meta_arq.exists():
        antigo = json.loads(meta_arq.read_text(encoding="utf-8"))
        mudou = [k for k in ("hf", "prompt_sha256", "max_tokens", "limite_palavras") if antigo.get(k) != meta[k]]
        if mudou and feitos:
            raise SystemExit(f"{arq} foi gerado com outro {', '.join(mudou)}; apague-o para refazer")
    print(f"[vllm] {a.modelo} = {hf} | TP {tp} | {meta['gpus']} | saída guiada: {guiado} | "
          f"{len(pendentes)} de {len(qs)} questões a responder", flush=True)
    if not pendentes and feitos:
        meta_arq.write_text(json.dumps({**meta, "respondidas": len(feitos)}, ensure_ascii=False, indent=1), encoding="utf-8")
        return 0
    llm = LLM(model=hf, tensor_parallel_size=tp, gpu_memory_utilization=a.memoria, max_model_len=a.max_model_len,
              dtype="auto", seed=0)
    s = sistema()
    conv = lambda u: [{"role": "system", "content": s}, {"role": "user", "content": u}]   # noqa: E731
    sonda = llm.chat([conv(usuario(None))], sp, use_tqdm=False)[0].outputs[0].text
    meta["sonda"] = {"usuario": usuario(None), "resposta": extrair(sonda)[0]}
    print(f"[vllm] sonda: {meta['sonda']['resposta']}", flush=True)
    inicio = time.time()
    with arq.open("a", encoding="utf-8") as f:
        for k in range(0, len(pendentes), a.lote):
            lote = pendentes[k:k + a.lote]
            outs = llm.chat([conv(usuario(q)) for q in lote], sp, use_tqdm=True)
            for q, o in zip(lote, outs):
                bruta = o.outputs[0].text
                resp, como = extrair(bruta)
                f.write(json.dumps({"uid": q["uid"], "modelo": a.modelo, "usuario_sha256": sha(usuario(q)),
                                    "resposta": resp, "como": como, "bruta": bruta,
                                    "palavras": len(resp.split())}, ensure_ascii=False) + "\n")
            f.flush()
            print(f"[vllm] {min(k + a.lote, len(pendentes))}/{len(pendentes)} ({time.time() - inicio:.0f} s)", flush=True)
    rs = linhas(arq)
    meta.update(respondidas=len(rs), como={c: sum(r["como"] == c for r in rs) for c in ("json", "extraida", "texto")},
                vazias=sum(not r["resposta"] for r in rs),
                acima_do_limite=sum(r["palavras"] > LIMITE for r in rs))
    meta_arq.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[vllm] {a.modelo}: {len(rs)} respostas em {arq}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
