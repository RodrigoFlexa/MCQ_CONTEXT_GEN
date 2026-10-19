#!/usr/bin/env bash
# No servidor: somente coordenação e chamadas Azure, sem leitura do corpus bruto.
set -euo pipefail
document_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd -- "$document_root"
document_python="$document_root/.venv-documento/bin/python"
if [[ -n "${DOCUMENT_PYTHON:-}" ]]; then
    document_python="$DOCUMENT_PYTHON"
elif [[ ! -x "$document_python" ]]; then
    document_python="$document_root/venv/bin/python"
    if [[ ! -x "$document_python" ]]; then document_python="$(command -v python3)"; fi
fi
exec "$document_python" -u -m pipeline.qa_research.document.batch run "$@"
