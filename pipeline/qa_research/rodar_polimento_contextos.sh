#!/usr/bin/env bash
set -euo pipefail
export PYTHONUTF8=1
qa_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd -- "$qa_root"
qa_python="${DOCUMENT_PYTHON:-$qa_root/.venv-documento/bin/python}"
if [[ ! -x "$qa_python" ]]; then
    echo "Python não encontrado: $qa_python. Defina DOCUMENT_PYTHON para o ambiente instalado."
    exit 1
fi
exec "$qa_python" -u -m pipeline.qa_research.polimento "$@"
