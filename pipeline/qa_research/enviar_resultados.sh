#!/usr/bin/env bash
# Envia uma pasta de resultados do servidor para o GitHub.
# Uso: bash pipeline/qa_research/enviar_resultados.sh <pasta> ["mensagem do commit"]
# Na sua máquina, depois: git pull
set -euo pipefail
if [[ $# -lt 1 || ! -d "$1" ]]; then
    echo "Uso: bash pipeline/qa_research/enviar_resultados.sh <pasta de resultados> [\"mensagem\"]"
    exit 1
fi
qa_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd -- "$qa_root"
pasta="${1%/}"
mensagem="${2:-Resultados: $(basename "$pasta")}"

git pull --rebase --autostash
git add -- "$pasta"
if git diff --cached --quiet; then
    echo "Nada novo para enviar em $pasta."
    exit 0
fi
git commit -m "$mensagem"
git push
echo
echo "Enviado. Na sua máquina: git pull"
