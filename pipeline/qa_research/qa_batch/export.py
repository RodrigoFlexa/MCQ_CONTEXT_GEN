"""QA limpo e snapshot auxiliar verificável para retorno via Git."""
import csv
import shutil
import tempfile
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from ..document.common import file_hash
from . import contracts as C
from .inputs import digest


def publish(output, batch):
    C.questions(batch)
    if batch["status"] != "ok":
        raise ValueError("Não é possível publicar lote incompleto")
    atomic_json(output / "qa.json", batch)
    with (output / "qa.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=("id", "dificuldade", "pergunta", "resposta"))
        writer.writeheader()
        writer.writerows(batch["questoes"])
    labels = {"facil": "Fácil", "media": "Média", "dificil": "Difícil"}
    lines = ["# Perguntas e respostas", ""]
    for q in batch["questoes"]:
        lines.extend([f"## {q['id']}. {labels[q['dificuldade']]}", "",
                      q["pergunta"], "", "**Resposta:** " + q["resposta"], ""])
    (output / "qa.md").write_text("\n".join(lines), encoding="utf-8")


def collect(output, destination):
    output, destination = Path(output).resolve(), Path(destination).resolve()
    if destination.exists() or output == destination or output in destination.parents or destination in output.parents:
        raise ValueError("Use um destino novo e separado da execução")
    with output_lock(output):
        summary = read_json(output / "resumo.json")
        identity = read_json(output / "identidade.json")
        if not summary or not identity:
            raise ValueError("Execução ainda não tem identidade e resumo")
        if summary["status"] == "em_execucao":
            raise ValueError("Aguarde o fim da execução")
        destination.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".qa-results-", dir=destination.parent))
        try:
            names = ("qa.json", "qa.csv", "qa.md", "entrada.json", "planejamento.json", "geracao.json",
                     "candidatas.json", "resumo.json", "identidade.json", "orcamento.json", "backend.json", "chamadas_llm.jsonl")
            for name in names:
                src = output / name
                if src.is_symlink():
                    raise ValueError("Link inesperado nos resultados: " + name)
                if src.is_file():
                    if name.startswith("qa.") and summary["status"] != "aprovado_modelo":
                        continue
                    shutil.copy2(src, staging / name)
            # Lista explícita: não copiar .env, SQLite, caches nem corpus original.
            for folder in ("chamadas", "revisoes", "refinamentos", "referencias", "migracoes"):
                directory = output / folder
                if directory.is_symlink():
                    raise ValueError("Diretório de resultados não pode ser link")
                for src in directory.glob("*.json"):
                    if src.is_symlink():
                        raise ValueError("Link inesperado nos resultados")
                    if folder == "chamadas":
                        checkpoint = read_json(src)
                        if digest(checkpoint["response"]) != checkpoint["response_sha256"]:
                            raise ValueError("Checkpoint alterado: " + src.name)
                    (staging / folder).mkdir(exist_ok=True)
                    shutil.copy2(src, staging / folder / src.name)
            if summary["status"] == "aprovado_modelo":
                batch = read_json(staging / "qa.json")
                C.questions(batch)
                if (batch["status"] != "ok" or summary["questoes_publicadas"] != 9
                        or digest(batch) != summary.get("qa_sha256")):
                    raise ValueError("Publicação QA inconsistente")
            files = {p.relative_to(staging).as_posix(): file_hash(p) for p in staging.rglob("*") if p.is_file()}
            atomic_json(staging / "manifest_resultados.json", {"schema": "qa-batch-results-v1", "files": files})
            from ..portable import _publish
            _publish(staging, destination)
        finally:
            # Apenas o staging criado por esta função, sob o pai explicitamente escolhido.
            if staging.exists() and staging.resolve().parent == destination.parent and staging.name.startswith(".qa-results-"):
                shutil.rmtree(staging)
    return destination
