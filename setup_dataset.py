#!/usr/bin/env python3
"""
setup_dataset.py — baixa o corpus Petrolês e deixa `dataset/` pronto para uso.

    python setup_dataset.py                  # baixa o corpus híbrido (default)
    python setup_dataset.py --variante completo
    python setup_dataset.py --listar         # só mostra o que já existe
    python setup_dataset.py --force          # rebaixa mesmo se já estiver lá

O que ele faz, nesta ordem: cria `dataset/`, baixa o .zip da PUC-Rio (com
retomada, se a conexão cair no meio), confere o arquivo, extrai os `.txt`
DIRETO na pasta de destino e apaga o .zip.

QUAL VARIANTE
-------------
O pipeline da fase 3 (`pipeline/fase_3/`) aponta, por padrão, para

    dataset/corpus-SemProcessamento-publico-PetrolesHibrido/

que é a variante **híbrida**: os dois arquivos de óleo e gás mais o NILC
(português geral). A variante **completa** traz só os dois de óleo e gás — é
1/5 do tamanho e faz a varredura do corpus rodar em ~1 min em vez de ~8, ao
custo de não ter o texto geral.

As duas funcionam com o pipeline; se escolher `completo`, aponte o
`cfg.corpus_dir` do notebook para a pasta correspondente. Se quiser o híbrido
mas sem pagar a varredura do NILC, baixe o híbrido e use
`cfg.corpus_ignorar = ["NILC.txt"]` — assim o arquivo fica no disco e você pode
ligá-lo depois sem rebaixar nada.

SEM DEPENDÊNCIAS
----------------
Só a biblioteca padrão, de propósito: um script de setup que exige
`pip install` antes de rodar não é um script de setup. Proxy corporativo é
respeitado via as variáveis de ambiente HTTP_PROXY / HTTPS_PROXY. Se o seu
gateway usa uma CA própria, aponte `--ca-bundle caminho/para/ca.pem`.
"""

from __future__ import annotations

import argparse
import os
import shutil
import ssl
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

BASE_URL = "https://www.petroles.ica.ele.puc-rio.br/files/Corpora"

VARIANTES = {
    "hibrido": {
        "zip": "corpus-SemProcessamento-publico-PetrolesHibrido.zip",
        "descricao": "óleo e gás + NILC (português geral) — ~4,7 GB extraídos",
        "esperados": 3,
    },
    "completo": {
        "zip": "corpus-SemProcessamento-publico-PetrolesCompleto.zip",
        "descricao": "só óleo e gás (ANP, teses, boletins) — ~1,0 GB extraído",
        "esperados": 2,
    },
}

MARGEM_DISCO = 1.6   # o extraído costuma passar de 3x o .zip; sobra de segurança


# ---------------------------------------------------------------- utilidades --

def humano(n: float) -> str:
    for unidade in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024:
            return f"{n:,.1f} {unidade}"
        n /= 1024
    return f"{n:,.1f} PB"


def barra(feito: int, total: int, t0: float, largura: int = 32) -> str:
    decorrido = max(time.time() - t0, 1e-9)
    taxa = feito / decorrido
    if total > 0:
        frac = min(feito / total, 1.0)
        cheio = int(frac * largura)
        restante = (total - feito) / taxa if taxa > 0 else 0
        return (f"\r  [{'█' * cheio}{'·' * (largura - cheio)}] {frac:6.1%}  "
                f"{humano(feito)} / {humano(total)}  {humano(taxa)}/s  "
                f"faltam {restante / 60:4.1f} min ")
    return f"\r  {humano(feito)}  {humano(taxa)}/s "


def contexto_ssl(ca_bundle: str | None) -> ssl.SSLContext | None:
    if not ca_bundle:
        return None
    caminho = Path(ca_bundle)
    if not caminho.is_file():
        sys.exit(f"ERRO: --ca-bundle não encontrado: {caminho}")
    ctx = ssl.create_default_context(cafile=str(caminho))
    return ctx


# ------------------------------------------------------------------ download --

def baixar(url: str, destino: Path, ctx: ssl.SSLContext | None) -> Path:
    """Baixa com retomada. O parcial fica em `<destino>.part` até completar."""
    parcial = destino.with_suffix(destino.suffix + ".part")
    ja_tem = parcial.stat().st_size if parcial.exists() else 0

    req = urllib.request.Request(url, headers={"User-Agent": "setup_dataset/1.0"})
    if ja_tem:
        req.add_header("Range", f"bytes={ja_tem}-")
        print(f"  retomando de {humano(ja_tem)}")

    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=60)
    except urllib.error.HTTPError as e:
        if e.code == 416 and ja_tem:      # já baixado por inteiro
            parcial.replace(destino)
            return destino
        raise

    with resp:
        retomou = resp.status == 206
        if ja_tem and not retomou:
            print("  servidor não aceitou retomada — recomeçando do zero")
            ja_tem = 0
        tamanho_resposta = int(resp.headers.get("Content-Length") or 0)
        total = tamanho_resposta + (ja_tem if retomou else 0)

        livre = shutil.disk_usage(destino.parent).free
        preciso = (total or 0) * MARGEM_DISCO
        if total and livre < preciso:
            sys.exit(f"ERRO: espaço insuficiente em {destino.parent}\n"
                     f"       livre: {humano(livre)} · necessário (com margem "
                     f"para extrair): {humano(preciso)}")

        modo = "ab" if (ja_tem and retomou) else "wb"
        feito = ja_tem if retomou else 0
        t0, ultimo = time.time(), 0.0
        with open(parcial, modo) as fh:
            while True:
                bloco = resp.read(1024 * 512)
                if not bloco:
                    break
                fh.write(bloco)
                feito += len(bloco)
                if time.time() - ultimo > 0.5:
                    sys.stdout.write(barra(feito, total, t0))
                    sys.stdout.flush()
                    ultimo = time.time()
    sys.stdout.write(barra(feito, total or feito, t0) + "\n")

    if total and feito != total:
        sys.exit(f"ERRO: download incompleto ({humano(feito)} de {humano(total)}).\n"
                 f"       O parcial foi mantido em {parcial.name} — rode de novo "
                 f"para retomar.")
    parcial.replace(destino)
    return destino


# ------------------------------------------------------------------ extração --

def extrair(caminho_zip: Path, destino: Path) -> list[Path]:
    """Extrai os .txt DIRETO em `destino`, sem recriar a hierarquia do .zip.

    O achatamento é proposital: `cfg.corpus_dir` do pipeline varre `*.txt` no
    primeiro nível da pasta, então um .zip que embrulhe tudo numa subpasta
    deixaria o corpus invisível para a varredura.
    """
    destino.mkdir(parents=True, exist_ok=True)
    escritos: list[Path] = []
    with zipfile.ZipFile(caminho_zip) as z:
        membros = [i for i in z.infolist()
                   if not i.is_dir() and i.filename.lower().endswith(".txt")]
        if not membros:
            sys.exit(f"ERRO: nenhum .txt dentro de {caminho_zip.name} — "
                     f"conteúdo: {[i.filename for i in z.infolist()][:10]}")
        total = sum(i.file_size for i in membros)
        print(f"  {len(membros)} arquivo(s), {humano(total)} extraídos")
        feito, t0, ultimo = 0, time.time(), 0.0
        for info in membros:
            # só o nome-base: achata a hierarquia e, de quebra, torna
            # impossível um caminho do .zip escapar da pasta de destino
            alvo = destino / Path(info.filename.replace("\\", "/")).name
            with z.open(info) as origem, open(alvo, "wb") as saida:
                while True:
                    bloco = origem.read(1024 * 1024)
                    if not bloco:
                        break
                    saida.write(bloco)
                    feito += len(bloco)
                    if time.time() - ultimo > 0.5:
                        sys.stdout.write(barra(feito, total, t0))
                        sys.stdout.flush()
                        ultimo = time.time()
            escritos.append(alvo)
        sys.stdout.write(barra(feito, total, t0) + "\n")
    return escritos


def conferir(caminho_zip: Path) -> None:
    """Lê o índice central do .zip. Pega truncamento e HTML de erro salvo
    como .zip, que é o modo de falha mais comum atrás de proxy.

    Um arquivo inválido é apagado aqui mesmo: mantê-lo faria a próxima execução
    dizer ".zip já baixado" e falhar exatamente no mesmo ponto, para sempre.
    """
    try:
        with zipfile.ZipFile(caminho_zip) as z:
            if z.testzip() is not None:
                raise zipfile.BadZipFile("CRC inválido em um dos membros")
        return
    except zipfile.BadZipFile as e:
        with open(caminho_zip, "rb") as fh:     # fechar antes do unlink (Windows)
            cabecalho = fh.read(200)
        dica = ""
        if cabecalho[:1] in (b"<", b"{"):
            dica = ("\n       O conteúdo baixado é HTML/JSON, não um .zip — "
                    "provavelmente página de erro ou de login do proxy.")
        caminho_zip.unlink(missing_ok=True)
        sys.exit(f"ERRO: {caminho_zip.name} não é um .zip válido ({e}).{dica}\n"
                 f"       O arquivo foi apagado; corrija o acesso à rede e rode "
                 f"de novo.")


# --------------------------------------------------------------------- main --

def descrever_pasta(pasta: Path) -> list[Path]:
    if not pasta.is_dir():
        return []
    return sorted(pasta.glob("*.txt"))


def main() -> int:
    p = argparse.ArgumentParser(
        description="Baixa o corpus Petrolês e prepara a pasta dataset/.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="\n".join(f"  {k:<10} {v['descricao']}" for k, v in VARIANTES.items()))
    p.add_argument("--variante", choices=sorted(VARIANTES), default="hibrido",
                   help="qual corpus baixar (default: hibrido, o que o pipeline usa)")
    p.add_argument("--dataset-dir", default=None,
                   help="pasta dataset/ (default: ao lado deste script)")
    p.add_argument("--force", action="store_true",
                   help="rebaixa e reextrai mesmo se o corpus já estiver no disco")
    p.add_argument("--manter-zip", action="store_true",
                   help="não apaga o .zip depois de extrair")
    p.add_argument("--ca-bundle", default=os.environ.get("AOAI_CA_BUNDLE"),
                   help="certificado da CA, se o seu gateway usa uma própria "
                        "(default: $AOAI_CA_BUNDLE)")
    p.add_argument("--listar", action="store_true",
                   help="só mostra o que já existe em dataset/ e sai")
    args = p.parse_args()

    raiz = Path(args.dataset_dir) if args.dataset_dir else Path(__file__).resolve().parent / "dataset"
    var = VARIANTES[args.variante]
    destino = raiz / var["zip"].removesuffix(".zip")

    if args.listar:
        print(f"dataset: {raiz}")
        if not raiz.is_dir():
            print("  (não existe ainda)")
            return 0
        for sub in sorted(x for x in raiz.iterdir() if x.is_dir()):
            txts = descrever_pasta(sub)
            tam = sum(t.stat().st_size for t in txts)
            print(f"  {sub.name}/  {len(txts)} .txt · {humano(tam)}")
            for t in txts:
                print(f"      {t.name:<52} {humano(t.stat().st_size):>10}")
        return 0

    print(f"corpus Petrolês — variante '{args.variante}'")
    print(f"  {var['descricao']}")
    print(f"  destino: {destino}\n")

    existentes = descrever_pasta(destino)
    if existentes and not args.force:
        tam = sum(t.stat().st_size for t in existentes)
        print(f"Já existe: {len(existentes)} .txt, {humano(tam)}")
        for t in existentes:
            print(f"  {t.name:<52} {humano(t.stat().st_size):>10}")
        if len(existentes) < var["esperados"]:
            print(f"\nATENÇÃO: esperava {var['esperados']} arquivos e encontrei "
                  f"{len(existentes)}. Rode com --force para rebaixar.")
            return 1
        print("\nNada a fazer. Use --force para rebaixar.")
        return 0

    raiz.mkdir(parents=True, exist_ok=True)
    caminho_zip = raiz / var["zip"]
    url = f"{BASE_URL}/{var['zip']}"
    ctx = contexto_ssl(args.ca_bundle)
    if args.ca_bundle:
        print(f"  usando CA própria: {args.ca_bundle}")

    if caminho_zip.exists() and not args.force:
        print(f"[1/3] .zip já baixado ({humano(caminho_zip.stat().st_size)})")
    else:
        print(f"[1/3] baixando {url}")
        try:
            baixar(url, caminho_zip, ctx)
        except urllib.error.URLError as e:
            sys.exit(f"\nERRO ao baixar: {e}\n"
                     f"       Atrás de proxy? defina HTTPS_PROXY. "
                     f"CA própria? use --ca-bundle.\n"
                     f"       Em último caso, baixe {url} pelo navegador, ponha o "
                     f".zip em {raiz} e rode este script de novo.")

    print("[2/3] conferindo o .zip")
    conferir(caminho_zip)

    print(f"[3/3] extraindo em {destino.name}/")
    escritos = extrair(caminho_zip, destino)

    if args.manter_zip:
        print(f"\n.zip mantido em {caminho_zip}")
    else:
        caminho_zip.unlink()
        print(f"\n.zip apagado ({var['zip']})")

    print(f"\npronto — {len(escritos)} arquivo(s) em {destino}:")
    for t in sorted(escritos):
        print(f"  {t.name:<52} {humano(t.stat().st_size):>10}")
    if len(escritos) != var["esperados"]:
        print(f"\nATENÇÃO: esperava {var['esperados']} arquivos, extraí "
              f"{len(escritos)}. Confira antes de rodar o pipeline.")
        return 1

    print(f"\nNo notebook da fase 3, o config deve apontar para:\n"
          f"    corpus_dir=RAIZ / \"dataset\" / \"{destino.name}\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
