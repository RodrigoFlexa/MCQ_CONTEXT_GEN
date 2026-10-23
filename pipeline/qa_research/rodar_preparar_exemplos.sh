#!/usr/bin/env bash
# Instala (só o que falta), limpa e revisa por LLM no Azure os exemplos externos:
# Pirá, MMMLU PT-BR, ARC-Challenge e QASC.
# Uso: bash pipeline/qa_research/rodar_preparar_exemplos.sh [opções]
#   --sem-revisao                         só instalação e limpeza por regras
#   --modelo-revisao gpt-5-mini-petrobras:low   (padrão: gpt-5-4-nano-petrobras:low)
#   --forcar-download                     baixa de novo mesmo o que já está instalado
set -uo pipefail
export PYTHONUTF8=1
qa_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd -- "$qa_root"
qa_python="$qa_root/.venv-documento/bin/python"
if [[ -n "${DOCUMENT_PYTHON:-}" ]]; then
    qa_python="$DOCUMENT_PYTHON"
elif [[ ! -x "$qa_python" ]]; then
    qa_python="$qa_root/venv/bin/python"
    if [[ ! -x "$qa_python" ]]; then qa_python="$(command -v python3)"; fi
fi

args=()
revisao=1
for a in "$@"; do
    if [[ "$a" == "--sem-revisao" ]]; then revisao=0; else args+=("$a"); fi
done
if [[ $revisao -eq 1 ]]; then args+=("--revisao-llm"); fi

"$qa_python" -u -m pipeline.qa_references.preparar_exemplos "${args[@]}"
status=$?
if [[ $status -eq 0 ]]; then
    echo
    echo "O código acabou de rodar no terminal :)"
    echo
    echo "Relatório da limpeza: pipeline/qa_references/limpeza/RELATORIO.md"
    echo "Para enviar o relatório (os dados ficam no servidor, fora do git):"
    echo "  bash pipeline/qa_research/enviar_resultados.sh pipeline/qa_references/limpeza \"Limpeza dos exemplos externos\""
    echo
    echo "Próximo passo:"
    echo "  bash pipeline/qa_research/rodar_experimento_externos.sh --limite 2   # teste rápido"
    echo "  bash pipeline/qa_research/rodar_experimento_externos.sh              # completo"
fi
exit $status
