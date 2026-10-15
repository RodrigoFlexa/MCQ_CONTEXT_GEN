#!/usr/bin/env bash
# Completa os 10 tópicos: roda os cinco que faltam depois de Lastro e dos quatro da segunda rodada.
# Uma execução, uma varredura lexical, um diretório de saída com quatro documentos por tópico.
# Uso: bash pipeline/inventario/run_ultimos_5_topicos_azure.sh [--plan | --check-api | outros args]
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
REUSE="${INV_REUSE:-pipeline/inventario/saida_mais_4_topicos_v4_nano_low}"
EXTRA=()
if [[ -d "$REUSE" ]]; then EXTRA+=(--reaproveitar-de "$REUSE"); fi
"${INV_PYTHON:-python3}" -u pipeline/inventario/run_inventario.py \
  --corpus-manifest "${INV_MANIFEST:-dataset/domain_corpora/manifest.json}" \
  --topicos 'Gestão do Desempenho Empresarial (KPI)' \
    'Manutenção, Inspeção e Integridade de Ativos' \
    'Segurança Ocupacional, Saúde e Meio Ambiente' \
    'Logística, Suprimentos e Movimentação de Cargas' \
    'Descomissionamento e Gestão do Ciclo de Vida da Unidade' \
  --llm-provider azure --perfil-modelos petrobras-nano-low --effort low \
  --embedder embedding-3-large-global --reranker none \
  --workers "${INV_WORKERS:-8}" --max-chamadas "${INV_MAX_CHAMADAS:-30000}" \
  --output "${INV_OUTPUT:-pipeline/inventario/saida_ultimos_5_topicos_v4_nano_low}" \
  ${EXTRA[@]+"${EXTRA[@]}"} "$@"
