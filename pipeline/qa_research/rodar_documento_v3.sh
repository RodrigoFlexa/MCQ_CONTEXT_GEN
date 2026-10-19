#!/usr/bin/env bash
# Execute com bash a partir do checkout. Não prepara índices nem embeddings.
set -euo pipefail
document_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd -- "$document_root"
document_python="$document_root/.venv-documento/bin/python"
if [[ -n "${DOCUMENT_PYTHON:-}" ]]; then
    document_python="$DOCUMENT_PYTHON"
elif [[ ! -x "$document_python" ]]; then
    document_python="$document_root/venv/bin/python"
    if [[ ! -x "$document_python" ]]; then
        document_python="$(command -v python3)"
    fi
fi
document_args=(
    --packet pipeline/qa_research/pacotes/produtos_quimicos_v2
    --output pipeline/qa_research/saida_documento_produtos_quimicos_v3
    --results pipeline/qa_research/relatorios/produtos_quimicos_v3
)
if [[ -f pipeline/qa_research/relatorios/produtos_quimicos_v2/identidade.json ]]; then
    document_args+=(--reuse-research pipeline/qa_research/relatorios/produtos_quimicos_v2)
fi
exec "$document_python" -u -m pipeline.qa_research.document run "${document_args[@]}" "$@"
