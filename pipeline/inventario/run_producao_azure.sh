#!/usr/bin/env bash
# Notas técnicas de Produção e Processo (12 subtópicos) na Azure.
# Ex.: bash pipeline/inventario/run_producao_azure.sh --plan | --check-api | (sem argumentos = rodada completa)
# Variáveis: INV_PYTHON, INV_MANIFEST, INV_OUTPUT, INV_REUSE (saída anterior p/ reaproveitar índice/vetores),
#            INV_WORKERS, INV_MAX_CHAMADAS.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
REUSE="${INV_REUSE:-pipeline/inventario/saida_producao_v3_correcao_azure}"
EXTRA=()
if [[ -d "$REUSE" ]]; then EXTRA+=(--reaproveitar-de "$REUSE"); fi
"${INV_PYTHON:-python3}" -u pipeline/inventario/run_inventario.py \
  --corpus-manifest "${INV_MANIFEST:-dataset/domain_corpora/manifest.json}" \
  --topicos 'Produção e Processo (Medição Fiscal e Sistema de Alívio)' \
  --llm-provider azure --llm-model gpt-5-4-petrobras --effort medium \
  --embedder embedding-3-large-global --reranker none \
  --workers "${INV_WORKERS:-8}" --max-chamadas "${INV_MAX_CHAMADAS:-30000}" \
  --output "${INV_OUTPUT:-pipeline/inventario/saida_producao_v4_notas}" ${EXTRA[@]+"${EXTRA[@]}"} "$@"
