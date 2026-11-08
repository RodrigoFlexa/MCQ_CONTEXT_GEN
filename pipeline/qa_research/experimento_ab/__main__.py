"""CLI do experimento A/B. Uso: python -m pipeline.qa_research.experimento_ab <comando> [opções]

  plano                 mostra braços, documentos e volume previsto (sem API)
  preparar              copia os documentos antigo/refinado para a pasta do experimento (sem API)
  calibrar              etapa 0: embeddings, pares rotulados, AUC, limiares e juiz da deduplicação
  gerar --braco A       etapas 1-2: geração v21 do braço (A, B, C ou D); C e D exigem A e B prontos
  avaliar --braco A     etapa 3: gap com/sem contexto (GPT-4.1 Nano/Mini/4.1) e sustentação dos gabaritos
  comparar              tabela 2x2 com efeitos e IC 95% (COMPARACAO.md)
  sustentacao --braco B etapa 4: checagem de sustentação + resposta mínima sobre as questões do braço (B_sust)
  saturar --braco D     rodadas extras por foco até saturar (D_sat), sobre a mesma 1ª rodada do braço
  v22 --braco B         gerador v22 (0 a 4 questões por foco, auditor por questão com o texto-fonte, sem refinador,
                        rodadas até saturar) com os documentos e o inventário de B (B_v22)
  v23 --braco B         gerador v23 (v22 + exemplos fixos de boas e ruins no prompt, resposta padrão declarada,
                        sem eliminação, mais decisão e procedimento, auditor v23) (B_v23)
  painel --braco B_v23  dificuldade empírica: sem contexto com GPT-5 mini e GPT-5.4, estratos por questão
                        (--avaliacao <pasta> para qualquer pasta de avaliação, como a do banco antigo)
  antigo                filtra o banco antigo: gabarito curto + auditor v23 nas 2156 sustentadas
  avaliar-antigo        benchmark_gap (mesmo protocolo do full_v1) sobre o banco antigo filtrado
  final                 dataset final único: reúne v23 (se pronto), v22 e antigo filtrado, exclui os defeitos da
                        revisão manual, deduplica entre fontes, avalia (com/sem contexto, sustentação, painel)
                        e escreve petroquest_final_v1/QUALIDADE.md
  v23-completo          gerador v23 nos 37 documentos fora do experimento (inventário da geração de outubro);
                        --docs-simultaneos limita os documentos gerados ao mesmo tempo (padrão 6)
  conceitos             geração de nomeação de termo técnico (a pergunta descreve, a resposta é o nome) nos 40 documentos
  variada               conceito, mecanismo e consequência nos 40 documentos, com exemplos de forma externos (visitas
                        1 a 3) e do dataset de múltipla escolha convertido (visita 4)
  tipos                 decisão, diagnóstico e procedimento, cada um numa geração separada nos 40 documentos, com
                        o esquema de exemplos da variada (--tipos escolhe quais; padrão os três, em sequência)
  rubrica               classifica o dataset final v2 em fácil/média/difícil pela rubrica do especialista e compara
                        com a dificuldade empírica -> petroquest_final_v2/rubrica/RUBRICA.md
  banco                 banco final: poda do dataset final v2 (regras R1-R4), revisão de unicidade das questões que
                        o GPT-5 erra (R5-R7, juiz GPT-5.4) e teto por tópico (R8) -> petroquest_banco_v1/BANCO.md;
                        --sem-revisao monta o banco provisório sem chamar a API
  splits                divide o banco final em treino/validação/teste (70/10/20, por grupo, estratificado)
  figuras               figuras do banco e do desempenho dos modelos (petroquest_banco_v1/figuras)
  avaliar-externos      juiz padrão sobre as respostas dos modelos Llama (vLLM na DL-28, respostas_externas/)
                        nas questões do banco final -> avaliacao_externos/QUALIDADE.md
  ablacao               ablação da geração (v2): 1000 vagas do banco, braços naive, documentos, regras,
                        documentos_regras, sem_retro, sem_externos e completo, mesma aceitação (auditor,
                        sustentação, dedup), taxa de aceite e vocabulário -> ablacao_geracao_v2/ABLACAO.md
  final-v2              dataset final v2: v23 + v23 completo + v22 + antigo + conceitos + variada, deduplicado, só gabaritos totalmente
                        sustentados, avaliado com resposta de até --palavras (20) por GPT-4.1 Nano/Mini/4.1,
                        GPT-5 nano/mini/5 e GPT-5.4 (referência), com e sem contexto -> petroquest_final_v2/QUALIDADE.md
  limite --palavras 20  experimento: as mesmas questões (amostra estratificada, --amostra 300) com resposta de até N
                        palavras, comparada às respostas de até 100 palavras (acurácia, F1, BLEU, ROUGE-L)

Braços derivados combinam sufixos: D_sat (saturação), D_sust (sustentação), D_sat_sust (os dois).

Repetir qualquer comando com a mesma pasta retoma de onde parou; nada já concluído é refeito.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from pipeline.qa_research.piloto_janela.core import atomic_json, blocos, read_json

from . import comum as C


def info_braco(nome: str) -> dict:
    partes = nome.split("_")
    base, sufixos = partes[0], partes[1:]
    if base not in C.BRACOS or any(s not in ("sat", "sust", "v22", "v23") for s in sufixos) or len(set(sufixos)) != len(sufixos):
        raise SystemExit(f"Braço inválido: {nome} (use A, B, C, D, <braço>_sat, <braço>_sust, <braço>_sat_sust ou "
                         "<braço>_v22 ou <braço>_v23)")
    sust = nome.endswith("_sust")
    return {**C.BRACOS[base], "base": base, "sustentacao": sust, "saturacao": "sat" in sufixos and not sust,
            "derivado": bool(sufixos)}


def _copiar_braco(origem: Path, destino: Path, manter_dedup: bool) -> None:
    """Cópia de um braço concluído: mesmas questões e caches (nenhuma chamada repetida)."""
    if not (origem / "geracao_concluida.json").exists():
        raise SystemExit(f"O braço {origem.name} ainda não concluiu a geração")
    if not destino.exists():
        ignorar = ["geracao_concluida.json", "aprovadas.jsonl", "finalizado.json", "resultado.json", "config.json",
                   "RELATORIO.md", "saturacao.json"] + ([] if manter_dedup else ["dedup_incremental"])
        shutil.copytree(origem, destino, ignore=shutil.ignore_patterns(*ignorar))


def _trava(exp: Path, nome: str):
    """Uma execução por braço. A trava fica fora da pasta do braço: apagar a pasta não libera a trava de um processo
    que ainda está rodando (foi assim que duas execuções se misturaram no B_v22)."""
    from contextlib import contextmanager

    from pipeline.inventario.locking import output_lock

    @contextmanager
    def cm():
        try:
            with output_lock(Path(exp) / ".travas" / nome):
                yield
        except RuntimeError as exc:
            if "Outra execução" not in str(exc):
                raise
            raise SystemExit(f"Outra execução está usando {nome}. Encerre-a antes (pkill -f experimento_ab) "
                             "ou espere terminar.") from exc
    return cm()


def _calibracao(exp: Path) -> Path:
    arq = exp / "calibracao" / "calibracao.json"
    if not arq.exists():
        raise SystemExit(f"Falta a calibração ({arq}). Rode antes: calibrar")
    return arq


def _gerador(exp: Path, nome: str, workers: int, dedup: str, saturacao: dict | None = None):
    from .geracao import GeracaoAB
    info = info_braco(nome)
    docs = C.docs_do_braco(exp, info["base"])
    if not (exp / "docs" / "manifesto.json").exists():
        raise SystemExit("Documentos não preparados. Rode antes: preparar")
    reusar = []
    if info["reusar"] and not info["derivado"]:
        origem = exp / "bracos" / info["reusar"]
        faltam = [i for i in C.ITENS if not (origem / "topicos" / i / "combinacoes.json").exists()]
        if faltam:
            raise SystemExit(f"O braço {nome} reaproveita o inventário de {info['reusar']} (mesmo documento), que ainda "
                             f"não terminou para {faltam}. Rode antes: gerar --braco {info['reusar']}")
        reusar = [origem]
    return GeracaoAB(exp / "bracos" / nome, C.ITENS, docs=docs, unidade=info["unidade"], braco=nome, reusar=reusar,
                     calibracao=_calibracao(exp) if dedup == "incremental" else None, dedup=dedup,
                     sustentacao=info["sustentacao"], saturacao=(saturacao or {}) if info["saturacao"] else None,
                     workers=workers)


def plano(exp: Path) -> None:
    print(f"Experimento: {C.relativo(exp)}")
    print(f"Documentos: {', '.join(C.ITENS)} (fonte {C.relativo(C.FONTE_DOCS)})")
    for b, info in C.BRACOS.items():
        docs = C.FONTE_DOCS / info["docs"]
        n = sum(len(blocos(i, docs)[1]) for i in C.ITENS)
        print(f"  {b}: documento {info['docs']:8s} | unidade {info['unidade']:8s} | {n} focos (1 chamada cada) | "
              f"até 25 compostas por documento | inventário " + (f"de {info['reusar']}" if info["reusar"] else "novo"))
    print("Etapa 0 (calibração): embeddings 3-small e 3-large das 2.818 questões; ~170 pares x (referência + 3 juízes).")
    print("Etapa 3 (avaliação): por braço, 2 condições x 3 modelos + juiz + 1 auditoria de sustentação por questão.")
    print("Sem chamadas de API neste comando.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.qa_research.experimento_ab", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("comando", choices=["plano", "preparar", "calibrar", "gerar", "avaliar", "comparar", "sustentacao",
                                        "saturar", "v22", "v23", "painel", "antigo", "avaliar-antigo", "final", "limite",
                                        "v23-completo", "conceitos", "variada", "tipos", "rubrica", "banco", "splits", "figuras",
                                        "final-v2", "ablacao", "avaliar-externos"])
    ap.add_argument("--experimento", type=Path, default=C.EXPERIMENTO)
    ap.add_argument("--braco")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--judge-workers", type=int, default=2)
    ap.add_argument("--dedup", choices=["incremental", "llm"], default="incremental")
    ap.add_argument("--por-faixa", type=int, default=8, help="calibração: pares sorteados por faixa de cosseno e modelo")
    ap.add_argument("--recalcular", action="store_true", help="calibração: só recalcula (usa rotulos_humanos.csv)")
    ap.add_argument("--mini-deployment", default="gpt-4-1-mini-petrobras")
    ap.add_argument("--max-rodadas", type=int, default=5, help="saturação: visitas máximas por foco (inclui a 1ª)")
    ap.add_argument("--paciencia", type=int, default=1, help="saturação: rodadas seguidas sem conhecimento novo para fechar")
    ap.add_argument("--onda", type=int, default=4, help="v22/v23: focos gerados ao mesmo tempo em cada documento")
    ap.add_argument("--tipos", default="decisao,diagnostico,procedimento",
                    help="tipos: quais gerações por tipo rodar, separados por vírgula")
    ap.add_argument("--sem-revisao", action="store_true", help="banco: sem a revisão de unicidade (provisório)")
    ap.add_argument("--teto-topico", type=int, default=150, help="banco: máximo de questões por tópico")
    ap.add_argument("--bracos", default="naive,documentos,regras,documentos_regras,sem_retro,sem_externos,completo",
                    help="ablacao: braços, separados por vírgula")
    ap.add_argument("--vagas", type=int, default=1000, help="ablacao: questões pedidas por braço")
    ap.add_argument("--so-relatorio", action="store_true",
                    help="final-v2: só refaz o QUALIDADE.md com o que já foi avaliado, sem montar nem avaliar")
    ap.add_argument("--docs-simultaneos", type=int, default=6, help="v23-completo: documentos gerados ao mesmo tempo")
    ap.add_argument("--palavras", type=int, default=20, help="limite: palavras máximas na resposta dos modelos")
    ap.add_argument("--amostra", type=int, default=300, help="limite: questões na amostra estratificada")
    ap.add_argument("--avaliacao", type=Path, help="painel: pasta de avaliação (padrão: avaliacao/<braço>)")
    a = ap.parse_args(argv)
    exp = a.experimento if a.experimento.is_absolute() else C.ROOT / a.experimento

    if a.comando == "plano":
        plano(exp)
        return 0
    if a.comando == "preparar":
        m = C.preparar_documentos(exp)
        for k, v in m["documentos"].items():
            print(f"  {k}: {v['blocos']} blocos, {v['capitulos']} capítulos, {v['palavras']} palavras")
        return 0
    if a.comando == "calibrar":
        from .calibracao import Calibracao
        falhas = Calibracao(exp / "calibracao", por_faixa=a.por_faixa, workers=a.workers).run(recalcular=a.recalcular)
        print(f"Resumo: {C.relativo(exp / 'calibracao' / 'CALIBRACAO.md')}")
        if falhas:
            print(f"{falhas} rótulos falharam; repita o comando para tentar só eles.")
        return 2 if falhas else 0
    if a.comando == "comparar":
        from .metricas import comparar
        emb = media = None
        cal = exp / "calibracao" / "calibracao.json"
        if cal.exists():
            import numpy as np
            c = read_json(cal)
            emb = C.embedder(c["embedding"], exp / "calibracao")
            media = np.asarray(read_json(exp / "calibracao" / c["media"]), dtype=float)
        comparar(exp, embedder=emb, media_vec=media)
        print(f"Tabela: {C.relativo(exp / 'COMPARACAO.md')}")
        return 0
    if a.comando == "antigo":
        from .antigo import SAIDA, FiltroAntigo
        with _trava(exp, "antigo"):
            falhas = FiltroAntigo(workers=a.workers).run()
        print(f"[antigo] {'filtro concluído' if not falhas else f'{falhas} questões falharam; repita o comando'}: "
              f"{C.relativo(SAIDA / 'RELATORIO.md')}")
        return 2 if falhas else 0
    if a.comando == "avaliar-antigo":
        from .antigo import AVALIACAO, avaliar
        with _trava(exp, "avaliacao_antigo"):
            st = avaliar(workers=a.workers, judge_workers=a.judge_workers, mini=a.mini_deployment)
        print(f"[antigo] avaliação {'concluída' if st == 0 else 'incompleta; repita o mesmo comando'}: "
              f"{C.relativo(AVALIACAO)}")
        return st
    if a.comando == "v23-completo":
        from .completo import SAIDA_GERACAO, gerador
        with _trava(exp, "v23_completo"):
            try:
                g = gerador(exp, workers=a.workers, onda=a.onda, docs_simultaneos=a.docs_simultaneos,
                            saturacao={"max_rodadas": a.max_rodadas, "paciencia": a.paciencia})
            except ValueError as exc:
                raise SystemExit(f"[v23-completo] {exc}") from exc
            falhas = g.run()
        if falhas:
            print(f"[v23-completo] {falhas} unidades falharam (isoladas; o resto está salvo). Repita o mesmo comando.")
            return 2
        print(f"[v23-completo] geração concluída: {C.relativo(SAIDA_GERACAO / 'RELATORIO.md')}")
        return 0
    if a.comando == "conceitos":
        from .completo import SAIDA_CONCEITOS, gerador_conceitos
        with _trava(exp, "conceitos"):
            try:
                g = gerador_conceitos(exp, workers=a.workers, onda=a.onda, docs_simultaneos=a.docs_simultaneos,
                                      saturacao={"max_rodadas": a.max_rodadas, "paciencia": a.paciencia})
            except ValueError as exc:
                raise SystemExit(f"[conceitos] {exc}") from exc
            falhas = g.run()
        if falhas:
            print(f"[conceitos] {falhas} unidades falharam (isoladas; o resto está salvo). Repita o mesmo comando.")
            return 2
        print(f"[conceitos] geração concluída: {C.relativo(SAIDA_CONCEITOS / 'RELATORIO.md')}")
        return 0
    if a.comando == "variada":
        from .completo import SAIDA_VARIADA, gerador_variada
        with _trava(exp, "variada"):
            try:
                g = gerador_variada(exp, workers=a.workers, onda=a.onda, docs_simultaneos=a.docs_simultaneos)
            except ValueError as exc:
                raise SystemExit(f"[variada] {exc}") from exc
            falhas = g.run()
        if falhas:
            print(f"[variada] {falhas} unidades falharam (isoladas; o resto está salvo). Repita o mesmo comando.")
            return 2
        print(f"[variada] geração concluída: {C.relativo(SAIDA_VARIADA / 'RELATORIO.md')}")
        return 0
    if a.comando == "tipos":
        from .completo import SAIDA_TIPO, gerador_tipo
        tipos = [t.strip() for t in a.tipos.split(",") if t.strip()]
        for t in tipos:
            with _trava(exp, f"tipo_{t}"):
                try:
                    g = gerador_tipo(exp, t, workers=a.workers, onda=a.onda, docs_simultaneos=a.docs_simultaneos)
                except ValueError as exc:
                    raise SystemExit(f"[tipos] {exc}") from exc
                falhas = g.run()
            if falhas:
                print(f"[tipos] {t}: {falhas} unidades falharam (isoladas; o resto está salvo). Repita o mesmo comando.")
                return 2
            print(f"[tipos] {t} concluído: {C.relativo(Path(str(SAIDA_TIPO).format(t)) / 'RELATORIO.md')}")
        return 0
    if a.comando == "splits":
        from .banco import SAIDA as SAIDA_BANCO
        from .splits import dividir
        r = dividir(SAIDA_BANCO)
        print(f"[splits] {r['tamanho']}: {C.relativo(SAIDA_BANCO / 'splits' / 'SPLITS.md')}")
        return 0
    if a.comando == "figuras":
        from .figuras import SAIDA as SAIDA_FIG, gerar
        gerar()
        print(f"[figuras] {C.relativo(SAIDA_FIG)}")
        return 0
    if a.comando == "avaliar-externos":
        from .externos import SAIDA as SAIDA_EXT, executar as externos
        with _trava(exp, "externos"):
            try:
                st = externos(workers=a.workers, judge_workers=a.judge_workers)
            except ValueError as exc:
                raise SystemExit(f"[externos] {exc}") from exc
        print(f"[externos] {'concluída' if st == 0 else 'incompleta; repita o mesmo comando'}: "
              f"{C.relativo(SAIDA_EXT / 'QUALIDADE.md')}")
        return st
    if a.comando == "ablacao":
        from .ablacao import SAIDA as SAIDA_ABL, Ablacao
        with _trava(exp, "ablacao"):
            try:
                abl = Ablacao(n=a.vagas, bracos=[b for b in a.bracos.split(",") if b], workers=a.workers, exp=exp)
                if a.so_relatorio:          # só refaz o ABLACAO.md com o que já foi gravado
                    abl.relatorio()
                    st = 0
                else:
                    st = abl.executar()
            except ValueError as exc:
                raise SystemExit(f"[ablacao] {exc}") from exc
        print(f"[ablacao] {'concluída' if st == 0 else 'incompleta; repita o mesmo comando'}: "
              f"{C.relativo(SAIDA_ABL / 'ABLACAO.md')}")
        return st
    if a.comando == "banco":
        from .banco import Banco, SAIDA as SAIDA_BANCO
        with _trava(exp, "banco"):
            try:
                st = Banco(workers=a.workers, teto=a.teto_topico, exp=exp).executar(revisar=not a.sem_revisao)
            except ValueError as exc:
                raise SystemExit(f"[banco] {exc}") from exc
        print(f"[banco] {'concluído' if st == 0 else 'incompleto; repita o mesmo comando'}: "
              f"{C.relativo(SAIDA_BANCO / 'BANCO.md')}")
        return st
    if a.comando == "rubrica":
        from .rubrica import executar as rubrica
        with _trava(exp, "rubrica"):
            try:
                st = rubrica(workers=a.workers)
            except ValueError as exc:
                raise SystemExit(f"[rubrica] {exc}") from exc
        print("[rubrica] " + ("concluída" if st == 0 else "incompleta; repita o mesmo comando") +
              ": pipeline/qa_research/relatorios/petroquest_final_v2/rubrica/RUBRICA.md")
        return st
    if a.comando == "final-v2":
        from .completo import SAIDA as SAIDA2, DatasetCompleto, executar as final2
        if a.so_relatorio:
            r = DatasetCompleto(exp=exp, limite=a.palavras).relatorio()
            print(f"[final-v2] relatório de {r['n']} questões: {C.relativo(SAIDA2 / 'QUALIDADE.md')}")
            return 0
        with _trava(exp, "final_v2"):
            try:
                st = final2(exp, workers=a.workers, judge_workers=a.judge_workers, limite=a.palavras)
            except ValueError as exc:
                raise SystemExit(f"[final-v2] {exc}") from exc
        print(f"[final-v2] {'concluído' if st == 0 else 'incompleto; repita o mesmo comando'}: "
              f"{C.relativo(SAIDA2 / 'QUALIDADE.md')}")
        return st
    if a.comando == "limite":
        from .limite import executar as limite
        with _trava(exp, f"limite_{a.palavras}"):
            try:
                st = limite(limite=a.palavras, n=a.amostra, workers=a.workers, judge_workers=a.judge_workers)
            except ValueError as exc:
                raise SystemExit(f"[limite] {exc}") from exc
        print(f"[limite] {'concluído' if st == 0 else 'incompleto; repita o mesmo comando'}")
        return st
    if a.comando == "final":
        from .final import SAIDA, executar as final
        with _trava(exp, "final"):
            try:
                st = final(exp, workers=a.workers, judge_workers=a.judge_workers, mini=a.mini_deployment)
            except ValueError as exc:
                raise SystemExit(f"[final] {exc}") from exc
        print(f"[final] {'concluído' if st == 0 else 'incompleto; repita o mesmo comando'}: "
              f"{C.relativo(SAIDA / 'QUALIDADE.md')}")
        return st
    if a.comando == "painel" and a.avaliacao:
        a.braco = a.braco or a.avaliacao.name
    if not a.braco:
        raise SystemExit("Informe --braco")
    sat = {"max_rodadas": a.max_rodadas, "paciencia": a.paciencia}
    if a.comando == "gerar":
        if info_braco(a.braco)["derivado"]:
            raise SystemExit("Braços derivados são criados com os comandos saturar ou sustentacao")
        with _trava(exp, a.braco):
            g = _gerador(exp, a.braco, a.workers, a.dedup)
            falhas = g.run()
        if falhas:
            print(f"[{a.braco}] {falhas} unidades falharam (isoladas; as demais foram salvas). Repita o mesmo comando "
                  "para tentar só elas.")
            return 2
        print(f"[{a.braco}] geração concluída: {C.relativo(exp / 'bracos' / a.braco / 'RELATORIO.md')}")
        return 0
    if a.comando in ("v22", "v23"):
        from .v22 import GeracaoV22
        from .v23 import GeracaoV23
        classe, v = (GeracaoV22, "v22") if a.comando == "v22" else (GeracaoV23, "v23")
        info = info_braco(a.braco)
        if info["derivado"]:
            raise SystemExit(f"Informe o braço de origem (A, B, C ou D); o {v} cria <braço>_{v}")
        if info["unidade"] != "janela":
            raise SystemExit(f"O {v} usa a janela de 3 blocos (braços A ou B)")
        origem, nome = exp / "bracos" / a.braco, f"{a.braco}_{v}"
        faltam = [i for i in C.ITENS if not (origem / "topicos" / i / "combinacoes.json").exists()]
        if faltam:
            raise SystemExit(f"O {v} reaproveita o inventário de {a.braco}, incompleto para {faltam}")
        with _trava(exp, nome):
            g = classe(exp / "bracos" / nome, C.ITENS, docs=C.docs_do_braco(exp, a.braco), braco=nome, reusar=[origem],
                       calibracao=_calibracao(exp), saturacao=sat, onda=a.onda, workers=a.workers)
            falhas = g.run()
        if falhas:
            print(f"[{nome}] {falhas} unidades falharam (isoladas; o resto está salvo). Repita o mesmo comando.")
            return 2
        print(f"[{nome}] geração concluída: {C.relativo(exp / 'bracos' / nome / 'RELATORIO.md')}")
        return 0
    if a.comando == "painel":
        from .painel import executar as painel
        aval = a.avaliacao or exp / "avaliacao" / a.braco
        aval = aval if aval.is_absolute() else C.ROOT / aval
        with _trava(exp, "painel_" + aval.name):
            st = painel(aval, workers=a.workers, judge_workers=a.judge_workers)
        print(f"[painel] {'concluído' if st == 0 else 'incompleto; repita o mesmo comando'}: "
              f"{C.relativo(aval / 'painel' / 'resumo.json')}")
        return st
    if a.comando in ("sustentacao", "saturar"):
        sufixo = "_sust" if a.comando == "sustentacao" else "_sat"
        origem, nome = exp / "bracos" / a.braco, a.braco + sufixo
        destino = exp / "bracos" / nome
        info_braco(nome)
        # sustentação refaz as decisões de deduplicação (o gate remove questões antes dela); saturação as mantém,
        # porque as rodadas novas são comparadas com o banco da 1ª rodada
        _copiar_braco(origem, destino, manter_dedup=a.comando == "saturar")
        with _trava(exp, nome):
            g = _gerador(exp, nome, a.workers, a.dedup, saturacao=sat)
            g.config()
            cfg = read_json(destino / "config.json")
            atomic_json(destino / "config.json", {**cfg, "origem": C.relativo(origem)})
            falhas = g.run()
        if falhas:
            print(f"[{nome}] {falhas} unidades falharam; repita o mesmo comando.")
            return 2
        print(f"[{nome}] concluído: {C.relativo(destino / 'resultado.json')}. Avalie com: avaliar --braco {nome}")
        return 0
    if a.comando == "avaliar":
        from .avaliacao import executar
        destino = exp / "avaliacao" / a.braco
        origem = exp / "avaliacao" / a.braco.rsplit("_", 1)[0]
        if info_braco(a.braco)["derivado"] and not destino.exists() and (origem / ".local").exists():
            # braço derivado: reaproveita o cache de chamadas da avaliação de origem (mesma pergunta e mesmo contexto
            # = mesma chamada; respostas e auditorias das questões em comum não são pagas de novo)
            shutil.copytree(origem / ".local", destino / ".local")
        with _trava(exp, "avaliacao_" + a.braco):
            st = executar(exp / "bracos" / a.braco, exp / "avaliacao" / a.braco, workers=a.workers,
                          judge_workers=a.judge_workers, mini=a.mini_deployment)
        print(f"[{a.braco}] avaliação {'concluída' if st == 0 else 'incompleta; repita o mesmo comando'}")
        return st
    return 1


if __name__ == "__main__":
    sys.exit(main())
