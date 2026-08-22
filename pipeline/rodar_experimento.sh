#!/usr/bin/env bash
# Executa as duas condições do experimento em sequência, na mesma GPU.
#
#   ./rodar_experimento.sh          # GPU 3 (padrão dos scripts)
#   ./rodar_experimento.sh 0        # GPU 0
#
# A ordem importa: o pipeline context-grounded roda primeiro porque o
# instruction-only lê dataset_mcq_petroles.jsonl para imprimir a tabela
# comparativa ao final. Se o primeiro falhar, o segundo não roda — um
# baseline sem a condição experimental para comparar não serve de nada.

set -euo pipefail
cd "$(dirname "$0")"

export CUDA_VISIBLE_DEVICES="${1:-3}"
export PYTHONUNBUFFERED=1          # log em tempo real, não em blocos

LOG_DIR="mcq_output/logs"
mkdir -p "$LOG_DIR"
STAMP="$(date +%Y%m%d_%H%M%S)"

run() {
    local nome="$1" script="$2"
    local log="$LOG_DIR/${STAMP}_${nome}.log"
    echo
    echo "=============================================================="
    echo ">>> $nome  |  GPU $CUDA_VISIBLE_DEVICES  |  $(date +%H:%M:%S)"
    echo ">>> log: $log"
    echo "=============================================================="
    local t0=$SECONDS
    # tee preserva o log mesmo com falha; PIPESTATUS traz o código do python
    python geracao_mcq_"${script}".py 2>&1 | tee "$log"
    local rc=${PIPESTATUS[0]}
    local dt=$(( SECONDS - t0 ))
    if [ "$rc" -ne 0 ]; then
        echo ">>> $nome FALHOU (código $rc) após $((dt/60))min — veja $log" >&2
        return "$rc"
    fi
    echo ">>> $nome concluído em $((dt/60))min $((dt%60))s"
}

t_inicio=$SECONDS
run "context-grounded" petroles
run "instruction-only" instrucao

echo
echo "=============================================================="
echo ">>> Experimento completo em $(( (SECONDS - t_inicio) / 60 ))min"
echo "=============================================================="
ls -la mcq_output/dataset_mcq_*.jsonl mcq_output/dataset_mcq_*.csv
