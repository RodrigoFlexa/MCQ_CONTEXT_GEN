#!/usr/bin/env bash
# Completa a primeira rodada de cinco tópicos, acrescentando quatro ao Lastro já produzido.
# Uma execução, uma varredura lexical, um diretório de saída com quatro documentos por tópico.
# Uso: bash pipeline/inventario/run_mais_4_topicos_azure.sh [--plan | --check-api | outros args]
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
REUSE="${INV_REUSE:-pipeline/inventario/saida_sistemas_de_lastro_v4_notas}"
EXTRA=()
if [[ -d "$REUSE" ]]; then EXTRA+=(--reaproveitar-de "$REUSE"); fi
"${INV_PYTHON:-python3}" -u pipeline/inventario/run_inventario.py \
  --corpus-manifest "${INV_MANIFEST:-dataset/domain_corpora/manifest.json}" \
  --topicos 'Produção e Processo (Medição Fiscal e Sistema de Alívio)' \
    'Operações submarinas, poços, risers e equipamentos submarinos' \
    'Utilidades, geração de energia e sistemas auxiliares' \
    'Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos' \
  --llm-provider azure --perfil-modelos petrobras-nano-low --effort low \
  --embedder embedding-3-large-global --reranker none \
  --workers "${INV_WORKERS:-8}" --max-chamadas "${INV_MAX_CHAMADAS:-30000}" \
  --output "${INV_OUTPUT:-pipeline/inventario/saida_mais_4_topicos_v4_nano_low}" \
  ${EXTRA[@]+"${EXTRA[@]}"} "$@"
