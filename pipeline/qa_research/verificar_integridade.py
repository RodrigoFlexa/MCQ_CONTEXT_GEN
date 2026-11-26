"""Verifica a integridade dos arquivos de uma ou mais pastas de resultados.

Motivo: o modo sparse do disco virtual do WSL (wsl --manage <distro> --set-sparse true), ativado para liberar espaço no
C:, foi desativado pela Microsoft em versões mais novas do WSL por risco de corrupção de dados. No servidor apareceu um
trecho de 256 KB de bytes aleatórios, alinhado a 4 KB, no meio de um arquivo que o pipeline tinha lido inteiro pouco
antes (petroquest_banco_v3/dataset.jsonl).

O que é verificado:
  .json            precisa ser UTF-8 e JSON válido;
  .jsonl           cada linha não vazia precisa ser UTF-8 e JSON válido;
  .csv .md .txt    precisa ser UTF-8;
  .sqlite3 .db     PRAGMA integrity_check (caches de chamadas ao modelo).

Com --mover, os arquivos corrompidos vão para <pasta>/_corrompidos/<caminho relativo> e o pipeline os refaz na próxima
execução (um arquivo por unidade, como geracao/, auditoria/, sustentacao/, dedup_validas/ e unicidade/, custa uma
chamada; os arquivos agregados são regravados sem custo; um cache perdido só custa as chamadas que ele evitaria).
Arquivo versionado cuja versão do último commit está íntegra (por exemplo um contexto) não é movido: restaure-o com
`git checkout -- <arquivo>`. Se a versão do git também está corrompida, ele é movido como os demais.

    python -m pipeline.qa_research.verificar_integridade pipeline/qa_research/relatorios/geracao_final_v3 \\
        pipeline/qa_research/relatorios/petroquest_banco_v3 pipeline/qa_research/relatorios/contextos_finais_v1 [--mover]
"""
import argparse
import json
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

TEXTO = {".csv", ".md", ".txt"}
SQLITE = {".sqlite3", ".db", ".sqlite"}


def verificar(arq: Path, dados: bytes | None = None) -> str | None:
    """Descrição do defeito, ou None se o arquivo (ou os bytes dados, de mesmo tipo) está íntegro."""
    suf = arq.suffix.lower()
    try:
        if suf in SQLITE:
            con = sqlite3.connect(f"file:{arq}?mode=ro", uri=True)
            try:
                r = con.execute("PRAGMA integrity_check").fetchall()
            finally:
                con.close()
            return None if r == [("ok",)] else f"sqlite: {r[:3]}"
        dados = arq.read_bytes() if dados is None else dados
        if suf in (".json", ".jsonl") or suf in TEXTO:
            try:
                texto = dados.decode("utf-8-sig" if suf == ".csv" else "utf-8")
            except UnicodeDecodeError as exc:
                return f"bytes inválidos a partir de {exc.start}"
            if suf != ".csv" and "\x00" * 16 in texto:     # bloco zerado (bytes nulos soltos no CSV vêm das respostas)
                return f"bloco de bytes nulos em {texto.index(chr(0) * 16)}"
            if suf == ".json":
                json.loads(texto)
            elif suf == ".jsonl":
                for i, linha in enumerate(texto.splitlines(), 1):
                    if linha.strip():
                        try:
                            json.loads(linha)
                        except json.JSONDecodeError as exc:
                            return f"linha {i}: {exc.msg}"
        return None
    except Exception as exc:  # noqa: BLE001
        return f"{type(exc).__name__}: {exc}"[:200]


def copia_boa_no_git(arq: Path) -> bool:
    """O arquivo é versionado e a versão do último commit está íntegra (então restaurar do git resolve)."""
    r = subprocess.run(["git", "show", f"HEAD:./{arq}"], capture_output=True, cwd=None)
    if r.returncode != 0:
        r = subprocess.run(["git", "show", f"HEAD:{arq.resolve().relative_to(raiz_git())}"], capture_output=True)
    return r.returncode == 0 and verificar(arq, r.stdout) is None


def raiz_git() -> Path:
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return Path(r.stdout.strip()) if r.returncode == 0 else Path("/")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pastas", nargs="+", type=Path)
    ap.add_argument("--mover", action="store_true", help="move os corrompidos não versionados para _corrompidos/")
    a = ap.parse_args(argv)
    total, ruins = 0, []
    alvo = {".json", ".jsonl"} | TEXTO | SQLITE
    for pasta in a.pastas:
        for arq in sorted(pasta.rglob("*")):
            if not arq.is_file() or "_corrompidos" in arq.parts or arq.suffix.lower() not in alvo:
                continue
            total += 1
            if total % 20000 == 0:
                print(f"  {total} arquivos verificados...", flush=True)
            d = verificar(arq)
            if d:
                ruins.append((pasta, arq, d))
                print(f"CORROMPIDO {arq}: {d}", flush=True)
    print(f"\n{total} arquivos verificados; {len(ruins)} corrompidos.")
    if ruins and a.mover:
        for pasta, arq, _ in ruins:
            if arq.suffix.lower() not in SQLITE and copia_boa_no_git(arq):
                print(f"  a versão do git está íntegra; restaure com: git checkout -- {arq}")
                continue
            dest = pasta / "_corrompidos" / arq.relative_to(pasta)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(arq), dest)
            print(f"  movido: {arq} -> {dest}")
    elif ruins:
        print("Rode de novo com --mover para tirar os corrompidos do caminho; o pipeline os refaz.")
    return 1 if ruins and not a.mover else 0


if __name__ == "__main__":
    sys.exit(main())
