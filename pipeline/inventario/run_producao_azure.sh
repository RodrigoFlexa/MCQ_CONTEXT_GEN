#!/usr/bin/env bash
# Documentos do próximo tópico (12 subtópicos), com revisão/refinamento.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
"${INV_PYTHON:-python3}" -u pipeline/inventario/run_inventario.py \
  --corpus-manifest "${INV_MANIFEST:-dataset/domain_corpora/manifest.json}" \
  --topicos 'Produção e Processo (Medição Fiscal e Sistema de Alívio)' \
  --llm-provider azure --llm-model gpt-5-4-petrobras --effort medium \
  --embedder embedding-3-large-global --reranker none \
  --workers 2 --review-batch 8 --max-chamadas "${INV_MAX_CHAMADAS:-30000}" \
  --output "${INV_OUTPUT:-pipeline/inventario/saida_producao_v3_correcao_azure}" "$@"
