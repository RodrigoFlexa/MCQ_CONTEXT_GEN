"""
utils_fase3.py — motor do pipeline de geração de MCQ da fase 3.

O notebook `pipeline_mcq_fase3.ipynb` orquestra; este módulo carrega o que é
mecânico demais para ficar em célula: varredura do corpus, embeddings, scorer de
vícios, entropia, estado e repositório.

Mapa do módulo (na ordem do pipeline):

    Config                     parâmetros de tudo, em um lugar só
    §1 texto                   normalização, tokenização, n-gramas
    §2 facetas                 extração LLM da instrução longa do subtópico
    §3 corpus                  varredura lexical streaming -> candidatos
    §4 embeddings              sentence-transformers + cache em disco
    §5 recuperação             rerank semântico + MMR -> documentos de geração
    §6 LLM                     consolidação, geração, judge, refinamento
    §7 vícios                  scorer determinístico (sem LLM)
    §8 entropia                codebook fixo, entropia de Shannon, estagnação
    §9 repositório e estado    persistência e retomada
   §10 few-shot                pool amostrado, seed -> questões aprovadas

Convenção de questão (dict) em todo o pipeline:

    do gerador:  {"id", "stem", "alternatives": [...], "correct_answer_index",
                  "dificuldade_gerador": "facil|media|dificil" (opcional,
                  autoavaliação do gerador — não confundir com "difficulty",
                  que é do judge; ver prompts_fase3.py)}
    + do judge:  {"nota": float em [0,1], "difficulty": "facil|media|dificil"}
    + do scorer: {"vicios": {...}}
"""

from __future__ import annotations

import hashlib
import heapq
import json
import math
import random
import re
import time
import unicodedata
from collections import Counter, deque
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Sequence

import numpy as np

import prompts_fase3 as P
from exemplos_externos_fase3 import EXEMPLOS_ARC

# ===========================================================================
# Config
# ===========================================================================


@dataclass
class Config:
    """Todos os parâmetros do pipeline. Instancie uma vez no notebook."""

    # ------------------------------------------------------------ caminhos --
    raiz: Path = Path("../..")                    # raiz do repositório
    corpus_dir: Path | None = None                # pasta com os .txt do Petrolês
    corpus_txt: list[Path] = field(default_factory=list)  # ...ou .txt avulsos
    corpus_zip: Path | None = None                # ...ou um .zip com eles dentro
    corpus_ignorar: list[str] = field(default_factory=list)  # nomes a pular
    out_dir: Path = Path("saida_fase3")

    # ------------------------------------------------------------ modelos --
    modelo_forte: str = "gpt-5-petrobras"         # gerador, judge, refinador
    modelo_leve: str = "gpt-4o-mini-petrobras"    # extrator, consolidador
    modelo_embedding: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    judge_reasoning_effort: str = "low"           # "baixo esforço" (passo 4)
    gerador_reasoning_effort: str = "medium"

    # ------------------------------------------------------------ facetas --
    n_facetas_max: int = 6

    # ------------------------------------------------------------ corpus ---
    # A janela é medida em PALAVRAS, não em linhas. Os arquivos do corpus têm
    # densidades muito diferentes por linha (~25 palavras/linha nos dois de óleo
    # e gás, ~7 no NILC): uma janela de N linhas produziria trechos de tamanhos
    # incomparáveis entre arquivos. Acumular até um orçamento de palavras trata
    # os três como um corpus só.
    alvo_palavras_trecho: int = 250
    sobreposicao_trecho: float = 0.5   # fração da janela mantida na próxima
    max_linhas_trecho: int = 120       # trava para linhas muito curtas
    min_palavras: int = 80
    max_palavras: int = 450
    max_frac_number: float = 0.15    # fração máxima de tokens "<NUMBER>"
    top_k_lexical: int = 300         # candidatos guardados por faceta
    peso_termo_forte: float = 3.0
    peso_termo_apoio: float = 1.0
    cap_termos: int = 6              # teto de termos distintos contados

    # ------------------------------------------------- recuperação (est. 2) --
    n_trechos_por_documento: int = 6   # N do passo 1 (trechos -> 1 documento)
    n_documentos_por_faceta: int = 4   # quantos documentos de geração por faceta
    peso_lexical: float = 0.4
    peso_semantico: float = 0.6
    mmr_lambda: float = 0.7
    mmr_dup_threshold: float = 0.92

    # ------------------------------------------------------- consolidação --
    max_palavras_documento: int = 900

    # ------------------------------------------------------------ geração --
    n_questoes_por_lote: int = 6
    n_alternativas: int = 4
    n_exemplos_fewshot: int = 3
    # Pós-processamento: a posição do gabarito é sorteada aqui, não pedida ao
    # gerador. Desligue se o embaralhamento for feito fora do pipeline.
    embaralhar_alternativas: bool = True
    # 1 exemplo de outro domínio (hoje: ARC-Challenge, ver
    # exemplos_externos_fase3.py) sorteado a cada lote, além dos exemplos do
    # próprio domínio — calibra a LÓGICA de construção de distrator sem
    # herdar os vícios do banco seed/repositório. Desligue pra voltar ao
    # comportamento anterior sem tocar no resto do pipeline.
    usar_exemplos_externos: bool = True

    # ------------------------------------------------------------- vícios --
    tol_similaridade: float = 0.55   # limite do vício, em [0,1]
    tol_comprimento: float = 0.55
    tol_distratores: float = 0.50
    # Vício 4 (racionalização): distrator que se justifica minimizando o
    # próprio ponto fraco ("assumindo que...", "pressupondo que...", "...tende
    # a ser secundário"). Tolerância zero de propósito: no banco da fase 3,
    # esse padrão nunca apareceu na alternativa correta (0 de 102) — é um
    # sinal específico de distrator e barato de corrigir no refinador, então
    # não há motivo para tolerar nenhuma ocorrência.
    tol_racionalizacao: float = 0.0
    tau_similaridade: float = 0.15   # delta de cosseno que satura o vício em 1
    tau_comprimento: float = 0.40    # desvio relativo de tamanho que satura
    # "distrator lixo" tem dois testes, ambos calibráveis em `calibrar_tolerancias`:
    lim_distrator_irrelevante: float = 0.15   # piso absoluto de cosseno com o enunciado
    fator_distrator_irrelevante: float = 0.45  # ...ou muito abaixo da correta

    # ------------------------------------------------------------- filtros --
    nota_minima_aprovacao: float = 0.60   # abaixo disso não entra no repositório
    nota_minima_fewshot: float = 0.80     # entra no pool de exemplos (passo 8)

    # ------------------------------------------------------------ entropia --
    n_clusters_codebook: int = 24    # k da clusterização fixa, por subtópico
    limiar_ganho_entropia: float = 0.010  # A CALIBRAR no piloto (passo 9)
    rodadas_estagnadas_max: int = 5
    min_questoes_para_entropia: int = 12  # pool pequeno demais não informa nada
    max_rodadas_por_documento: int = 30   # trava de segurança

    # ------------------------------------------------------------- geral ---
    seed: int = 42

    def __post_init__(self):
        self.raiz = Path(self.raiz)
        self.out_dir = Path(self.out_dir)
        for sub in ("indices", "documentos", "estado", "repositorio", "logs",
                    "embeddings"):
            (self.out_dir / sub).mkdir(parents=True, exist_ok=True)

    def resumo(self) -> str:
        d = {k: (str(v) if isinstance(v, Path) else v)
             for k, v in asdict(self).items()}
        return json.dumps(d, ensure_ascii=False, indent=2, default=str)


# ===========================================================================
# §1 texto
# ===========================================================================

_TABELA_ACENTOS: dict[int, str] | None = None
_RE_TOKEN = re.compile(r"[a-z0-9&]+")


def normalizar(texto: str) -> str:
    """Minúsculas sem acento — a forma canônica dos termos do léxico."""
    global _TABELA_ACENTOS
    if _TABELA_ACENTOS is None:
        _TABELA_ACENTOS = {}
        for cp in range(0x2500):
            ch = chr(cp)
            dec = unicodedata.normalize("NFD", ch.lower())
            _TABELA_ACENTOS[cp] = "".join(
                c for c in dec if unicodedata.category(c) != "Mn")
    return texto.translate(_TABELA_ACENTOS)


def tokenizar(texto_normalizado: str) -> list[str]:
    return _RE_TOKEN.findall(texto_normalizado)


_STOPWORDS = frozenset("""
a o as os um uma uns umas de do da dos das em no na nos nas por para com sem
sob sobre entre ao aos e ou que se ja nao mais menos muito pouco tambem como
quando onde qual quais seu sua seus suas este esta esse essa aquele aquela
isso isto aquilo ser estar ter haver deve devem pode podem foi sao eh
""".split())


def palavras_conteudo(texto: str) -> set[str]:
    return {t for t in tokenizar(normalizar(texto))
            if len(t) > 2 and t not in _STOPWORDS}


def hash_curto(*partes: Any, n: int = 10) -> str:
    h = hashlib.sha1("|".join(str(p) for p in partes).encode("utf-8"))
    return h.hexdigest()[:n]


# ===========================================================================
# §2 facetas — a instrução longa vira alvos operacionais
# ===========================================================================
# As instruções de `topicos.py` vão de 350 a 6.400 caracteres e enumeram muitos
# assuntos numa frase só. Um embedding do parágrafo inteiro é a média de dez
# assuntos — recupera o genérico e nada do específico. A faceta é o recorte que
# resolve isso: vira query de busca (semântica + lexical) e vira o alvo
# declarado da rodada de geração.


@dataclass
class Faceta:
    id: str
    topico: str
    subtopico: str
    titulo: str
    foco: str
    query: str
    termos_fortes: list[str]
    termos_apoio: list[str]

    @property
    def texto_query(self) -> str:
        return f"{self.titulo}. {self.query}"


def _limpar_termos(termos: Iterable[str]) -> list[str]:
    vistos, saida = set(), []
    for t in termos or []:
        t = normalizar(str(t)).strip()
        t = re.sub(r"\s+", " ", t)
        if len(t) < 3 or t in vistos:
            continue
        vistos.add(t)
        saida.append(t)
    return saida


def extrair_facetas(llm_leve, topicos: dict, cfg: Config,
                    subtopicos_alvo: Sequence[tuple[str, str]] | None = None,
                    verbose: bool = True) -> list[Faceta]:
    """Roda o extrator (modelo leve) sobre cada subtópico. Resultado em cache."""
    cache_path = cfg.out_dir / "indices" / "facetas.jsonl"
    cache: dict[str, dict] = {}
    if cache_path.exists():
        for linha in cache_path.read_text(encoding="utf-8").splitlines():
            if linha.strip():
                f = json.loads(linha)
                cache[f["id"]] = f

    pares = subtopicos_alvo or [(t, s) for t, subs in topicos.items()
                                for s in subs]
    facetas: list[Faceta] = []
    novos: list[dict] = []
    for topico, subtopico in pares:
        instrucao = topicos[topico][subtopico]
        sid = hash_curto(topico, subtopico)
        ja = [f for f in cache.values() if f["subtopico_id"] == sid]
        if ja:
            facetas.extend(Faceta(**{k: v for k, v in f.items()
                                     if k != "subtopico_id"}) for f in ja)
            continue

        sistema, user = P.prompt_extrator(topico, subtopico, instrucao,
                                          cfg.n_facetas_max)
        dados = llm_leve.complete_json(user, system=sistema, max_tokens=3000,
                                       default={"facetas": []})
        brutas = dados.get("facetas") or []
        if not brutas:  # a instrução vira uma faceta única, sem perder o subtópico
            brutas = [{"titulo": subtopico, "foco": instrucao,
                       "query": instrucao[:600], "termos_fortes": [],
                       "termos_apoio": []}]
        for i, b in enumerate(brutas[:cfg.n_facetas_max]):
            f = Faceta(
                id=f"{sid}-f{i}",
                topico=topico,
                subtopico=subtopico,
                titulo=str(b.get("titulo") or f"faceta {i}").strip(),
                foco=str(b.get("foco") or instrucao).strip(),
                query=str(b.get("query") or b.get("titulo") or subtopico).strip(),
                termos_fortes=_limpar_termos(b.get("termos_fortes")),
                termos_apoio=_limpar_termos(b.get("termos_apoio")),
            )
            facetas.append(f)
            novos.append({**asdict(f), "subtopico_id": sid})
        if verbose:
            n = len([f for f in facetas if f.subtopico == subtopico])
            print(f"  {subtopico[:60]:<60} -> {n} facetas")

    if novos:
        with open(cache_path, "a", encoding="utf-8") as fh:
            for f in novos:
                fh.write(json.dumps(f, ensure_ascii=False) + "\n")
    return facetas


def agrupar_por_subtopico(facetas: Sequence[Faceta]) -> dict[str, list[Faceta]]:
    grupos: dict[str, list[Faceta]] = {}
    for f in facetas:
        grupos.setdefault(f.subtopico, []).append(f)
    return grupos


# ===========================================================================
# §3 corpus — varredura lexical em uma passada
# ===========================================================================
# O Petrolês são vários GB de texto cru, uma sentença por linha, sem fronteira
# de documento, com números mascarados como <NUMBER> em parte dos arquivos.
# Embeddar tudo é inviável (milhões de trechos); então a busca é em dois
# estágios, como na fase 2:
#
#   estágio 1 (aqui)  varredura lexical streaming, UMA passada sobre TODOS os
#                     arquivos da pasta do corpus, pontuando TODAS as facetas ao
#                     mesmo tempo e guardando os top-K trechos por faceta;
#   estágio 2 (§5)    rerank semântico + MMR só sobre esses candidatos.
#
# O léxico não é escrito à mão (inviável para 40 subtópicos): vem dos
# `termos_fortes`/`termos_apoio` que o extrator produziu por faceta.
#
# Casamento de termos sem dependência externa: em vez de N regexes por trecho,
# monta-se um índice `termo -> facetas` e, por linha, testam-se n-gramas apenas
# a partir de tokens que iniciam algum termo conhecido. Isso derruba o custo
# para ~1 lookup por token na esmagadora maioria das posições.


class IndiceLexico:
    def __init__(self, facetas: Sequence[Faceta], cfg: Config):
        self.termo2faceta: dict[str, list[tuple[str, bool]]] = {}
        self.iniciais: set[str] = set()
        self.max_n = 1
        for f in facetas:
            for termo, forte in ([(t, True) for t in f.termos_fortes] +
                                 [(t, False) for t in f.termos_apoio]):
                toks = termo.split()
                if not toks:
                    continue
                self.termo2faceta.setdefault(termo, []).append((f.id, forte))
                self.iniciais.add(toks[0])
                self.max_n = max(self.max_n, len(toks))
        self.max_n = min(self.max_n, 5)
        self.cfg = cfg

    def __len__(self) -> int:
        return len(self.termo2faceta)

    def hits_linha(self, texto: str) -> dict[str, tuple[set[str], set[str]]]:
        """{faceta_id: (termos_fortes_vistos, termos_apoio_vistos)} para a linha."""
        toks = tokenizar(normalizar(texto))
        achados: dict[str, tuple[set[str], set[str]]] = {}
        n = len(toks)
        for i, tok in enumerate(toks):
            if tok not in self.iniciais:
                continue
            for k in range(1, min(self.max_n, n - i) + 1):
                termo = tok if k == 1 else " ".join(toks[i:i + k])
                alvo = self.termo2faceta.get(termo)
                if not alvo:
                    continue
                for fid, forte in alvo:
                    fortes, apoio = achados.setdefault(fid, (set(), set()))
                    (fortes if forte else apoio).add(termo)
        return achados


@dataclass
class _Linha:
    idx: int                 # índice da linha no arquivo (rastreabilidade)
    texto: str
    n_palavras: int
    n_number: int
    hits: dict[str, tuple[set[str], set[str]]]


def arquivos_do_corpus(cfg: Config) -> list[Path]:
    """Resolve os .txt do corpus, em ordem determinística.

    Aceita `corpus_dir` (todos os .txt da pasta), `corpus_txt` (lista explícita)
    ou `corpus_zip`. Nomes em `cfg.corpus_ignorar` são pulados — é assim que se
    exclui um arquivo do run sem mexer na pasta.
    """
    if cfg.corpus_dir:
        pasta = Path(cfg.corpus_dir)
        if not pasta.is_dir():
            raise FileNotFoundError(f"corpus_dir não existe: {pasta}")
        arquivos = sorted(pasta.glob("*.txt"))
    elif cfg.corpus_txt:
        arquivos = [Path(p) for p in cfg.corpus_txt]
    else:
        return []                                  # caso .zip, ver _iter_linhas
    ignorar = {n.lower() for n in cfg.corpus_ignorar}
    faltando = [str(a) for a in arquivos if not a.is_file()]
    if faltando:
        raise FileNotFoundError(f"arquivo(s) de corpus inexistente(s): {faltando}")
    return [a for a in arquivos if a.name.lower() not in ignorar]


def descrever_corpus(cfg: Config, verbose: bool = True) -> list[dict]:
    """Lista os arquivos que a varredura vai ler, com tamanho e forma estimados.

    Vale rodar antes da varredura: é o único ponto em que um arquivo esquecido
    (ou um a mais, entrando sem querer) aparece antes de custar meia hora.
    """
    if cfg.corpus_zip and not cfg.corpus_dir and not cfg.corpus_txt:
        import zipfile
        with zipfile.ZipFile(cfg.corpus_zip) as z:
            info = [{"arquivo": n, "bytes": z.getinfo(n).file_size}
                    for n in sorted(z.namelist()) if n.lower().endswith(".txt")]
        if verbose:
            for d in info:
                print(f"  {d['arquivo']:<52} {d['bytes'] / 1e9:>6.2f} GB  (no .zip)")
        return info

    arquivos = arquivos_do_corpus(cfg)
    if not arquivos:
        raise RuntimeError(
            "nenhum arquivo de corpus — defina cfg.corpus_dir, cfg.corpus_txt "
            "ou cfg.corpus_zip")
    info = []
    for caminho in arquivos:
        tam = caminho.stat().st_size
        with open(caminho, "rb") as fh:            # amostra de 20 MB
            amostra = fh.read(20_000_000)
        n_lin = max(amostra.count(b"\n"), 1)
        palavras_linha = (amostra.count(b" ") + n_lin) / n_lin
        fator = tam / max(len(amostra), 1)
        info.append({"arquivo": caminho.name, "bytes": tam,
                     "linhas_est": int(n_lin * fator),
                     "palavras_por_linha": round(palavras_linha, 1)})
    if verbose:
        total_lin = sum(d["linhas_est"] for d in info)
        print(f"corpus: {len(info)} arquivo(s), "
              f"{sum(d['bytes'] for d in info) / 1e9:.2f} GB, "
              f"~{total_lin / 1e6:.0f}M linhas")
        for d in info:
            print(f"  {d['arquivo']:<48} {d['bytes'] / 1e9:>6.2f} GB · "
                  f"~{d['linhas_est'] / 1e6:>6.1f}M linhas · "
                  f"{d['palavras_por_linha']:>5.1f} palavras/linha · "
                  f"{100 * d['linhas_est'] / total_lin:>4.0f}% das linhas")
    return info


def _iter_linhas_corpus(cfg: Config) -> Iterator[tuple[str, int, str]]:
    """Gera `(nome_arquivo, indice_linha, texto)` de todos os arquivos, em fila.

    Os arquivos são percorridos em sequência e tratados como um corpus só; o
    nome volta em cada linha apenas para a rastreabilidade do `chunk_id`. A
    janela nunca atravessa a fronteira entre dois arquivos (ver `varrer_corpus`).
    """
    arquivos = arquivos_do_corpus(cfg)
    if arquivos:
        for caminho in arquivos:
            with open(caminho, encoding="utf-8", errors="replace") as fh:
                for i, bruto in enumerate(fh):
                    yield caminho.name, i, bruto.strip()
        return
    if cfg.corpus_zip:
        import zipfile
        ignorar = {n.lower() for n in cfg.corpus_ignorar}
        with zipfile.ZipFile(cfg.corpus_zip) as z:
            for nome in sorted(z.namelist()):
                if not nome.lower().endswith(".txt"):
                    continue
                if Path(nome).name.lower() in ignorar:
                    continue
                with z.open(nome) as fh:
                    for i, bruto in enumerate(fh):
                        yield (Path(nome).name, i,
                               bruto.decode("utf-8", errors="replace").strip())
        return
    raise RuntimeError(
        "nenhum arquivo de corpus — defina cfg.corpus_dir, cfg.corpus_txt "
        "ou cfg.corpus_zip")


def varrer_corpus(facetas: Sequence[Faceta], cfg: Config,
                  limite_linhas: int | None = None,
                  verbose: bool = True) -> Path:
    """Estágio 1: uma passada no corpus, top-K trechos por faceta em disco.

    Custa alguns minutos e roda UMA vez por conjunto de facetas. O resultado é
    `saida_fase3/indices/candidatos.jsonl`; se já existir, é reaproveitado
    (apague o arquivo para reindexar).
    """
    destino = cfg.out_dir / "indices" / "candidatos.jsonl"
    manifesto = cfg.out_dir / "indices" / "candidatos_manifesto.json"
    nomes_arquivos = [a.name for a in arquivos_do_corpus(cfg)] or ["<zip>"]
    assinatura = hash_curto(sorted(f.id for f in facetas), nomes_arquivos,
                            cfg.alvo_palavras_trecho, cfg.sobreposicao_trecho,
                            cfg.top_k_lexical)
    if destino.exists() and manifesto.exists():
        if json.loads(manifesto.read_text())["assinatura"] == assinatura:
            if verbose:
                print(f"índice já existe e confere ({destino}) — reaproveitando")
            return destino

    indice = IndiceLexico(facetas, cfg)
    if verbose:
        print(f"varredura: {len(facetas)} facetas, {len(indice)} termos distintos")
        print(f"arquivos ({len(nomes_arquivos)}): {', '.join(nomes_arquivos)}")
    if len(indice) == 0:
        raise RuntimeError("nenhum termo no léxico — o extrator não devolveu termos")

    heaps: dict[str, list] = {f.id: [] for f in facetas}
    contador = 0
    janela: deque[_Linha] = deque()
    palavras_janela = 0
    a_liberar = max(1, int(cfg.alvo_palavras_trecho *
                           (1.0 - cfg.sobreposicao_trecho)))
    arquivo_atual = None
    t0 = time.time()
    n_linhas = 0
    linhas_por_arquivo: Counter = Counter()
    trechos_por_arquivo: Counter = Counter()

    def fechar_janela(nome_arquivo: str):
        nonlocal contador
        soma_palavras = sum(l.n_palavras for l in janela)
        if not (cfg.min_palavras <= soma_palavras <= cfg.max_palavras):
            return
        soma_number = sum(l.n_number for l in janela)
        if soma_number / max(soma_palavras, 1) > cfg.max_frac_number:
            return
        acum: dict[str, tuple[set[str], set[str]]] = {}
        for l in janela:
            for fid, (fortes, apoio) in l.hits.items():
                a, b = acum.setdefault(fid, (set(), set()))
                a |= fortes
                b |= apoio
        if not acum:
            return
        texto_cache = None
        for fid, (fortes, apoio) in acum.items():
            if not fortes and len(apoio) < 2:      # gate anti-falso-positivo
                continue
            score = (cfg.peso_termo_forte * min(len(fortes), cfg.cap_termos)
                     + cfg.peso_termo_apoio * min(len(apoio), cfg.cap_termos))
            h = heaps[fid]
            if len(h) >= cfg.top_k_lexical and score <= h[0][0]:
                continue
            if texto_cache is None:
                texto_cache = " ".join(l.texto for l in janela)
                trechos_por_arquivo[nome_arquivo] += 1
            contador += 1
            ini, fim = janela[0].idx, janela[-1].idx
            item = (score, contador, {
                "chunk_id": f"{nome_arquivo}:{ini}-{fim}",
                "arquivo": nome_arquivo,
                "linha_ini": ini,
                "linha_fim": fim,
                "faceta_id": fid,
                "lex_score": score,
                "termos_fortes": sorted(fortes),
                "texto": texto_cache,
            })
            if len(h) < cfg.top_k_lexical:
                heapq.heappush(h, item)
            else:
                heapq.heapreplace(h, item)

    for nome, i, texto in _iter_linhas_corpus(cfg):
        if nome != arquivo_atual:
            # a janela não atravessa a fronteira entre arquivos: um trecho
            # metade NILC metade ANP não corresponde a texto nenhum
            janela.clear()
            palavras_janela = 0
            arquivo_atual = nome
        n_linhas += 1
        linhas_por_arquivo[nome] += 1
        if limite_linhas and n_linhas > limite_linhas:
            break
        if not texto:
            continue
        linha = _Linha(
            idx=i,
            texto=texto,
            n_palavras=texto.count(" ") + 1,
            n_number=texto.count("<NUMBER>"),
            hits=indice.hits_linha(texto),
        )
        janela.append(linha)
        palavras_janela += linha.n_palavras

        # Fecha por orçamento de PALAVRAS (não de linhas): é o que iguala
        # arquivos de densidade diferente. `max_linhas_trecho` é só a trava
        # para o caso de linhas curtíssimas nunca alcançarem o orçamento.
        if (palavras_janela >= cfg.alvo_palavras_trecho
                or len(janela) >= cfg.max_linhas_trecho):
            fechar_janela(nome)
            liberadas = 0
            while janela and liberadas < a_liberar:
                liberadas += janela[0].n_palavras
                palavras_janela -= janela.popleft().n_palavras

        if verbose and n_linhas % 5_000_000 == 0:
            taxa = n_linhas / max(time.time() - t0, 1e-9)
            print(f"  {n_linhas / 1e6:>5.0f}M linhas · "
                  f"{time.time() - t0:>5.0f}s · {taxa / 1000:,.0f}k linhas/s")

    # Quem sobreviveu ao top-K, por arquivo de origem: é o número que diz se um
    # arquivo do corpus está de fato contribuindo ou só consumindo varredura.
    guardados_por_arquivo: Counter = Counter()
    with open(destino, "w", encoding="utf-8") as fh:
        for fid, h in heaps.items():
            for _, _, payload in sorted(h, key=lambda x: -x[0]):
                guardados_por_arquivo[payload["arquivo"]] += 1
                fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

    total_guardados = sum(guardados_por_arquivo.values())
    manifesto.write_text(json.dumps({
        "assinatura": assinatura,
        "arquivos": nomes_arquivos,
        "n_linhas": n_linhas,
        "segundos": round(time.time() - t0, 1),
        "linhas_por_arquivo": dict(linhas_por_arquivo),
        "trechos_avaliados_por_arquivo": dict(trechos_por_arquivo),
        "candidatos_por_arquivo": dict(guardados_por_arquivo),
        "por_faceta": {fid: len(h) for fid, h in heaps.items()},
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    if verbose:
        vazias = [fid for fid, h in heaps.items() if not h]
        print(f"varredura concluída: {n_linhas:,} linhas em "
              f"{time.time() - t0:,.0f}s")
        print(f"  candidatos guardados: {total_guardados:,}")
        print(f"  {'arquivo':<48}{'linhas lidas':>14}{'candidatos':>12}{'share':>8}")
        for nome in nomes_arquivos:
            g = guardados_por_arquivo.get(nome, 0)
            print(f"  {nome:<48}{linhas_por_arquivo.get(nome, 0):>14,}{g:>12,}"
                  f"{(g / total_guardados if total_guardados else 0):>8.1%}")
        for nome in nomes_arquivos:
            share_linhas = linhas_por_arquivo.get(nome, 0) / max(n_linhas, 1)
            share_cand = guardados_por_arquivo.get(nome, 0) / max(total_guardados, 1)
            if share_linhas > 0.25 and share_cand < 0.05:
                print(f"  NOTA: '{nome}' é {share_linhas:.0%} das linhas lidas e "
                      f"só {share_cand:.1%} dos candidatos.\n"
                      f"        Se isso se repetir, vale pô-lo em "
                      f"cfg.corpus_ignorar e reindexar mais rápido.")
        if vazias:
            print(f"  ATENÇÃO — {len(vazias)} faceta(s) sem candidato: {vazias[:5]}")
    return destino


def carregar_candidatos(cfg: Config) -> dict[str, list[dict]]:
    caminho = cfg.out_dir / "indices" / "candidatos.jsonl"
    por_faceta: dict[str, list[dict]] = {}
    with open(caminho, encoding="utf-8") as fh:
        for linha in fh:
            if linha.strip():
                c = json.loads(linha)
                por_faceta.setdefault(c["faceta_id"], []).append(c)
    return por_faceta


# ===========================================================================
# §4 embeddings
# ===========================================================================
# sentence-transformers multilíngue, rodando local. Serve a quatro coisas:
# rerank do estágio 2, MMR, scorer de vícios (§7) e a distribuição cujo
# entropia mede a saturação do subtópico (§8). Como o mesmo texto reaparece
# entre rodadas, há cache em disco por hash.


class Embedder:
    def __init__(self, cfg: Config, verbose: bool = True):
        self.cfg = cfg
        self.dir_cache = cfg.out_dir / "embeddings"
        self.dir_cache.mkdir(parents=True, exist_ok=True)
        self._cache_path = self.dir_cache / "cache.npz"
        self._cache: dict[str, np.ndarray] = {}
        if self._cache_path.exists():
            with np.load(self._cache_path) as z:
                self._cache = {k: z[k] for k in z.files}
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "sentence-transformers é necessário para os embeddings:\n"
                "    pip install sentence-transformers"
            ) from exc
        nome = cfg.modelo_embedding.replace("sentence-transformers/", "")
        self.model = SentenceTransformer(nome)
        self.dim = self.model.get_sentence_embedding_dimension()
        if verbose:
            print(f"embedder: {nome} (dim={self.dim}) · "
                  f"cache com {len(self._cache)} vetores")

    def encode(self, textos: Sequence[str], batch_size: int = 64,
               usar_cache: bool = True, progresso: bool = False) -> np.ndarray:
        textos = list(textos)
        if not textos:
            return np.zeros((0, self.dim), dtype=np.float32)
        chaves = [hash_curto(t, n=16) for t in textos]
        faltando = [i for i, k in enumerate(chaves)
                    if not usar_cache or k not in self._cache]
        if faltando:
            novos = self.model.encode(
                [textos[i] for i in faltando], batch_size=batch_size,
                normalize_embeddings=True, show_progress_bar=progresso)
            novos = np.asarray(novos, dtype=np.float32)
            for pos, i in enumerate(faltando):
                self._cache[chaves[i]] = novos[pos]
        return np.stack([self._cache[k] for k in chaves])

    def salvar_cache(self) -> None:
        if self._cache:
            np.savez_compressed(self._cache_path, **self._cache)


def cosseno(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Cosseno entre vetores já normalizados (produto interno)."""
    return a @ b.T


def _z(v: np.ndarray) -> np.ndarray:
    s = v.std()
    return (v - v.mean()) / s if s > 1e-9 else np.zeros_like(v)


# ===========================================================================
# §5 recuperação — estágio 2 e montagem dos documentos de geração
# ===========================================================================
# Do pool lexical de cada faceta: rerank por similaridade com a query da faceta,
# seleção com MMR (relevante E diverso) e fatiamento em blocos de N trechos.
# Cada bloco é um "documento" no sentido do passo 1 do pipeline — e é a unidade
# que o critério de parada (§8) percorre quando o subtópico satura.


def _mmr(relevancia: np.ndarray, E: np.ndarray, n: int,
         lam: float, dup: float) -> list[int]:
    ordem = list(np.argsort(-relevancia)[:max(n * 12, 120)])
    escolhidos: list[int] = []
    while ordem and len(escolhidos) < n:
        melhor, melhor_val = None, -np.inf
        for j in ordem:
            sim_max = max((float(E[j] @ E[s]) for s in escolhidos), default=0.0)
            if sim_max > dup:
                continue
            val = lam * float(relevancia[j]) - (1 - lam) * sim_max
            if val > melhor_val:
                melhor, melhor_val = j, val
        if melhor is None:
            break
        escolhidos.append(melhor)
        ordem.remove(melhor)
    return escolhidos


def montar_documentos_faceta(faceta: Faceta, candidatos: list[dict],
                             emb: Embedder, cfg: Config) -> list[dict]:
    """Rerank + MMR + fatiamento em blocos. Devolve os blocos, sem consolidar."""
    if not candidatos:
        return []
    textos = [c["texto"] for c in candidatos]
    E = emb.encode(textos)
    q = emb.encode([faceta.texto_query])[0]
    sem = E @ q
    lex = np.array([c["lex_score"] for c in candidatos], dtype=np.float32)
    combinado = cfg.peso_lexical * _z(lex) + cfg.peso_semantico * _z(sem)

    n_total = cfg.n_trechos_por_documento * cfg.n_documentos_por_faceta
    escolhidos = _mmr(combinado, E, n_total, cfg.mmr_lambda, cfg.mmr_dup_threshold)

    blocos = []
    N = cfg.n_trechos_por_documento
    for b in range(0, len(escolhidos), N):
        fatia = escolhidos[b:b + N]
        if len(fatia) < max(2, N // 2):     # bloco final raquítico não vira doc
            break
        blocos.append({
            "doc_id": f"{faceta.id}-d{b // N}",
            "faceta_id": faceta.id,
            "subtopico": faceta.subtopico,
            "topico": faceta.topico,
            "trechos": [candidatos[i]["texto"] for i in fatia],
            "chunk_ids": [candidatos[i]["chunk_id"] for i in fatia],
            "scores": [float(combinado[i]) for i in fatia],
        })
    return blocos


def plano_de_documentos(facetas: Sequence[Faceta], candidatos_por_faceta: dict,
                        emb: Embedder, cfg: Config,
                        verbose: bool = True) -> list[dict]:
    """Fila ordenada de documentos de um subtópico.

    Intercala as facetas (f0d0, f1d0, f2d0, f0d1, ...): o subtópico cobre a
    largura da instrução antes de aprofundar em qualquer recorte.
    """
    por_faceta = []
    for f in facetas:
        blocos = montar_documentos_faceta(f, candidatos_por_faceta.get(f.id, []),
                                          emb, cfg)
        if verbose:
            print(f"    {f.titulo[:52]:<52} {len(candidatos_por_faceta.get(f.id, [])):>5} cand "
                  f"-> {len(blocos)} doc(s)")
        por_faceta.append(blocos)
    plano = []
    for i in range(max((len(b) for b in por_faceta), default=0)):
        for blocos in por_faceta:
            if i < len(blocos):
                plano.append(blocos[i])
    return plano


# ===========================================================================
# §6 operações de LLM
# ===========================================================================


def _marcador(rodada: int, doc_id: str, seed: int) -> str:
    """Torna o prompt de geração único por rodada.

    O backend cacheia por hash do pedido: sem isto, duas rodadas com o mesmo
    documento e o mesmo few-shot devolveriam questões idênticas do cache. Com
    isto, rodadas diferentes divergem e a MESMA rodada continua cacheável — o
    notebook pode ser re-executado sem pagar de novo.
    """
    return f"[lote {doc_id} · rodada {rodada} · seed {seed}]"


def consolidar_documento(llm_leve, doc: dict, faceta: Faceta,
                         cfg: Config) -> str:
    cache = cfg.out_dir / "documentos" / f"{doc['doc_id']}.md"
    if cache.exists():
        return cache.read_text(encoding="utf-8")
    sistema, user = P.prompt_consolidacao(
        faceta.subtopico, faceta.foco, doc["trechos"], cfg.max_palavras_documento)
    texto = llm_leve.complete(user, system=sistema,
                              max_tokens=int(cfg.max_palavras_documento * 2.5))
    cache.write_text(texto, encoding="utf-8")
    return texto


def _normalizar_questao(bruta: dict, cfg: Config) -> dict | None:
    """Valida a forma da questão. Devolve None se estiver quebrada.

    Os campos que o gerador (e o refinador) produzem. `difficulty` é do judge e
    `nota` também — não são inventados aqui, e não aparecem no dict devolvido
    justamente para que `refinar_questao`, ao mesclar, não sobrescreva o que o
    judge já decidiu.

    `dificuldade_gerador` é a exceção: é uma autoavaliação do PRÓPRIO gerador
    (ver SYS_GERADOR em prompts_fase3.py), então é legítimo ele produzir de
    novo a cada refinamento — não pertence ao judge, não há o que proteger.
    Fica de fora do dict se vier ausente ou fora do vocabulário esperado, em
    vez de forçar um default: um valor ausente é mais honesto que "media"
    inventado aqui.
    """
    try:
        stem = str(bruta["stem"]).strip()
        alts = [str(a).strip() for a in bruta["alternatives"]]
        idx = int(bruta["correct_answer_index"])
    except (KeyError, TypeError, ValueError):
        return None
    if not stem or len(alts) != cfg.n_alternativas or not (0 <= idx < len(alts)):
        return None
    if any(not a for a in alts) or len(set(alts)) != len(alts):
        return None
    q = {"stem": stem, "alternatives": alts, "correct_answer_index": idx}
    dif_ger = str(bruta.get("dificuldade_gerador", "")).strip().lower()
    if dif_ger in ("facil", "media", "dificil"):
        q["dificuldade_gerador"] = dif_ger
    return q


def embaralhar_posicao(questao: dict, rng: random.Random) -> dict:
    """Sorteia a posição da alternativa correta (pós-processamento).

    O prompt do gerador não pede mais variação de posição entre A/B/C/D: isso é
    contabilidade sobre um lote inteiro, que um modelo faz mal e uma linha de
    código faz exatamente. Aplicado no fim, depois do refinamento, logo antes de
    armazenar — o scorer de vícios é indiferente à posição, então nada do que
    veio antes é invalidado.
    """
    q = dict(questao)
    alts = list(q["alternatives"])
    correta = alts[int(q["correct_answer_index"])]
    rng.shuffle(alts)
    q["alternatives"] = alts
    q["correct_answer_index"] = alts.index(correta)   # sem duplicatas: ver acima
    return q


def amostrar_exemplo_externo(rng: random.Random,
                             pool: Sequence[dict] = EXEMPLOS_ARC) -> dict | None:
    """1 exemplo de outro domínio, sorteado uniformemente do pool externo.

    Hoje o pool é só o ARC-Challenge (5 itens, ver exemplos_externos_fase3.py).
    Devolve None se o pool estiver vazio, para o chamador poder desligar sem
    precisar checar `cfg.usar_exemplos_externos` de novo.
    """
    if not pool:
        return None
    return rng.choice(list(pool))


def gerar_lote(llm_forte, doc: dict, faceta: Faceta, documento: str,
               exemplos: Sequence[dict], rodada: int, cfg: Config,
               exemplo_externo: dict | None = None) -> list[dict]:
    sistema, user = P.prompt_geracao(
        subtopico=faceta.subtopico, topico=faceta.topico, faceta_foco=faceta.foco,
        documento=documento, exemplos=exemplos, exemplo_externo=exemplo_externo,
        n_questoes=cfg.n_questoes_por_lote, n_alternativas=cfg.n_alternativas,
        marcador_rodada=_marcador(rodada, doc["doc_id"], cfg.seed))
    dados = llm_forte.complete_json(user, system=sistema, max_tokens=12000,
                                    default={"questoes": []})
    brutas = dados.get("questoes") if isinstance(dados, dict) else dados
    saida = []
    for i, b in enumerate(brutas or []):
        q = _normalizar_questao(b, cfg)
        if q is None:
            continue
        q.update({
            "id": f"{doc['doc_id']}-r{rodada}-q{i}",
            "doc_id": doc["doc_id"],
            "faceta_id": faceta.id,
            "faceta_titulo": faceta.titulo,
            "subtopico": faceta.subtopico,
            "topico": faceta.topico,
            "chunk_ids": doc["chunk_ids"],
            "rodada": rodada,
            "gerado_em": time.strftime("%Y-%m-%dT%H:%M:%S"),
        })
        saida.append(q)
    return saida


def julgar_lote(llm_judge, questoes: Sequence[dict], subtopico: str,
                cfg: Config) -> list[dict]:
    """Passo 4: descarta as incorretas, dá nota [0,1] e dificuldade às demais."""
    if not questoes:
        return []
    sistema, user = P.prompt_judge(questoes, subtopico)
    dados = llm_judge.complete_json(user, system=sistema, max_tokens=8000,
                                    default={"avaliacoes": []})
    avals = {str(a.get("id")): a for a in (dados.get("avaliacoes") or [])}
    aprovadas = []
    for q in questoes:
        a = avals.get(str(q["id"]))
        if a is None:                     # sem veredito não passa
            continue
        if not a.get("correta_ok", False):
            continue
        try:
            nota = float(a.get("nota"))
        except (TypeError, ValueError):
            nota = float(np.mean([float(a.get(k, 0.0)) for k in
                                  ("correcao", "clareza", "alternativas",
                                   "relevancia")]))
        nota = float(min(max(nota, 0.0), 1.0))
        if nota < cfg.nota_minima_aprovacao:
            continue
        dif = str(a.get("dificuldade", "media")).lower()
        q = dict(q)
        q["nota"] = round(nota, 3)
        q["difficulty"] = dif if dif in ("facil", "media", "dificil") else "media"
        q["judge"] = {k: a.get(k) for k in
                      ("correcao", "clareza", "alternativas", "relevancia",
                       "comentario")}
        aprovadas.append(q)
    return aprovadas


def refinar_questao(llm_forte, questao: dict, diagnostico: dict,
                    documento: str | None, cfg: Config) -> dict | None:
    sistema, user = P.prompt_refinamento(questao, diagnostico, documento)
    dados = llm_forte.complete_json(user, system=sistema, max_tokens=6000,
                                    default={})
    q = _normalizar_questao(dados, cfg) if dados else None
    if q is None:
        return None
    nova = dict(questao)
    nova.update(q)
    nova["refinada"] = True
    nova["refinamento"] = str(dados.get("mudancas", ""))[:400]
    return nova


# ===========================================================================
# §7 scorer de vícios (passo 5) — determinístico, sem LLM
# ===========================================================================
# Quatro vícios de construção que fazem a questão ser respondível sem saber o
# conteúdo. Cada um é normalizado para [0,1] — 0 = sem vício, 1 = saturado —
# para que a tolerância (passo 6) seja um número comparável entre eles.
#
#   similaridade   a correta se parece mais com o enunciado do que os
#                  distratores (cosseno de embedding + sobreposição de
#                  palavras de conteúdo). Mede-se a VANTAGEM da correta;
#                  distrator parecido demais não é vício, é distrator bom.
#   comprimento    a correta destoa em tamanho — mais longa (o caso comum, o
#                  autor detalha a certa) ou mais curta. Desvio em módulo.
#   distratores    distrator "lixo": ou sem relação semântica com o enunciado
#                  (elimina-se de bate-pronto), ou carregado de linguagem
#                  absolutista que a correta não tem (entrega por eliminação).
#   racionalizacao distrator que se JUSTIFICA dentro do próprio texto,
#                  minimizando o seu ponto fraco ("assumindo que...",
#                  "pressupondo que...", "...tende a ser secundário/pequeno").
#                  Achado ao analisar a rodada de 102 questões da fase 3: esse
#                  padrão apareceu em 26 delas, sempre em distrator (nunca na
#                  correta) e concentrado nas questões que 3 modelos Ollama
#                  pequenos (qwen2.5:7b, phi4-mini, llama3.2:3b) acertaram sem
#                  ver o gabarito — um "tell" de prova de múltipla escolha que
#                  não depende de conhecimento de domínio (ver
#                  analysis/avaliacao_dificuldade_ollama.ipynb). Os três
#                  vícios acima não capturam isso: similaridade olha proximidade
#                  com o enunciado, comprimento olha só caracteres, distratores
#                  só pega irrelevância ou "sempre/nunca" literal.

PALAVRAS_ARMADILHA = (
    "apenas", "somente", "exclusivamente", "unico", "unica", "exclusivo",
    "exclusiva", "nunca", "sempre", "todos", "todas", "nenhum", "nenhuma",
    "qualquer", "impossivel", "garante", "elimina", "eliminando", "dispensa",
    "dispensando", "independentemente", "invariavelmente", "obrigatoriamente",
    "totalmente", "completamente", "jamais",
)
_RE_ARMADILHA = re.compile(
    r"\b(" + "|".join(PALAVRAS_ARMADILHA) + r")\b")

# Verbos de abertura de uma racionalização + o desfecho que ela costuma ter
# (minimizar a própria falha). Testado contra as 102 questões da fase 3: 0
# falsos positivos na alternativa correta, 36 ocorrências em distratores,
# espalhadas por 26 questões.
FRASES_RACIONALIZACAO = (
    r"assumindo que", r"pressupondo que", r"supondo que", r"entendendo que",
    r"por entender que", r"apostando que", r"acreditando que", r"avaliando que",
    r"considerando que", r"partindo do principio",
    r"tende(?:m)? a ser (?:pequen\w*|secundari\w*|irrelevant\w*|desprezivel\w*)",
    r"nao (?:e relevante|influencia\w*|impacta\w*|afeta\w*)",
    r"pouco relevante",
)
_RE_RACIONALIZACAO = re.compile(
    r"\b(" + "|".join(FRASES_RACIONALIZACAO) + r")\b")


def _jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if (a or b) else 0.0


def _clip01(x: float) -> float:
    return float(min(max(x, 0.0), 1.0))


def pontuar_vicios(questao: dict, emb: Embedder, cfg: Config) -> dict:
    """Devolve `{vicio: {valor, limite, excedeu, detalhe}}` para cada vício."""
    stem = questao["stem"]
    alts = questao["alternatives"]
    ic = int(questao["correct_answer_index"])
    idx_d = [i for i in range(len(alts)) if i != ic]

    E = emb.encode([stem] + alts)
    e_stem, e_alts = E[0], E[1:]
    sims = e_alts @ e_stem

    ps = palavras_conteudo(stem)
    jacc = np.array([_jaccard(ps, palavras_conteudo(a)) for a in alts])

    # -- vício 1: vantagem de similaridade da correta -----------------------
    d_emb = float(sims[ic] - np.mean(sims[idx_d]))
    d_lex = float(jacc[ic] - np.mean(jacc[idx_d]))
    v_sim = max(_clip01(d_emb / cfg.tau_similaridade),
                _clip01(d_lex / cfg.tau_similaridade))

    # -- vício 2: desbalanceamento de comprimento ---------------------------
    comp = np.array([len(a) for a in alts], dtype=float)
    media_d = float(np.mean(comp[idx_d])) or 1.0
    desvio = (float(comp[ic]) - media_d) / media_d
    v_comp = _clip01(abs(desvio) / cfg.tau_comprimento)

    # -- vício 3: distratores lixo ------------------------------------------
    # "sem relação com o enunciado" é relativo ao próprio item: um piso absoluto
    # de cosseno depende do modelo de embedding e não sobrevive à troca dele.
    piso = max(cfg.lim_distrator_irrelevante,
               cfg.fator_distrator_irrelevante * float(sims[ic]))
    irrelevantes, armadilhas = [], []
    for i in idx_d:
        if float(sims[i]) < piso:
            irrelevantes.append(chr(65 + i))
        if _RE_ARMADILHA.search(normalizar(alts[i])):
            armadilhas.append(chr(65 + i))
    correta_tem_armadilha = bool(_RE_ARMADILHA.search(normalizar(alts[ic])))
    frac_irr = len(irrelevantes) / len(idx_d)
    frac_arm = len(armadilhas) / len(idx_d)
    if correta_tem_armadilha:          # não há concentração se a correta também tem
        frac_arm = max(0.0, frac_arm - 1.0 / len(idx_d))
    v_dist = _clip01(max(frac_irr, frac_arm))

    # -- vício 4: distrator que racionaliza o próprio ponto fraco -----------
    racionalizantes = [chr(65 + i) for i in idx_d
                        if _RE_RACIONALIZACAO.search(normalizar(alts[i]))]
    correta_tem_racionalizacao = bool(_RE_RACIONALIZACAO.search(normalizar(alts[ic])))
    frac_racio = len(racionalizantes) / len(idx_d)
    if correta_tem_racionalizacao:     # mesma cortesia do vício 3: não pune se a correta também usa
        frac_racio = max(0.0, frac_racio - 1.0 / len(idx_d))
    v_racio = _clip01(frac_racio)

    diag = {
        "similaridade": {
            "valor": round(v_sim, 3), "limite": cfg.tol_similaridade,
            "detalhe": (f"vantagem da correta: cosseno {d_emb:+.3f}, "
                        f"léxico {d_lex:+.3f} (alternativa "
                        f"{chr(65 + ic)})")},
        "comprimento": {
            "valor": round(v_comp, 3), "limite": cfg.tol_comprimento,
            "detalhe": (f"correta {int(comp[ic])} chars vs média dos "
                        f"distratores {media_d:.0f} ({desvio:+.0%})")},
        "distratores": {
            "valor": round(v_dist, 3), "limite": cfg.tol_distratores,
            "detalhe": (f"sem relação com o enunciado (piso {piso:.2f}): "
                        f"{irrelevantes or '—'}; "
                        f"linguagem absolutista: {armadilhas or '—'}"
                        + (" (a correta também tem)" if correta_tem_armadilha else ""))},
        "racionalizacao": {
            "valor": round(v_racio, 3), "limite": cfg.tol_racionalizacao,
            "detalhe": (f"distrator se justifica minimizando o próprio ponto "
                        f"fraco (\"assumindo que...\", \"pressupondo que...\", "
                        f"\"...tende a ser secundário\"): {racionalizantes or '—'}"
                        + (" (a correta também tem)" if correta_tem_racionalizacao else ""))},
    }
    for k, v in diag.items():
        v["excedeu"] = v["valor"] > v["limite"]
    return diag


def tem_vicio(diagnostico: dict) -> bool:
    return any(v["excedeu"] for v in diagnostico.values())


def resumo_vicios(diagnostico: dict) -> dict[str, float]:
    return {k: v["valor"] for k, v in diagnostico.items()}


# ===========================================================================
# §8 entropia e critério de parada (passo 9)
# ===========================================================================
# A pergunta é "o subtópico ainda rende questão nova?". A resposta é a entropia
# de Shannon normalizada da distribuição dos embeddings (questão + alternativa
# correta) acumulados no pool daquele subtópico, sobre uma clusterização FIXA,
# treinada uma vez — se o codebook mudasse a cada rodada, a comparação entre
# rodadas não significaria nada.
#
# O codebook é treinado UMA VEZ POR SUBTÓPICO, sobre os embeddings dos trechos
# candidatos daquele subtópico. Por que não um codebook global do domínio: as
# questões de um subtópico caem quase todas no mesmo cluster global, a entropia
# fica constante em zero e o critério de parada dispara já na primeira rodada.
# O que interessa medir é a cobertura DENTRO do subtópico — se as questões novas
# ainda visitam regiões do material que as anteriores não visitaram — e para isso
# a clusterização precisa resolver a estrutura fina daquele material.
#
# A comparação de entropia é sempre entre rodadas do MESMO subtópico, então
# codebooks distintos entre subtópicos não atrapalham. O que não pode mudar é o
# codebook de um subtópico ao longo das rodadas dele — por isso fica em disco e
# nunca é re-treinado (só com `forcar=True`).


def texto_para_embedding(questao: dict) -> str:
    """Par questão + alternativa correta — a unidade semântica que o passo 7
    manda armazenar e a que a entropia observa."""
    return (questao["stem"] + " " +
            questao["alternatives"][int(questao["correct_answer_index"])])


class Codebook:
    """Clusterização fixa. Treinada uma vez, salva em disco, nunca re-treinada."""

    def __init__(self, centros: np.ndarray, meta: dict):
        self.centros = centros
        self.meta = meta

    @property
    def k(self) -> int:
        return int(self.centros.shape[0])

    def atribuir(self, E: np.ndarray) -> np.ndarray:
        if E.size == 0:
            return np.zeros(0, dtype=int)
        return np.argmax(E @ self.centros.T, axis=1)

    def salvar(self, caminho: Path) -> None:
        np.savez_compressed(caminho, centros=self.centros,
                            meta=np.array(json.dumps(self.meta)))

    @classmethod
    def carregar(cls, caminho: Path) -> "Codebook":
        with np.load(caminho, allow_pickle=False) as z:
            return cls(z["centros"], json.loads(str(z["meta"])))


def treinar_codebook(textos: Sequence[str], emb: Embedder, cfg: Config,
                     nome: str, k: int | None = None, fonte: str = "chunks",
                     forcar: bool = False, verbose: bool = True) -> Codebook:
    """Treina (ou recupera do disco) a clusterização fixa identificada por `nome`."""
    caminho = cfg.out_dir / "indices" / f"codebook_{hash_curto(nome)}.npz"
    if caminho.exists() and not forcar:
        cb = Codebook.carregar(caminho)
        if verbose:
            print(f"  codebook '{nome[:40]}' já treinado (k={cb.k}) — reaproveitando")
        return cb
    if len(textos) < 8:
        raise RuntimeError(
            f"textos de treino insuficientes para o codebook de '{nome}' "
            f"({len(textos)}) — a varredura do corpus não achou candidatos")
    try:
        from sklearn.cluster import KMeans
    except ImportError as exc:
        raise RuntimeError("scikit-learn é necessário: pip install scikit-learn") from exc

    E = emb.encode(list(textos), progresso=False)
    k = min(k or cfg.n_clusters_codebook, max(2, len(textos) // 8))
    km = KMeans(n_clusters=k, random_state=cfg.seed, n_init=10).fit(E)
    centros = km.cluster_centers_.astype(np.float32)
    centros /= (np.linalg.norm(centros, axis=1, keepdims=True) + 1e-9)
    cb = Codebook(centros, {"nome": nome, "fonte": fonte, "k": int(k),
                            "n_treino": len(textos),
                            "modelo": cfg.modelo_embedding})
    cb.salvar(caminho)
    if verbose:
        print(f"  codebook '{nome[:40]}': k={k} sobre {len(textos):,} textos ({fonte})")
    return cb


def codebook_do_subtopico(subtopico: str, facetas: Sequence[Faceta],
                          candidatos_por_faceta: dict, emb: Embedder,
                          cfg: Config, verbose: bool = True) -> Codebook:
    """Atalho: treina o codebook fixo de um subtópico com os trechos dele."""
    ids = {f.id for f in facetas if f.subtopico == subtopico}
    textos = [c["texto"] for fid in ids
              for c in candidatos_por_faceta.get(fid, [])]
    return treinar_codebook(textos, emb, cfg, nome=f"sub::{subtopico}",
                            fonte="chunks do subtópico", verbose=verbose)


def entropia_normalizada(rotulos: Sequence[int], k: int) -> float:
    """Shannon sobre a distribuição de clusters, dividida por log(k)."""
    if len(rotulos) == 0 or k <= 1:
        return 0.0
    cont = np.bincount(np.asarray(rotulos, dtype=int), minlength=k)
    p = cont[cont > 0] / cont.sum()
    return float(-(p * np.log(p)).sum() / math.log(k)) + 0.0


@dataclass
class EstadoSubtopico:
    """O estado que o pipeline carrega por subtópico — só isto (passo 9)."""

    subtopico: str
    topico: str = ""
    doc_idx: int = 0                                  # posição na fila de docs
    rodada: int = 0                                   # rodada global do subtópico
    rodadas_no_documento: int = 0
    rodadas_estagnadas: int = 0
    historico_entropia: list[float] = field(default_factory=list)
    ids_pool: list[str] = field(default_factory=list)  # questões aprovadas
    concluido: bool = False

    # ------------------------------------------------------------ passo 9 --
    def registrar_rodada(self, entropia: float, n_pool: int, cfg: "Config") -> dict:
        """Anota a entropia da rodada e atualiza o contador de estagnação.

        Duas guardas contra falso positivo de estagnação: a primeira rodada não
        tem com o que comparar, e um pool ainda pequeno tem entropia baixa por
        falta de amostra, não por saturação do subtópico.
        """
        primeira = not self.historico_entropia
        anterior = self.historico_entropia[-1] if self.historico_entropia else 0.0
        ganho = entropia - anterior
        self.historico_entropia.append(round(float(entropia), 6))

        maduro = n_pool >= cfg.min_questoes_para_entropia
        if primeira or not maduro:
            motivo = "aquecendo" if not maduro else "primeira rodada"
        elif ganho < cfg.limiar_ganho_entropia:
            self.rodadas_estagnadas += 1
            motivo = "sem ganho"
        else:
            self.rodadas_estagnadas = 0
            motivo = "ganho"
        estagnou = self.rodadas_estagnadas >= cfg.rodadas_estagnadas_max
        return {"entropia": round(entropia, 4), "ganho": round(ganho, 4),
                "n_pool": n_pool, "motivo": motivo,
                "estagnadas": self.rodadas_estagnadas, "estagnou": estagnou}

    # --------------------------------------------------------- persistência --
    def salvar(self, cfg: Config) -> None:
        caminho = cfg.out_dir / "estado" / f"{hash_curto(self.subtopico)}.json"
        caminho.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2),
                           encoding="utf-8")

    @classmethod
    def carregar(cls, subtopico: str, topico: str, cfg: Config) -> "EstadoSubtopico":
        caminho = cfg.out_dir / "estado" / f"{hash_curto(subtopico)}.json"
        if caminho.exists():
            return cls(**json.loads(caminho.read_text(encoding="utf-8")))
        return cls(subtopico=subtopico, topico=topico)


def sugerir_limiar_entropia(historicos: dict[str, list[float]],
                            percentil: float = 75.0,
                            verbose: bool = True) -> float:
    """Calibra o limiar do passo 9 com os ganhos observados no piloto.

    Chutar o limiar a priori é o que se quer evitar. A ideia: rodar o piloto com
    o limiar quase zerado, deixar os subtópicos saturarem de fato, e ler onde
    fica a fronteira nos dados.

    Cada histórico é partido em duas fases — *crescimento*, até a entropia
    alcançar 90% do máximo que atingiu, e *platô*, dali em diante. O limiar sai
    do percentil dos ganhos do platô: é o teto do ruído de uma rodada que já não
    acrescenta cobertura. Fica travado em zero por baixo — um limiar negativo
    exigiria que a entropia *caísse* para declarar estagnação, e o critério
    nunca dispararia.

    Uma amostra que só viu a fase de crescimento (nenhum subtópico saturou) não
    calibra nada: o aviso aparece e o valor devolvido é conservador.
    """
    crescimento: list[float] = []
    plato: list[float] = []
    for h in historicos.values():
        if len(h) < 3:
            continue
        arr = np.asarray(h, dtype=float)
        ganhos = np.diff(arr)
        alvo = 0.9 * arr.max() if arr.max() > 0 else np.inf
        atingiu = np.argmax(arr >= alvo) if (arr >= alvo).any() else len(arr)
        crescimento.extend(ganhos[:max(atingiu, 0)])
        plato.extend(ganhos[max(atingiu, 0):])

    if not crescimento and not plato:
        if verbose:
            print("sem rodadas suficientes para calibrar — rode o piloto mais tempo")
        return 0.0

    base = plato if len(plato) >= 3 else (crescimento + plato)
    limiar = max(0.0, float(np.percentile(base, percentil)))

    if verbose:
        def desc(nome, v):
            if not len(v):
                return f"  {nome:<12} —"
            a = np.asarray(v)
            return (f"  {nome:<12} n={len(a):<4} mediana {np.median(a):+.4f} · "
                    f"p75 {np.percentile(a, 75):+.4f} · máx {a.max():+.4f}")
        print("ganhos de entropia por fase:")
        print(desc("crescimento", crescimento))
        print(desc("platô", plato))
        if len(plato) < 3:
            print("  AVISO: quase nenhum subtópico chegou ao platô — o limiar "
                  "abaixo veio de uma amostra que só viu crescimento.\n"
                  "         Suba `max_rodadas` e recalibre.")
        print(f"limiar sugerido (p{percentil:.0f} do platô, travado em 0): "
              f"{limiar:.4f}")
    return limiar



# ===========================================================================
# §9 repositório de questões (passo 7)
# ===========================================================================
# Uma questão aprovada é armazenada com: o embedding do par questão +
# alternativa correta, os documentos de origem, a nota de qualidade, a
# dificuldade e os scores de vício. JSONL para leitura humana; .npy paralelo
# para os embeddings.


class Repositorio:
    def __init__(self, cfg: Config, emb: Embedder):
        self.cfg = cfg
        self.emb = emb
        self.caminho = cfg.out_dir / "repositorio" / "questoes.jsonl"
        self.caminho_emb = cfg.out_dir / "repositorio" / "embeddings.npy"
        self.questoes: list[dict] = []
        self.embeddings: np.ndarray = np.zeros((0, emb.dim), dtype=np.float32)
        self._carregar()

    def _carregar(self) -> None:
        if self.caminho.exists():
            self.questoes = [json.loads(l) for l in
                             self.caminho.read_text(encoding="utf-8").splitlines()
                             if l.strip()]
        if self.caminho_emb.exists():
            self.embeddings = np.load(self.caminho_emb)
        if len(self.embeddings) != len(self.questoes):   # reconstrói se dessincronizou
            self.embeddings = (self.emb.encode([texto_para_embedding(q)
                                                for q in self.questoes])
                               if self.questoes else
                               np.zeros((0, self.emb.dim), dtype=np.float32))

    def __len__(self) -> int:
        return len(self.questoes)

    def adicionar(self, questao: dict, diagnostico: dict) -> dict:
        q = dict(questao)
        q["vicios"] = resumo_vicios(diagnostico)
        q["vicios_detalhe"] = {k: v["detalhe"] for k, v in diagnostico.items()}
        q.setdefault("refinada", False)
        q["armazenado_em"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        e = self.emb.encode([texto_para_embedding(q)])
        self.questoes.append(q)
        self.embeddings = np.vstack([self.embeddings, e])
        with open(self.caminho, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(q, ensure_ascii=False) + "\n")
        return q

    def salvar(self) -> None:
        np.save(self.caminho_emb, self.embeddings)
        self.emb.salvar_cache()

    def por_subtopico(self, subtopico: str) -> list[int]:
        return [i for i, q in enumerate(self.questoes)
                if q.get("subtopico") == subtopico]

    def embeddings_de(self, indices: Sequence[int]) -> np.ndarray:
        if not indices:
            return np.zeros((0, self.emb.dim), dtype=np.float32)
        return self.embeddings[np.asarray(indices, dtype=int)]

    def dataframe(self):
        import pandas as pd
        if not self.questoes:
            return pd.DataFrame()
        linhas = []
        for q in self.questoes:
            linhas.append({
                "id": q["id"], "topico": q.get("topico"),
                "subtopico": q.get("subtopico"), "faceta": q.get("faceta_titulo"),
                "rodada": q.get("rodada"), "nota": q.get("nota"),
                "dificuldade": q.get("difficulty"),
                "dificuldade_gerador": q.get("dificuldade_gerador"),
                "refinada": q.get("refinada", False),
                **{f"vicio_{k}": v for k, v in (q.get("vicios") or {}).items()},
                "stem": q["stem"],
            })
        return pd.DataFrame(linhas)


# ===========================================================================
# §10 pool de few-shot (passo 8)
# ===========================================================================
# No começo só há o banco seed (as vencedoras do formulário da fase 2). À
# medida que o pipeline aprova questões de nota alta, elas entram no sorteio e
# o seed perde peso — a dependência do seed cai sozinha, sem chaveamento
# manual. O sorteio é de qualquer tópico, de propósito: o few-shot calibra
# forma, não conteúdo.


class PoolFewShot:
    def __init__(self, seed: Sequence[dict], repo: Repositorio, cfg: Config):
        self.seed = list(seed)
        self.repo = repo
        self.cfg = cfg
        self.rng = random.Random(cfg.seed)

    def aprovadas_alto_score(self) -> list[dict]:
        return [q for q in self.repo.questoes
                if float(q.get("nota", 0)) >= self.cfg.nota_minima_fewshot]

    def peso_do_seed(self, n_aprovadas: int) -> float:
        """1,0 sem nenhuma aprovada; decai até 0,1 quando o banco próprio cresce."""
        return max(0.1, 1.0 - n_aprovadas / 40.0)

    def amostrar(self, k: int | None = None,
                 excluir_subtopico: str | None = None) -> list[dict]:
        k = k if k is not None else self.cfg.n_exemplos_fewshot
        aprovadas = self.aprovadas_alto_score()
        if excluir_subtopico:     # evita que o modelo copie o assunto da rodada
            aprovadas = [q for q in aprovadas
                         if q.get("subtopico") != excluir_subtopico]
        w_seed = self.peso_do_seed(len(aprovadas))
        itens = ([(q, w_seed) for q in self.seed] +
                 [(q, 1.0) for q in aprovadas])
        if not itens:
            return []
        escolhidos: list[dict] = []
        pool = list(itens)
        for _ in range(min(k, len(pool))):
            pesos = [w for _, w in pool]
            i = self.rng.choices(range(len(pool)), weights=pesos, k=1)[0]
            escolhidos.append(pool.pop(i)[0])
        return escolhidos

    def composicao(self) -> dict:
        n_apr = len(self.aprovadas_alto_score())
        return {"seed": len(self.seed), "aprovadas_alto_score": n_apr,
                "peso_do_seed": round(self.peso_do_seed(n_apr), 3)}


# ===========================================================================
# Rodada: passos 3 a 8 encadeados
# ===========================================================================


def executar_rodada(*, llm_forte, llm_judge, doc: dict, faceta: Faceta,
                    documento: str, pool: PoolFewShot, repo: Repositorio,
                    emb: Embedder, cfg: Config, rodada: int,
                    verbose: bool = True) -> dict:
    """Um ciclo dos passos 3–8 sobre um documento consolidado.

    Ordem: geração -> vícios/refinamento -> judge -> armazenamento. O judge
    roda por ÚLTIMO de propósito: seu papel é validar qualidade, dificuldade e
    correção técnica da versão FINAL da questão, não de um rascunho que ainda
    vai ser reescrito pelo refinador. Rodá-lo antes fazia o judge avaliar (e
    gastar chamada de LLM em) texto que o passo de vícios podia jogar fora ou
    reescrever logo em seguida — e a nota/dificuldade que ele atribuía ficava
    presa à versão pré-refinamento, não à que de fato ia pro repositório.

    Devolve o relatório da rodada (contagens por etapa e as questões guardadas).
    """
    log: dict[str, Any] = {"rodada": rodada, "doc_id": doc["doc_id"],
                           "faceta": faceta.titulo}

    # Um rng só pra rodada inteira (sorteio do exemplo externo + embaralhamento
    # da posição do gabarito, nessa ordem): reprodutível, sem precisar de dois
    # objetos Random com offsets ad-hoc.
    rng = random.Random(cfg.seed + rodada)

    # -- passo 3: geração ----------------------------------------------------
    exemplos = pool.amostrar(excluir_subtopico=faceta.subtopico)
    exemplo_externo = (amostrar_exemplo_externo(rng) if cfg.usar_exemplos_externos
                        else None)
    geradas = gerar_lote(llm_forte, doc, faceta, documento, exemplos, rodada, cfg,
                         exemplo_externo=exemplo_externo)
    log["geradas"] = len(geradas)
    log["fewshot"] = [q["id"] for q in exemplos]
    log["exemplo_externo"] = exemplo_externo["id"] if exemplo_externo else None

    # -- passos 5 e 6: vícios e refinamento (agora ANTES do judge) ----------
    # Corre sobre todas as questões geradas, não só sobre um subconjunto
    # pré-aprovado: métrica e refinamento preparam o texto que o judge vai
    # avaliar por último.
    candidatas: list[dict] = []
    diagnosticos: dict[str, dict] = {}
    descartadas = refinadas = 0
    for q in geradas:
        diag = pontuar_vicios(q, emb, cfg)
        if tem_vicio(diag):
            nova = refinar_questao(llm_forte, q, diag, documento, cfg)
            if nova is None:
                descartadas += 1
                continue
            diag2 = pontuar_vicios(nova, emb, cfg)
            if tem_vicio(diag2):        # reincidiu: descarta, não insiste
                descartadas += 1
                continue
            q, diag = nova, diag2
            refinadas += 1
        # -- pós-processamento: posição do gabarito -------------------------
        # Os VALORES dos vícios não mudam com a posição, mas o `detalhe` cita a
        # letra da correta; recalcular (embeddings já em cache) mantém o
        # registro coerente com o que vai pro judge e, se aprovado, pro
        # repositório.
        if cfg.embaralhar_alternativas:
            q = embaralhar_posicao(q, rng)
            diag = pontuar_vicios(q, emb, cfg)
        candidatas.append(q)
        diagnosticos[q["id"]] = diag
    log.update({"refinadas": refinadas, "descartadas_vicio": descartadas})

    # -- passo 4: judge, agora ao FIM da rodada ------------------------------
    # Único responsável por: qualidade, dificuldade e filtrar o que não está
    # tecnicamente correto — sobre a versão que já passou pelo scorer/refino.
    aprovadas = julgar_lote(llm_judge, candidatas, faceta.subtopico, cfg)
    log["aprovadas_judge"] = len(aprovadas)

    # -- passo 7: armazenamento ----------------------------------------------
    guardadas = [repo.adicionar(q, diagnosticos[q["id"]]) for q in aprovadas]
    log["guardadas"] = len(guardadas)
    log["ids_guardadas"] = [q["id"] for q in guardadas]

    if verbose:
        print(f"    rodada {rodada:>2} · {faceta.titulo[:34]:<34} "
              f"gerou {log['geradas']:>2} · refinou {refinadas} · "
              f"descartou {descartadas} · judge {log['aprovadas_judge']:>2} · "
              f"guardou {len(guardadas)}")
    return log


def registrar_log(cfg: Config, nome: str, payload: dict) -> None:
    caminho = cfg.out_dir / "logs" / f"{nome}.jsonl"
    with open(caminho, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, default=str) + "\n")


def calibrar_tolerancias(questoes: Sequence[dict], emb: "Embedder", cfg: Config,
                         percentil: float = 75.0, verbose: bool = True) -> dict:
    """Situa as tolerâncias do passo 6 contra um conjunto de referência.

    Cuidado com a interpretação, que não é a mesma do limiar de entropia. O
    banco seed são questões que especialistas julgaram melhores — mas o
    formulário da fase 2 perguntava qual estava "melhor elaborada", com
    justificativa de clareza, correção, alternativas e relevância. Vício de
    construção não estava na pauta, e passou: em 95% das 60 questões da fase 2 a
    alternativa correta é mais longa que a média dos distratores.

    Ou seja, o seed mostra onde o vício está HOJE, não onde ele deveria estar.
    Adotar o p90 do seed como tolerância institucionaliza o viés da fase 2 e o
    scorer não reprova nada. O uso correto é como referência de custo: para cada
    tolerância candidata, quantas questões do conjunto iriam para refinamento.
    Tolerância apertada demais manda todo lote para o refinador (caro, e o
    refinador vira o verdadeiro gerador); frouxa demais não filtra nada.
    """
    valores = {"similaridade": [], "comprimento": [], "distratores": [],
               "racionalizacao": []}
    for q in questoes:
        d = pontuar_vicios(q, emb, cfg)
        for k in valores:
            valores[k].append(d[k]["valor"])

    atual = {"similaridade": cfg.tol_similaridade,
             "comprimento": cfg.tol_comprimento,
             "distratores": cfg.tol_distratores,
             "racionalizacao": cfg.tol_racionalizacao}
    sugerido = {k: round(float(np.percentile(v, percentil)), 3)
                for k, v in valores.items() if v}

    if verbose:
        print(f"scorer de vícios sobre {len(questoes)} questões de referência\n")
        print(f"  {'vício':<14}{'mediana':>9}{'p75':>7}{'p90':>7}"
              f"{'  | tolerância atual':>22}{'reprova':>9}")
        for k, v in valores.items():
            a = np.array(v)
            taxa = float((a > atual[k]).mean())
            print(f"  {k:<14}{np.median(a):>9.2f}{np.percentile(a, 75):>7.2f}"
                  f"{np.percentile(a, 90):>7.2f}{atual[k]:>22.2f}{taxa:>8.0%}")
        print(f"\n  custo de cada tolerância candidata "
              f"(fração que iria para o refinador):")
        for k, v in valores.items():
            a = np.array(v)
            cand = [round(float(np.percentile(a, p)), 2) for p in (50, 75, 90)]
            taxas = [f"{c} -> {float((a > c).mean()):.0%}" for c in cand]
            print(f"    {k:<14} p50/p75/p90: {' · '.join(taxas)}")
        print(f"\n  sugestão (p{percentil:.0f}): {sugerido}")
        print("  Aperte em relação a isso se quiser que a fase 3 melhore o viés\n"
              "  da fase 2 em vez de reproduzi-lo — pagando mais refinamento.")
    return sugerido



def ids_pool_ausentes_do_repositorio(est: "EstadoSubtopico",
                                     repo: "Repositorio") -> list[str]:
    """Ids que o estado do subtópico marca como aprovados (`ids_pool`) mas que
    não existem mais em `repo.questoes`.

    Detecta o cenário do bug de ago/2026: o arquivo do repositório perdeu
    dados em disco (deleção externa, dessincronia de sync de pasta, etc.) sem
    que o estado (contador de rodada, `historico_entropia`) fosse tocado — a
    entropia calculada depois disso passou a rodar sobre um pool reiniciado do
    zero, e `EstadoSubtopico.registrar_rodada` tratou isso como "aquecendo"
    (primeira rodada / pool imaturo) em vez de acusar a inconsistência, porque
    nada cruzava `ids_pool` contra o repositório de fato.
    """
    ids_no_repo = {q["id"] for q in repo.questoes}
    return [i for i in est.ids_pool if i not in ids_no_repo]


def executar_subtopico(*, subtopico: str, topico: str, facetas: Sequence[Faceta],
                       plano: Sequence[dict], llm_leve, llm_forte, llm_judge,
                       pool: "PoolFewShot", repo: "Repositorio", emb: "Embedder",
                       codebook: "Codebook", cfg: Config,
                       max_rodadas: int = 60, verbose: bool = True,
                       ignorar_inconsistencia_pool: bool = False) -> "EstadoSubtopico":
    """Passos 3–9 em laço, até estagnar em todos os documentos do subtópico.

    Retomável: o estado é gravado a cada rodada, então reexecutar continua de
    onde parou em vez de recomeçar (e o cache do backend evita repagar as
    chamadas idênticas).
    """
    est = EstadoSubtopico.carregar(subtopico, topico, cfg)

    # -- checagem de consistência (ago/2026) --------------------------------
    # Antes de rodar mais uma rodada em cima de um estado retomado, confere se
    # o pool que o estado acha que existe bate com o que está de fato no
    # repositório. Ver `ids_pool_ausentes_do_repositorio`.
    faltando = ids_pool_ausentes_do_repositorio(est, repo)
    if faltando and not ignorar_inconsistencia_pool:
        raise RuntimeError(
            f"inconsistência no repositório do subtópico '{subtopico}': "
            f"{len(faltando)} de {len(est.ids_pool)} questões que o estado "
            f"(rodada {est.rodada}) marca como aprovadas não existem em "
            f"repo.questoes — o repositório parece ter perdido dados sem o "
            f"estado ser resetado (foi exatamente o que aconteceu em ago/2026, "
            f"ver os arquivos saida_fase3/repositorio/questoes.jsonl.bak_* e "
            f"fase3_pipeline.md na memória do projeto). Não sigo em frente "
            f"sozinho porque a entropia calculada sobre um pool incompleto "
            f"invalida o critério de parada. Reconcilie o repositório "
            f"(recuperando as questões faltantes de um backup ou commit git) "
            f"ou, se a perda for aceita de propósito, chame de novo com "
            f"ignorar_inconsistencia_pool=True.")
    elif faltando and verbose:
        print(f"  [aviso] {len(faltando)} questões do ids_pool de '{subtopico}' "
              f"não estão no repositório — seguindo mesmo assim "
              f"(ignorar_inconsistencia_pool=True).")

    fac_por_id = {f.id: f for f in facetas}
    if verbose:
        print(f"\n=== {subtopico} === ({len(plano)} documentos, "
              f"retomando na rodada {est.rodada + 1}, doc {est.doc_idx})")

    for _ in range(max_rodadas):
        if est.concluido:
            break
        if est.doc_idx >= len(plano):
            est.concluido = True
            break

        doc = plano[est.doc_idx]
        faceta = fac_por_id[doc["faceta_id"]]
        documento = consolidar_documento(llm_leve, doc, faceta, cfg)

        est.rodada += 1
        est.rodadas_no_documento += 1
        log = executar_rodada(llm_forte=llm_forte, llm_judge=llm_judge, doc=doc,
                              faceta=faceta, documento=documento, pool=pool,
                              repo=repo, emb=emb, cfg=cfg, rodada=est.rodada,
                              verbose=verbose)
        est.ids_pool.extend(log["ids_guardadas"])

        # -- passo 9: entropia do pool acumulado do SUBTÓPICO ----------------
        idxs = repo.por_subtopico(subtopico)
        rotulos = codebook.atribuir(repo.embeddings_de(idxs))
        H = entropia_normalizada(rotulos, codebook.k)
        info = est.registrar_rodada(H, len(idxs), cfg)
        log.update(info)
        registrar_log(cfg, "rodadas", {"subtopico": subtopico, **log})
        if verbose:
            print(f"       entropia {info['entropia']:.4f} "
                  f"(ganho {info['ganho']:+.4f}, {info['motivo']}) · "
                  f"pool {info['n_pool']} · estagnadas {info['estagnadas']}")

        limite_doc = est.rodadas_no_documento >= cfg.max_rodadas_por_documento
        if info["estagnou"] or limite_doc:
            motivo = "estagnou" if info["estagnou"] else "limite de rodadas"
            est.doc_idx += 1
            est.rodadas_estagnadas = 0
            est.rodadas_no_documento = 0
            if verbose:
                print(f"       -> {motivo}: avança para o documento "
                      f"{est.doc_idx}/{len(plano)}")
            if est.doc_idx >= len(plano):
                est.concluido = True
                if verbose:
                    print("       -> subtópico concluído")
        est.salvar(cfg)
        repo.salvar()
    return est


__all__ = [
    "Config", "Faceta", "Embedder", "Codebook", "EstadoSubtopico",
    "Repositorio", "PoolFewShot", "IndiceLexico",
    "normalizar", "tokenizar", "palavras_conteudo", "hash_curto",
    "extrair_facetas", "agrupar_por_subtopico",
    "varrer_corpus", "carregar_candidatos", "arquivos_do_corpus",
    "descrever_corpus",
    "montar_documentos_faceta", "plano_de_documentos",
    "consolidar_documento", "gerar_lote", "julgar_lote", "refinar_questao",
    "pontuar_vicios", "tem_vicio", "resumo_vicios", "PALAVRAS_ARMADILHA",
    "FRASES_RACIONALIZACAO",
    "embaralhar_posicao",
    "texto_para_embedding", "treinar_codebook", "codebook_do_subtopico",
    "entropia_normalizada",
    "sugerir_limiar_entropia", "calibrar_tolerancias",
    "executar_rodada", "executar_subtopico", "registrar_log",
    "ids_pool_ausentes_do_repositorio",
]
