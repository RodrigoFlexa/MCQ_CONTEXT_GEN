"""Lê o docx de frases do especialista e devolve a referência de cada subtópico.

O docx ("SUGESTÃO DE FRASES PARA COMPOR PROMPT MÚLTIPLA ESCOLHA V14") traz, por
subtópico, até três versões do mesmo texto: a descrição longa original, uma
"Versão resumida" e uma "Versão compacta". A fase 5 filtra as questões pela
semelhança com esse texto, então é preciso extraí-lo de forma reprodutível em
vez de copiar à mão.

Uso, a partir da raiz do repositório:

    python pipeline/fase_5/extrair_referencias.py
    python pipeline/fase_5/extrair_referencias.py --preferencia resumida

Saída: `pipeline/fase_5/referencias_especialista.json`, com as três variantes de
cada subtópico, a escolhida pela ordem de preferência e os avisos de
reconciliação com `pipeline/fase_3/topicos.py`.

Particularidades do docx que o parser trata explicitamente:
  * a hierarquia vem da numeração do Word (ilvl 0 = tópico, ilvl 1 = subtópico),
    não do estilo do parágrafo, que varia entre "List Paragraph", "Normal" e
    "Normal (Web)";
  * "Versão reumida" (sem o 's') aparece uma vez e é lida como resumida;
  * em "Sistema de Combate a Incêndio" o especialista rotulou as DUAS versões
    como "Versão resumida"; a segunda ocorrência é lida como compacta;
  * as compactas de "Operação de Separadores Trifásicos" e "Compressão de Gás"
    repetem o texto de outro subtópico (copiar/colar do especialista). O parser
    detecta variante repetida e cai para a próxima da ordem de preferência,
    registrando o aviso.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(RAIZ / "pipeline" / "fase_3"))

PREFERENCIA_PADRAO = ("compacta", "resumida", "longa")

RE_MINIMO = re.compile(r"\(\s*(\d+)\s+quest[õo]es?\s*\)", re.IGNORECASE)
RE_RESUMIDA = re.compile(r"^vers[ãa]o\s+re[us]?umida\s*:\s*", re.IGNORECASE)
RE_COMPACTA = re.compile(r"^vers[ãa]o\s+compacta\s*:\s*", re.IGNORECASE)
INICIO_DESCRICAO = "as questões devem abordar"


def normalizar(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto or "")
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", sem_acento).strip().lower()


def nivel_de_lista(paragrafo) -> int | None:
    """Nível da numeração do Word (0 = tópico, 1 = subtópico), ou None."""
    from docx.oxml.ns import qn
    pPr = paragrafo._p.find(qn("w:pPr"))
    if pPr is None:
        return None
    numPr = pPr.find(qn("w:numPr"))
    if numPr is None:
        return None
    ilvl = numPr.find(qn("w:ilvl"))
    return int(ilvl.get(qn("w:val"))) if ilvl is not None else 0


def ler_docx(caminho: Path) -> list[dict]:
    """Percorre o docx e devolve um registro por (tópico, subtópico)."""
    import docx

    documento = docx.Document(str(caminho))
    blocos: list[dict] = []
    topico = None
    minimo_topico = None
    atual: dict | None = None

    def novo_bloco(topico: str, subtopico: str | None, minimo: int | None) -> dict:
        bloco = {"topico_docx": topico, "subtopico_docx": subtopico,
                 "minimo_questoes": minimo,
                 "variantes": {"longa": None, "resumida": None, "compacta": None}}
        blocos.append(bloco)
        return bloco

    for paragrafo in documento.paragraphs:
        texto = paragrafo.text.strip()
        if not texto:
            continue
        nivel = nivel_de_lista(paragrafo)

        if nivel == 0:
            titulo = RE_MINIMO.sub("", texto).strip()
            minimo = RE_MINIMO.search(texto)
            topico = titulo
            minimo_topico = int(minimo.group(1)) if minimo else None
            atual = None
            continue

        if nivel == 1 and topico:
            # Cabeçalho de subtópico: os textos vêm nos parágrafos seguintes.
            # Alguns parágrafos de descrição também são "List Paragraph" mas sem
            # numeração, então quem manda é o nível, não o estilo.
            if normalizar(texto).startswith(normalizar(INICIO_DESCRICAO)):
                if atual is None:
                    atual = novo_bloco(topico, None, minimo_topico)
                if atual["variantes"]["longa"] is None:
                    atual["variantes"]["longa"] = texto
                continue
            atual = novo_bloco(topico, RE_MINIMO.sub("", texto).strip(),
                               minimo_topico)
            continue

        if topico is None:
            continue  # cabeçalho do documento, antes do primeiro tópico

        if RE_RESUMIDA.match(texto):
            if atual is None:
                atual = novo_bloco(topico, None, minimo_topico)
            corpo = RE_RESUMIDA.sub("", texto).strip()
            # o especialista rotulou duas versões como "resumida" em um dos
            # subtópicos; a segunda ocupa o lugar da compacta
            if atual["variantes"]["resumida"] is None:
                atual["variantes"]["resumida"] = corpo
            elif atual["variantes"]["compacta"] is None:
                atual["variantes"]["compacta"] = corpo
            continue

        if RE_COMPACTA.match(texto):
            if atual is None:
                atual = novo_bloco(topico, None, minimo_topico)
            atual["variantes"]["compacta"] = RE_COMPACTA.sub("", texto).strip()
            continue

        if normalizar(texto).startswith(normalizar(INICIO_DESCRICAO)):
            if atual is None:
                atual = novo_bloco(topico, None, minimo_topico)
            if atual["variantes"]["longa"] is None:
                atual["variantes"]["longa"] = texto
            continue

    return blocos


def reconciliar(blocos: list[dict]) -> tuple[list[dict], list[str]]:
    """Casa cada bloco do docx com o par (tópico, subtópico) de `topicos.py`."""
    from topicos import TOPICOS

    pares = [(t, s) for t, subs in TOPICOS.items() for s in subs]
    por_sub = {normalizar(s): (t, s) for t, s in pares}
    por_topico = {}
    for t, s in pares:
        por_topico.setdefault(normalizar(t), []).append((t, s))

    avisos: list[str] = []
    casados: list[dict] = []
    usados: set[tuple[str, str]] = set()

    for bloco in blocos:
        sub_docx = bloco["subtopico_docx"]
        par = None
        if sub_docx:
            par = por_sub.get(normalizar(sub_docx))
        if par is None:
            # tópico sem subtópicos no docx (KPI, Descomissionamento): casa com
            # o subtópico único do tópico em topicos.py
            candidatos = por_topico.get(normalizar(bloco["topico_docx"]), [])
            if len(candidatos) == 1:
                par = candidatos[0]
        if par is None:
            avisos.append(f"sem par em topicos.py: "
                          f"{bloco['topico_docx']} >> {sub_docx}")
            continue
        if par in usados:
            avisos.append(f"par repetido no docx, ignorando a 2ª ocorrência: {par[1]}")
            continue
        usados.add(par)
        casados.append({"topico": par[0], "subtopico": par[1],
                        "topico_docx": bloco["topico_docx"],
                        "subtopico_docx": sub_docx,
                        "minimo_questoes": bloco["minimo_questoes"],
                        "variantes": bloco["variantes"], "avisos": []})

    faltando = [f"{t} >> {s}" for t, s in pares if (t, s) not in usados]
    for item in faltando:
        avisos.append(f"sem referência no docx: {item}")
    return casados, avisos


def conteudo(texto: str | None) -> set[str]:
    """Palavras de conteúdo (>3 letras, sem acento) de um texto."""
    return {p for p in re.findall(r"[a-z0-9]+", normalizar(texto or ""))
            if len(p) > 3}


def escolher_variantes(refs: list[dict], preferencia: tuple[str, ...]) -> None:
    """Escolhe a variante de cada subtópico, descartando texto de OUTRO subtópico.

    A descrição longa de cada subtópico é a referência de assunto: resumida e
    compacta deveriam ser resumos dela. Quando uma variante se parece mais com a
    longa de outro subtópico do que com a própria, foi copiada do vizinho
    (aconteceu em "Operação de Separadores Trifásicos", que recebeu o texto de
    tratadores eletrostáticos, e em "Compressão de Gás", que recebeu o de
    tratamento do gás). Nesses casos a variante é descartada e a escolha cai
    para a próxima da ordem de preferência — na prática, a longa correta.
    """
    longas = {ref["subtopico"]: conteudo(ref["variantes"].get("longa"))
              for ref in refs}

    def dono_provavel(texto: str) -> tuple[str, float, float]:
        alvo = conteudo(texto)
        pontos = {sub: len(alvo & palavras) / max(len(alvo), 1)
                  for sub, palavras in longas.items() if palavras}
        if not pontos:
            return "", 0.0, 0.0
        dono = max(pontos, key=pontos.get)
        return dono, pontos[dono], 0.0

    for ref in refs:
        proprio = longas.get(ref["subtopico"], set())
        for variante in preferencia:
            texto = ref["variantes"].get(variante)
            if not texto:
                continue
            if variante != "longa" and proprio:
                alvo = conteudo(texto)
                dono, ponto_dono, _ = dono_provavel(texto)
                ponto_proprio = len(alvo & proprio) / max(len(alvo), 1)
                if dono and dono != ref["subtopico"]:
                    ref["avisos"].append(
                        f"variante '{variante}' descartada: casa melhor com a "
                        f"descrição de '{dono}' ({ponto_dono:.2f}) do que com a "
                        f"própria ({ponto_proprio:.2f}) — copiar/colar no docx")
                    continue
            ref["variante_escolhida"] = variante
            ref["texto"] = texto
            break
        else:
            ref["variante_escolhida"] = None
            ref["texto"] = None
            ref["avisos"].append("nenhuma variante utilizável")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--docx", type=Path,
                        default=RAIZ / "SUGESTÃO DE FRASES PARA COMPOR PROMPT "
                                       "MÚLTIPLA ESCOLHA V14 09 09 26.docx")
    parser.add_argument("--saida", type=Path,
                        default=AQUI / "referencias_especialista.json")
    parser.add_argument("--preferencia", default=",".join(PREFERENCIA_PADRAO),
                        help="Ordem de preferência das variantes, separada por "
                             f"vírgula (padrão: {','.join(PREFERENCIA_PADRAO)}).")
    args = parser.parse_args()

    preferencia = tuple(p.strip() for p in args.preferencia.split(",") if p.strip())
    blocos = ler_docx(args.docx)
    refs, avisos = reconciliar(blocos)
    escolher_variantes(refs, preferencia)

    saida = {
        "docx": args.docx.name,
        "gerado_em": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "preferencia": list(preferencia),
        "referencias": refs,
        "avisos": avisos,
    }
    args.saida.write_text(json.dumps(saida, ensure_ascii=False, indent=2),
                          encoding="utf-8")

    print(f"{len(blocos)} blocos no docx · {len(refs)} subtópicos casados")
    contagem = {}
    for ref in refs:
        contagem[ref["variante_escolhida"]] = contagem.get(ref["variante_escolhida"], 0) + 1
    print("variante escolhida:", ", ".join(f"{k}={v}" for k, v in contagem.items()))
    for ref in refs:
        for aviso in ref["avisos"]:
            print(f"  [{ref['subtopico'][:40]}] {aviso}")
    for aviso in avisos:
        print(f"  [reconciliação] {aviso}")
    print(f"-> {args.saida}")


if __name__ == "__main__":
    main()
