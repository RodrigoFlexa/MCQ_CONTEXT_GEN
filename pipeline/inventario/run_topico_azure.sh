#!/usr/bin/env bash
# Notas técnicas de UM tópico na Azure (gpt-5-4-petrobras + embedding-3-large-global).
# Uso: bash pipeline/inventario/run_topico_azure.sh "<tópico ou parte do nome>" [--plan | --check-api | outros args]
# Ex.: bash pipeline/inventario/run_topico_azure.sh "Sistemas de Lastro" --plan
# Variáveis: INV_PYTHON, INV_MANIFEST, INV_OUTPUT (padrão: saida_<tópico>_v4_notas), INV_REUSE (saída anterior
#            para reaproveitar índice e vetores; a varredura só é reaproveitada se os assuntos baterem),
#            INV_WORKERS, INV_MAX_CHAMADAS.
set -euo pipefail
if [[ $# -lt 1 || "$1" == -* ]]; then
  echo 'Uso: run_topico_azure.sh "<tópico>" [args do run_inventario.py]' >&2
  exit 2
fi
TOPICO="$1"; shift
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
SLUG="$(printf '%s' "$TOPICO" | iconv -f utf-8 -t ascii//TRANSLIT 2>/dev/null | tr 'A-Z' 'a-z' | tr -cs 'a-z0-9' '_' | cut -c1-30 | sed 's/^_//;s/_$//')"
OUT="${INV_OUTPUT:-pipeline/inventario/saida_${SLUG:-topico}_v4_notas}"
REUSE="${INV_REUSE:-pipeline/inventario/saida_producao_v3_correcao_azure}"
EXTRA=()
if [[ -d "$REUSE" ]]; then EXTRA+=(--reaproveitar-de "$REUSE"); fi
echo "[run_topico_azure] tópico: $TOPICO | saída: $OUT"
"${INV_PYTHON:-python3}" -u pipeline/inventario/run_inventario.py \
  --corpus-manifest "${INV_MANIFEST:-dataset/domain_corpora/manifest.json}" \
  --topicos "$TOPICO" \
  --llm-provider azure --llm-model gpt-5-4-petrobras --effort medium \
  --embedder embedding-3-large-global --reranker none \
  --workers "${INV_WORKERS:-8}" --max-chamadas "${INV_MAX_CHAMADAS:-8000}" \
  --output "$OUT" ${EXTRA[@]+"${EXTRA[@]}"} "$@"
