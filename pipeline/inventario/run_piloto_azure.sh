#!/usr/bin/env bash
# Apenas documentos do tópico KPI. Ex.: bash pipeline/inventario/run_piloto_azure.sh --plan
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
"${INV_PYTHON:-python3}" -u pipeline/inventario/run_inventario.py \
  --corpus-manifest "${INV_MANIFEST:-dataset/domain_corpora/manifest.json}" \
  --topicos 'Gestão do Desempenho Empresarial (KPI)' \
  --llm-provider azure --llm-model gpt-5-4-petrobras --effort medium \
  --embedder embedding-3-large-global --reranker none \
  --workers 2 --max-chamadas 400 \
  --output "${INV_OUTPUT:-pipeline/inventario/saida_piloto_kpi_azure}" "$@"
