#!/usr/bin/env bash
# Experimento A/B da geração de questões (pipeline/qa_research/experimento_ab/README.md).
#   2x2: documento (antigo x refinado) x unidade de contexto (janela de 3 blocos x capítulo), gerador v21,
#   deduplicação incremental calibrada, avaliação com/sem contexto (GPT-4.1 Nano/Mini/4.1) e sustentação.
#
# Uso: bash pipeline/qa_research/rodar_experimento_ab.sh [etapa] [--experimento <pasta>] [--workers N]
#   tudo (padrão)        preparar -> calibracao -> geracao -> avaliacao -> comparacao
#   plano                mostra o que será feito, sem chamadas de API
#   calibracao | geracao | avaliacao | comparacao   só a etapa indicada
#   sustentacao <BRAÇO>  etapa 4 no braço vencedor (ex.: B): checagem de sustentação, avaliação e comparação
#   saturacao <BRAÇO>    rodadas extras por foco até saturar (ex.: D -> D_sat), avaliação e comparação
#   v22 <BRAÇO>          gerador v22 com os documentos e o inventário do braço (ex.: B -> B_v22), avaliação e
#                        comparação; opções --max-rodadas (padrão 5), --paciencia (1) e --onda (4)
#   v23 <BRAÇO>          gerador v23 (exemplos fixos de boas e ruins, resposta padrão, sem eliminação, mais decisão
#                        e procedimento, auditor v23) -> <BRAÇO>_v23; avaliação; painel de dificuldade (GPT-5 mini e
#                        GPT-5.4 sem contexto) em <BRAÇO>, <BRAÇO>_v22 e <BRAÇO>_v23; comparação
#   painel <BRAÇO>       só o painel de dificuldade de um braço já avaliado, e a comparação
#   antigo               banco antigo: gabarito curto + auditor v23 nas 2156 sustentadas, benchmark_gap e painel
# Uma trava impede duas execuções no mesmo braço; antes de repetir após interromper, encerre o processo antigo
# (pkill -f experimento_ab).
# Repetir o mesmo comando retoma de onde parou; nada concluído é refeito. Falhas isoladas são tentadas de novo
# automaticamente (até 3 vezes por etapa).
set -uo pipefail
export PYTHONUTF8=1
qa_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd -- "$qa_root"
py="${DOCUMENT_PYTHON:-$qa_root/.venv-documento/bin/python}"
if [[ ! -x "$py" ]]; then
    py="$qa_root/venv/bin/python"
    if [[ ! -x "$py" ]]; then py="$(command -v python3)"; fi
fi

etapa="tudo"
if [[ $# -gt 0 && "$1" != --* ]]; then etapa="$1"; shift; fi
braco_sust=""
if [[ "$etapa" == "sustentacao" || "$etapa" == "saturacao" || "$etapa" == "v22" || "$etapa" == "v23" || "$etapa" == "painel" ]]; then
    braco_sust="${1:-}"
    if [[ -z "$braco_sust" || "$braco_sust" == --* ]]; then echo "Uso: ... $etapa <braço, ex.: B ou D_sat>"; exit 1; fi
    shift
fi
exp="pipeline/qa_research/relatorios/experimento_ab_v1"
comuns=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --experimento) exp="$2"; shift 2 ;;
        --workers) comuns+=(--workers "$2"); shift 2 ;;
        --max-rodadas) comuns+=(--max-rodadas "$2"); shift 2 ;;
        --paciencia) comuns+=(--paciencia "$2"); shift 2 ;;
        --onda) comuns+=(--onda "$2"); shift 2 ;;
        *) echo "Opção desconhecida: $1"; exit 1 ;;
    esac
done
comuns+=(--experimento "$exp")

rodar() {   # rodar <rótulo> <comando python...>; status 2 = falhas isoladas -> tenta de novo
    local rotulo="$1"; shift
    local st=0
    for t in 1 2 3; do
        echo "[$(date +%H:%M:%S)] $rotulo (tentativa $t)"
        "$py" -u -m pipeline.qa_research.experimento_ab "$@" "${comuns[@]}"
        st=$?
        [[ $st -eq 0 ]] && return 0
        [[ $st -eq 2 ]] || return $st
        sleep 20
    done
    return $st
}

duas_filas() {   # duas_filas <comando> : A->C e B->D em paralelo (C e D reaproveitam o inventário de A e B)
    local cmd="$1"
    ( rodar "$cmd A" "$cmd" --braco A && rodar "$cmd C" "$cmd" --braco C ) 2>&1 | sed -u 's/^/[A,C] /' &
    local p1=$!
    ( rodar "$cmd B" "$cmd" --braco B && rodar "$cmd D" "$cmd" --braco D ) 2>&1 | sed -u 's/^/[B,D] /' &
    local p2=$!
    local s1=0 s2=0
    wait $p1 || s1=$?
    wait $p2 || s2=$?
    [[ $s1 -eq 0 && $s2 -eq 0 ]]
}

fim_erro() {
    echo
    echo "Etapa '$1' não terminou. As unidades concluídas estão salvas; repita o mesmo comando para continuar:"
    echo "  bash pipeline/qa_research/rodar_experimento_ab.sh $etapa ${braco_sust} --experimento $exp"
    echo "Falhas registradas: $exp/bracos/*/falhas/ e $exp/calibracao/falhas/"
    exit 2
}

set -o pipefail
case "$etapa" in
    plano)
        "$py" -m pipeline.qa_research.experimento_ab plano "${comuns[@]}"; exit $? ;;
    tudo|calibracao|geracao|avaliacao|comparacao|sustentacao|saturacao|v22|v23|painel|antigo) ;;
    *) echo "Etapa desconhecida: $etapa"; exit 1 ;;
esac

if [[ "$etapa" == "tudo" || "$etapa" == "calibracao" ]]; then
    rodar "preparar documentos" preparar || fim_erro preparar
    rodar "etapa 0: calibração da deduplicação" calibrar || fim_erro calibracao
fi
if [[ "$etapa" == "tudo" || "$etapa" == "geracao" ]]; then
    rodar "preparar documentos" preparar || fim_erro preparar
    echo "== Geração dos braços A..D (duas filas em paralelo)"
    duas_filas gerar || fim_erro geracao
fi
if [[ "$etapa" == "tudo" || "$etapa" == "avaliacao" ]]; then
    echo "== Avaliação dos braços A..D (duas filas em paralelo)"
    duas_filas avaliar || fim_erro avaliacao
fi
if [[ "$etapa" == "sustentacao" ]]; then
    rodar "etapa 4: sustentação em $braco_sust" sustentacao --braco "$braco_sust" || fim_erro sustentacao
    rodar "avaliar ${braco_sust}_sust" avaliar --braco "${braco_sust}_sust" || fim_erro sustentacao
fi
if [[ "$etapa" == "saturacao" ]]; then
    rodar "saturação por foco em $braco_sust" saturar --braco "$braco_sust" || fim_erro saturacao
    rodar "avaliar ${braco_sust}_sat" avaliar --braco "${braco_sust}_sat" || fim_erro saturacao
fi
if [[ "$etapa" == "v22" ]]; then
    rodar "gerador v22 a partir de $braco_sust" v22 --braco "$braco_sust" || fim_erro v22
    rodar "avaliar ${braco_sust}_v22" avaliar --braco "${braco_sust}_v22" || fim_erro v22
fi
if [[ "$etapa" == "v23" ]]; then
    rodar "gerador v23 a partir de $braco_sust" v23 --braco "$braco_sust" || fim_erro v23
    rodar "avaliar ${braco_sust}_v23" avaliar --braco "${braco_sust}_v23" || fim_erro v23
    for b in "$braco_sust" "${braco_sust}_v22" "${braco_sust}_v23"; do
        if [[ -f "$exp/avaliacao/$b/rodada_concluida.json" ]]; then
            rodar "painel de dificuldade em $b" painel --braco "$b" || fim_erro v23
        fi
    done
fi
if [[ "$etapa" == "painel" ]]; then
    rodar "painel de dificuldade em $braco_sust" painel --braco "$braco_sust" || fim_erro painel
fi
if [[ "$etapa" == "antigo" ]]; then
    # 2 chamadas por questão (2156 questões): 16 em paralelo por padrão; um --workers explícito prevalece
    rodar "banco antigo: gabarito curto + auditor v23" antigo --workers 16 || fim_erro antigo
    rodar "banco antigo: benchmark_gap" avaliar-antigo || fim_erro antigo
    rodar "banco antigo: painel de dificuldade" painel --avaliacao pipeline/qa_research/relatorios/benchmark_gap_antigo_filtrado_v1 || fim_erro antigo
fi
if [[ "$etapa" == "tudo" || "$etapa" == "comparacao" || "$etapa" == "sustentacao" || "$etapa" == "saturacao" || "$etapa" == "v22" || "$etapa" == "v23" || "$etapa" == "painel" ]]; then
    rodar "comparação" comparar || fim_erro comparacao
fi

echo
echo "O código acabou de rodar no terminal :)"
echo
echo "Resultados:"
echo "  cat $exp/COMPARACAO.md"
echo "  cat $exp/calibracao/CALIBRACAO.md"
echo "Enviar ao GitHub (no servidor):"
if [[ "$etapa" == "antigo" ]]; then
    echo "  bash pipeline/qa_research/enviar_resultados.sh pipeline/qa_research/relatorios/banco_antigo_filtrado_v1 \"Resultados: banco antigo filtrado\""
    echo "  bash pipeline/qa_research/enviar_resultados.sh pipeline/qa_research/relatorios/benchmark_gap_antigo_filtrado_v1 \"Resultados: avaliação do banco antigo filtrado\""
else
    echo "  bash pipeline/qa_research/enviar_resultados.sh $exp \"Resultados: experimento A/B ($etapa)\""
fi
echo "Na sua máquina:"
echo "  git pull --ff-only origin codex/qa-evidencias-verificadas"
